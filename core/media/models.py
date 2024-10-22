import uuid
import os
from django.db import models
from django.utils.deconstruct import deconstructible
from ..base.models import TimeStampedModel


@deconstructible
class PathAndRename:
    def __init__(self, sub_path="media"):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # استخراج امتداد الملف واسم الملف الأساسي
        ext = filename.split(".")[-1]
        base_filename = os.path.splitext(filename)[0]

        # استخدام اسم الملف الأصلي
        new_filename = f"{base_filename}.{ext}"

        # التحقق مما إذا كان الكائن يحتوي على الخاصية `custom_upload_path`
        if hasattr(instance, "custom_upload_path"):
            # استخدام المسار المخصص
            upload_path = os.path.join(
                self.sub_path, instance.custom_upload_path, new_filename
            )
        else:
            # المسار الافتراضي
            upload_path = os.path.join(self.sub_path, str(instance.uid), new_filename)

        return upload_path


class Media(TimeStampedModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=PathAndRename())
    file_type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.uid)
