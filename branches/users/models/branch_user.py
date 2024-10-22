import uuid
from polymorphic.managers import PolymorphicManager


from users.models import User
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from core.base.models import TimeStampedModel

class Status(models.TextChoices):
    ACTIVE = "ACTIVE", _('Active')
    INACTIVE = "INACTIVE", _('Inactive')
    REVIEWING = "REVIEWING", _('Reviewing')
    STOPPED = "STOPPED", _('Stopped')
    BLOCKED = "BLOCKED", _('Blocked')


class BranchUserManager(PolymorphicManager):
    def create(self, **kwargs):
        branch = kwargs.get('branch')
        if not branch:
            raise ValueError("Branch must be set before creating a Delivery user.")
        return super().create(**kwargs)


class BranchUser(User):
    objects = BranchUserManager()
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, default=Status.REVIEWING, max_length=50)
    online = models.BooleanField(default=False)
    location = models.PointField(blank=True, null=True, srid=4326)

    def __str__(self):
        return self.username + " " + self.branch.name


class WorkPeriod(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(BranchUser, on_delete=models.CASCADE, related_name='work_periods')
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self) -> str:
        return f'{self.start} - {self.end}'


class Zone(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "Active", _("Active")
        INACTIVE = "Inactive", _("Inactive")
        PENDING = "Pending", _("Pending")

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(BranchUser, on_delete=models.CASCADE, related_name='zones')
    area = models.PolygonField(_("Area Zone"))
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)
    duration = models.DurationField()