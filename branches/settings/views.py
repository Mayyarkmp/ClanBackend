from rest_framework.response import Response
from core.base.viewsets import SuperGenericViewSet
from .utils import get_branch_settings


class BranchSettingsViewSet(SuperGenericViewSet):
    def list(self, request, *args, **kwargs):
        settings = get_branch_settings()

        return Response(settings)
