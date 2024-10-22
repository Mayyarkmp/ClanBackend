import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from core.base.models import TimeStampedModel
from users.models import UserManager, User


class Status(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")
    REVIEWING = "REVIEWING", _("Reviewing")
    STOPPED = "STOPPED", _("Stopped")
    BLOCKED = "BLOCKED", _("Blocked")


class Grade(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)
    name_en = models.CharField(_("English Name"), max_length=100, null=True, blank=True)
    codename = models.SlugField(_("Codename"), max_length=100)


class ClanUserManager(UserManager):
    pass


class CentralUser(User, PolymorphicModel):
    grade = models.ForeignKey(
        Grade, on_delete=models.PROTECT, related_name="users", blank=True, null=True
    )
    status = models.CharField(
        choices=Status.choices, default=Status.REVIEWING, max_length=50
    )
    online = models.BooleanField(default=False)
    objects = ClanUserManager()

    @property
    def type(self):
        return "central"


class AssignedBranches(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    branches = models.ManyToManyField(
        "branches.Branch", verbose_name=_("Branches"), related_name="central_staffs"
    )
    user = models.OneToOneField(
        CentralUser,
        verbose_name=_("Staff"),
        on_delete=models.CASCADE,
        related_name="assigned_branches",
    )

    def __str__(self) -> str:
        return self.user.username + f" ({self.branches.count()} branch)"


class WorkPeriod(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CentralUser,
        on_delete=models.CASCADE,
        related_name="work_periods",
        verbose_name=_("Staff"),
    )
    start = models.TimeField(_("Start Time"))
    end = models.TimeField(_("End Time"))

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"
