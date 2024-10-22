from django.utils.functional import SimpleLazyObject
from utils import Utils


class LanguageMiddleware(object):
    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        request.language = SimpleLazyObject(lambda: Utils.get_language(request))
