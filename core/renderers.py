from rest_framework.renderers import JSONRenderer
from django.utils.translation import gettext_lazy as _


class ClanRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if response.status_code < 400:
            message = renderer_context.get('message', _('Request was successful'))
            response_data = {
                'status': 'success',
                'data': data,
                'message': message,
            }
        else:
            message = renderer_context.get('error_message', _('There was an error processing your request'))
            response_data = {
                'status': 'error',
                'errors': data,
                'message': message,
            }

        return super(ClanRenderer, self).render(response_data, accepted_media_type, renderer_context)
