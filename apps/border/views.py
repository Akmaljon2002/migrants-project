from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.border.models import BorderCross
from apps.border.schemas import border_viewset_schema
from apps.border.serializers import BorderCrossSerializer


@border_viewset_schema
class BorderCrossViewSet(viewsets.ModelViewSet):
    queryset = BorderCross.objects.all()
    serializer_class = BorderCrossSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return BorderCross.objects.all().order_by("reg_date")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values("id", "reg_date", "endpoint_id", "direction_type_code", "migrant_id",
                                          "trip_purpose_id", "transport_type_code_id",
                                          "driection_country_id")
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(queryset)
