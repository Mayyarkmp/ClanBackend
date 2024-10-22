from django.conf import settings
from django_user_agents.utils import get_user_agent

class Utils:
    @staticmethod
    def get_language(request):
        languages = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        if languages:
            preferred_language = languages.split(',')[0]
            return preferred_language.split(';')[0][:2]
        return settings.LANGUAGE_CODE

