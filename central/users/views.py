from django.db.models import Q

from .models import CentralUser, AssignedBranches, Grade, WorkPeriod
from core.base.viewsets import SuperModelViewSet
from .serializers import CentralUserSerializer, AssignedBranchesSerializer, GradeSerializer, WorkPeriodSerializer


class GradeViewSet(SuperModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    parent_lookup_kwargs = {
        "central_user_pk": ["users__pk"],
    }



class CentralUserViewSet(SuperModelViewSet):
    queryset = CentralUser.objects.all()
    serializer_class = CentralUserSerializer
    parent_lookup_kwargs = {
        "grade_pk": ["grade__pk"],
        "branch_pk": ["assigned_branches__branches__pk"],
    }


class AssignedBranchesViewSet(SuperModelViewSet):
    queryset = AssignedBranches.objects.all()
    serializer_class = AssignedBranchesSerializer


class WorkPeriodViewSet(SuperModelViewSet):
    queryset = WorkPeriod.objects.all()
    serializer_class = WorkPeriodSerializer
    parent_lookup_kwargs = {
        "central_user_pk": ["user__pk"],
        "grade_pk": ["user__grade__pk"]
    }
