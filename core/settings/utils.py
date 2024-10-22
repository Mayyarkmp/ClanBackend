from django.contrib.contenttypes.models import ContentType
from .models import GeneralSettings

#
# class Utils:
#     @staticmethod
#     def get_settings()


def get_settings():
    """Get Global Settings"""
    global_type = ContentType.objects.get_for_model(GeneralSettings)
    settings = GeneralSettings.objects.filter(polymorphic_ctype=global_type)
    obj = {}
    for setting in settings:
        obj[setting.key] = {
            "type": setting.type,
            "value_type": setting.value_type,
            "value": setting.value,
        }

    return obj
