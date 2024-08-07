from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


class CustomUserRateThrottle(UserRateThrottle):
    rate = '3/minute'


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
