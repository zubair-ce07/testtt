import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import serializers


def email_validation(value):
    try:
        validate_email(value)
    except ValidationError:
        raise serializers.ValidationError('Email address entered is not correct')


def dob_validation(date):
    days = date - datetime.datetime.now().date()
    age = (abs(days)/365).days
    if age < 13:
        raise serializers.ValidationError('You mush be at least 13 yrs old to join learnerapp')

