import datetime

from attr.validators import min_len
from django.contrib.auth import get_user_model
import uuid
import os
from django.utils.deconstruct import deconstructible
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from core.base.models import TimeStampedModel

User = get_user_model()


@deconstructible
class PathAndRename:
    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{datetime.datetime.now(tz=datetime.timezone.utc).isoformat()}.{format(ext)}"
        return os.path.join(
            "media", "chat", str(instance.room.uid), str(instance.sender.uid), filename
        )


class Room(TimeStampedModel):
    uid = models.UUIDField(_("UID"), unique=True, default=uuid.uuid4, editable=False,)
    members = models.ManyToManyField(
        User, verbose_name=_("Members"), max_length=2, related_name="rooms",
    )
    creator = models.CharField(
        _("Creator"), max_length=100, blank=True, null=True, db_index=True
    )
    name = models.CharField(_("Name"), max_length=100, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_blocked = models.BooleanField(_("Is Blocked"), default=False)

    def __str__(self):
        return f"{self.uid.__str__()})"


class Message(models.Model):
    class Types(models.TextChoices):
        TEXT = "TEXT", _("Text")
        IMAGE = "IMAGE", _("Image")
        VIDEO = "VIDEO", _("Video")
        AUDIO = "AUDIO", _("Audio")
        FILE = "FILE", _("File")
        LOCATION = "LOCATION", _("Location")
        CONTACT = "CONTACT", _("Contact")
        VOICE = "VOICE", _("Voice")

    uid = models.UUIDField(
        _("UID"), unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Room"),
        db_index=True,
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name=_("Sender"),
        db_index=True,
    )
    message = models.TextField(_("Message"), null=True, blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)
    sending_datetime = models.DateTimeField(
        _("Sending Datetime"), blank=True, null=True
    )
    receiving_datetime = models.DateTimeField(
        _("Receiving Datetime"), blank=True, null=True
    )
    reading_datetime = models.DateTimeField(
        _("Reading Datetime"), blank=True, null=True
    )
    editing_datetime = models.DateTimeField(
        _("Editing Datetime"), blank=True, null=True
    )
    is_edited = models.BooleanField(_("Is Edited"), default=False)
    is_read = models.BooleanField(_("Is Read"), default=False)
    is_sent = models.BooleanField(_("Is Sent"), default=False)
    is_received = models.BooleanField(_("Is Received"), default=False)
    type = models.CharField(
        _("Type"), choices=Types.choices, default=Types.TEXT, max_length=20
    )
    file = models.FileField(_("File"), upload_to=PathAndRename(), null=True, blank=True)
    location = models.PointField(_("Location"), null=True, blank=True)
    old_messages = models.JSONField(_("Old Content"), blank=True, null=True)

    class Meta:
        ordering = ("timestamp",)

    def __str__(self):
        return f"{self.sender}  : {self.room}"
