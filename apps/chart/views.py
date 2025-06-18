from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chart.chart_configs import get_chart_config
from apps.chart.schemas import chart_stats_schema, chart_stats_schema_all
from utils.clickhouse import client


def execute_clickhouse_query(query):
    result = client.execute(query)
    return result


@chart_stats_schema
class BaseChartAPIView(APIView):
    permission_classes = [AllowAny]
    query: str = ''
    label_field: str = 'label'
    value_field: str = 'value'

    def get(self, request):
        rows = execute_clickhouse_query(self.query)
        data = [
            {self.label_field: row[0], self.value_field: row[1]}
            for row in rows
        ]
        return Response(data)


@chart_stats_schema
class LongTrips(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = execute_clickhouse_query("""
            SELECT COUNT(DISTINCT migrant_id)
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
              AND reg_date <= today() - 30
        """)
        return Response({"label": "30_days_plus", "value": result[0][0]})


@chart_stats_schema
class VeryLongTrips(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = execute_clickhouse_query("""
            SELECT COUNT(DISTINCT migrant_id)
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
              AND reg_date <= today() - 90
        """)
        return Response({"label": "90_days_plus", "value": result[0][0]})



class MigrantsByCountry(BaseChartAPIView):
    query = """
        SELECT driection_country_id, COUNT(*) as count
        FROM border_cross_data
        WHERE direction_type_code = 'OUT'
        GROUP BY driection_country_id
        ORDER BY count DESC
    """
    label_field = "driection_country_id"
    value_field = "count"


class MigrantsByRegion(BaseChartAPIView):
    query = """
        SELECT region_id, COUNT(*) as count
        FROM migrant_data
        GROUP BY region_id
        ORDER BY count DESC
    """
    label_field = "region_id"
    value_field = "count"


class MigrationPurposeStats(BaseChartAPIView):
    query = """
        SELECT trip_purpose_id, COUNT(*) as count
        FROM border_cross_data
        GROUP BY trip_purpose_id
        ORDER BY count DESC
    """
    label_field = "trip_purpose_id"
    value_field = "count"


class TransportStats(BaseChartAPIView):
    query = """
        SELECT transport_type_code_id, COUNT(*) as count
        FROM border_cross_data
        GROUP BY transport_type_code_id
        ORDER BY count DESC
    """
    label_field = "transport_type_code_id"
    value_field = "count"


@chart_stats_schema_all
class ChartStatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, stat_name):
        config = get_chart_config(stat_name)
        if not config:
            raise NotFound(f"Stat '{stat_name}' not found.")

        rows = execute_clickhouse_query(config["query"])
        return Response({
            "title": config["title"],
            "data": [{"label": str(r[0]), "value": r[1]} for r in rows if len(r) >= 2]
        })
