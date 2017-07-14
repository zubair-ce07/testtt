from rest_framework import throttling


class MyCustomThrottle(throttling.UserRateThrottle):
    rate = '100/day'
