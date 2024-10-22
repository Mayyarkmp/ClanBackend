from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        from activity import registry
        registry.register(
            self.get_model('Message'),
            self.get_model('Room'),
        )
