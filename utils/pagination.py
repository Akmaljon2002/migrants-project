from urllib.parse import urlencode
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50


class BaseService:
    def __init__(self, request: Request):
        self.request: Request = request

    def query(self, param: str, default=None):
        return self.request.GET.get(param, default)


class BaseServicePagination:
    def __init__(self, request: Request):
        self.request: Request = request
        self.pagination = Pagination()

    def query(self, param: str, default=None):
        return self.request.GET.get(param, default)

    def paginate(self, queryset: QuerySet):
        return self.pagination.paginate_queryset(
            queryset,
            self.request
        )

    def paginated_response(self, data: list):
        return self.pagination.get_paginated_response(
            data
        )


def build_pagination_links(request, page, page_size, total_count):
    base_url = request.build_absolute_uri(request.path)
    query_params = request.query_params.copy()

    def get_link(new_page):
        query_params["page"] = new_page
        return f"{base_url}?{urlencode(query_params)}"

    next_link = get_link(page + 1) if (page * page_size) < total_count else None
    prev_link = get_link(page - 1) if page > 1 else None

    return next_link, prev_link


class BaseManualServicePagination:
    def __init__(self, request: Request):
        self.request = request
        self.limit = 10
        self.offset = 0

    def query(self, param: str, default=None):
        return self.request.GET.get(param, default)

    def paginate(self, queryset: QuerySet):
        try:
            self.limit = min(int(self.request.GET.get('limit', 10)), 100)
            self.offset = max(int(self.request.GET.get('offset', 0)), 0)
        except ValueError:
            self.limit = 10
            self.offset = 0

        return queryset[self.offset:self.offset + self.limit]

    def paginated_response(self, data: list):
        return Response({
            "limit": self.limit,
            "offset": self.offset,
            "results": data
        })