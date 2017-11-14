from rest_framework import throttling


class CustomThrottle(throttling.UserRateThrottle):
    rate = '1000/day'
