from django.contrib.sessions.backends.db import SessionStore
from django.utils.deprecation import MiddlewareMixin


class EnsureSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.COOKIES.get('session_key')

        if session_key:
            try:
                request.session = SessionStore(session_key=session_key)
                if not request.session.exists(session_key):
                    self.create_new_session(request)
            except:
                self.create_new_session(request)
        else:
            self.create_new_session(request)


    def create_new_session(self, request):
        request.session = SessionStore()
        request.session.create()

    def process_response(self, request, response):
        if hasattr(request, 'session') and request.session.session_key:
            response.set_cookie('session_key', request.session.session_key)
        return response
