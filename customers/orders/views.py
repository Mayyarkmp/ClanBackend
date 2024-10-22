from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Q
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from branches.models import BranchServiceZone, DeliveryTimeSlot
from core.settings.models.location import GeographicalZone
from customers.models import BrowsingKey
from customers.orders.serializers import (
    CheckDeliverySerializer,
)


class CheckDeliveryView(APIView):
    def post(self, request):
        serializer = CheckDeliverySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_location = serializer.create_point()

        zones = GeographicalZone.objects.filter(
            status=GeographicalZone.Status.ACTIVE
        ).filter(
            Q(polygon__contains=user_location)
            | Q(city__polygon__contains=user_location)
            | Q(subregion__polygon__contains=user_location)
            | Q(region__polygon__contains=user_location)
            | Q(country__polygon__contains=user_location)
        )

        if not zones.exists():
            return Response(
                {"status": "not available"}, status=status.HTTP_404_NOT_FOUND
            )

        service_zones = BranchServiceZone.objects.filter(
            status=BranchServiceZone.Status.ACTIVE,
            area__in=zones,
            branch__is_active=True,
        )

        results = []
        for zone in service_zones:
            data = {
                "branch": zone.branch.name,
                "delivery_type": zone.delivery_type,
                "zone_type": zone.zone_type,
            }
            if zone.zone_type == "CUSTOM_TIME":
                current_day = datetime.now().weekday()
                current_time = datetime.now().time()
                time_slots = zone.time_slots.filter(status="ACTIVE").filter(
                    Q(day_of_week=current_day)
                    | Q(day_of_week=DeliveryTimeSlot.DaysOfWeek.ALL)
                )
                available = any(
                    slot.start_time <= current_time <= slot.end_time
                    for slot in time_slots
                )
                data["available_now"] = available
            else:
                data["available_now"] = True

            results.append(data)

        browsing_key = BrowsingKey.objects.create()

        if not results:
            return Response(
                {"status": "not available"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "status": "available",
                "services": results,
                "key": browsing_key.key,
            },
            status=status.HTTP_200_OK,
        )
