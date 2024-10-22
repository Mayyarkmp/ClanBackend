from django.db.models import Q
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from branches.models import Branch, BranchServiceZone, DeliveryTimeSlot
from branches.users.models.manager import Manager
from branches.serializers import (
    BranchSerializer,
    BranchServiceZoneSerializer,
    DeliveryTimeSlotSerializer,
)
from core.base.viewsets import SuperModelViewSet


class BranchViewSet(SuperModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    parent_lookup_kwargs = {
        "central_user_pk": ["central_staffs__user__pk"],
        "product_pk": ["products__product__pk"],
    }

    # Manager creates the first branch when signing up
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        serializer.save(owner=user)

        return Response(serializer.data)

    # After first branch creation from Manager, he can create more branches too
    @action(detail=False, methods=["post"], url_path="create-active-manager-branch")
    def createBranchForActiveManager(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner_uid = serializer.validated_data.get("owner")

        try:
            manager = Manager.objects.get(user__uid=owner_uid)
        except Manager.DoesNotExist:
            return Response(
                {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if not manager.is_active:
            return Response(
                {"error": "Manager account is not active"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        branch_data = serializer.validated_data
        branch = Branch.objects.create(
            **branch_data,
            status=Branch.Status.REVIEWING,
            owner=manager.user,
        )
        return Response(BranchSerializer(branch).data, status=status.HTTP_201_CREATED)


class BranchServiceZoneViewSet(SuperModelViewSet):
    queryset = BranchServiceZone.objects.all()
    serializer_class = BranchServiceZoneSerializer
    parent_lookup_kwargs = {
        "branch_pk": ["branch__pk"],
    }


class DeliveryTimeSlotViewSet(SuperModelViewSet):
    queryset = DeliveryTimeSlot.objects.all()
    serializer_class = DeliveryTimeSlotSerializer
    parent_lookup_kwargs = {
        "branch_pk": ["service_area__branch__pk"],
    }
