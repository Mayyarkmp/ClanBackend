from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.media"
    label = "media"

    def ready(self):
        import core.media.signals
