from guardian.shortcuts import assign_perm, remove_perm
from rest_framework.response import Response
from rest_framework import status

from core.base.viewsets import SuperModelViewSet
from .serializers import PermissionSerializer, GroupSerializer
from django.contrib.auth.models import Group, Permission


class PermissionViewSet(SuperModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    parent_lookup_kwargs = {
        "group_pk": ["group__pk"],
        "central_user_pk": ["user__pk"],
    }


    def create(self, request, group_pk=None):
        group = Group.objects.get(pk=group_pk) if group_pk else None
        perm = request.data.get('perm')

        if perm:
            if group:
                assign_perm(perm, group)
                return Response({'status': 'permission added to group'}, status=status.HTTP_201_CREATED)
            else:
                assign_perm(perm)
                return Response({'status': 'permission added globally'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'permission not provided'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, group_pk=None):
        group = Group.objects.get(pk=group_pk) if group_pk else None
        perm = self.get_object()

        if group:
            remove_perm(perm.codename, group)
            return Response({'status': 'permission removed from group'}, status=status.HTTP_204_NO_CONTENT)

        remove_perm(perm.codename)
        return Response({'status': 'permission removed globally'}, status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(SuperModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    parent_lookup_kwargs = {
        "central_user_pk": ["user__pk"],
    }


