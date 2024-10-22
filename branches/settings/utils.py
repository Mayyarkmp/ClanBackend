from .models import BranchSettings
from core.settings.utils import get_settings


def get_branch_settings(branch):
    branch_settings = BranchSettings.objects.filter(branch=branch)
    global_settings = get_settings()
    settings = {}

    for branch_setting in branch_settings:
        settings[branch_setting.key] = {
            "type": branch_setting.type,
            "value_type": branch_setting.value_type,
            "value": branch_setting.value,
        }

    for setting in global_settings:

        if hasattr(setting, "key") and getattr(setting, "key") in settings.values():
            settings[setting.key] = {
                "type": setting.type,
                "value_type": setting.value_type,
                "value": setting.value,
            }

    return settings


def get_global_branch_settings():
    pass
