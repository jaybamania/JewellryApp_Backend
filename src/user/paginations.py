from rest_framework.pagination import LimitOffsetPagination


class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 40
    max_limit = 40
