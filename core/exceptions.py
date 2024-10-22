from rest_framework.views import  exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        response.data = {
            'status': 'error',
            'errors': response.data,
            'message': 'There was an error processing your request'
        }

    return response
