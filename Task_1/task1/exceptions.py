from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        errors = {}
        for field, value in response.data.items():
            errors.update({field: value})
        response.data = dict()
        response.data['response'] = None
        response.data['success'] = False
        response.data['message'] = errors
    return response
