from rest_framework import status
from rest_framework.response import Response


def invalid_serializer_response(serializer):
    return Response(
        {'error': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


def missing_attribute_response(missing_attr):
    return Response(
        {'error': "missing attribute '{0}'".format(missing_attr)},
        status=status.HTTP_400_BAD_REQUEST
    )
