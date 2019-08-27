"""
NOTE: The exception handler defined here is not used in the project. It was
written for practice and to get a better understanding of DRF.

We want errors to be sent back under the namespace of 'errors'. By default, if
we are not using field specific validation methods, (i.e. override validate
method), errors are returned under 'non_field_errors' namespace.

    'NON_FIELD_ERRORS_KEY': 'errors',
"""

from rest_framework.views import exception_handler as drf_exception_handler


def _add_namespace_error(_, __, response):
    response.data = {
        'errors': response.data
    }

    return response


def exception_handler(exception, context):
    # let DRF handle the exception
    response = drf_exception_handler(exception, context)

    # exceptions that we care about
    handlers = {
        'ValidationError': _add_namespace_error
    }
    # identify the type of the current exception
    exception_class = exception.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exception, context, response)

    return response
