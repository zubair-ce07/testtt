from rest_framework import throttling


class CustomThrottle(throttling.UserRateThrottle):
    rate = '100/day'
