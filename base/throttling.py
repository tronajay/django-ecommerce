from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled


class CustomUserLoginThrottle(AnonRateThrottle):
    rate = "10/day"
