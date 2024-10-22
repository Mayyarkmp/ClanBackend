from django.apps import AppConfig


class ContentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.contents'
    label = 'contents'

    def ready(self):
        import core.contents.signals
