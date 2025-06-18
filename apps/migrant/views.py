from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.migrant.models import Migrant
from apps.migrant.schemas import migrant_viewset_schema
from apps.migrant.serializers import MigrantSerializer


@migrant_viewset_schema
class MigrantViewSet(viewsets.ModelViewSet):
    queryset = Migrant.objects.all()
    serializer_class = MigrantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Migrant.objects.all().order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = Migrant.objects.values(
            "id", "first_name", "last_name", "region_id", "district_id", "pinfl", "created_at"
        ).order_by("-created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(queryset)