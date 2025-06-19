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
            SELECT COUNT(*)
            FROM (
                SELECT migrant_id, reg_date,
                       ROW_NUMBER() OVER (PARTITION BY migrant_id ORDER BY created_at DESC) AS rn
                FROM border_cross_data
                WHERE direction_type_code = 'OUT'
            )
            WHERE rn = 1 AND reg_date <= today() - 30
        """)
        return Response({"label": "30_days_plus", "value": result[0][0]})


@chart_stats_schema
class VeryLongTrips(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = execute_clickhouse_query("""
            SELECT COUNT(*)
            FROM (
                SELECT migrant_id, reg_date,
                       ROW_NUMBER() OVER (PARTITION BY migrant_id ORDER BY created_at DESC) AS rn
                FROM border_cross_data
                WHERE direction_type_code = 'OUT'
            )
            WHERE rn = 1 AND reg_date <= today() - 90
        """)
        return Response({"label": "90_days_plus", "value": result[0][0]})



class MigrantsByCountry(BaseChartAPIView):
    query = """
        SELECT driection_country_id, COUNT(*) as count
        FROM (
            SELECT driection_country_id,
                   ROW_NUMBER() OVER (PARTITION BY migrant_id ORDER BY created_at DESC) AS rn
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
        )
        WHERE rn = 1 AND driection_country_id IS NOT NULL
        GROUP BY driection_country_id
        ORDER BY count DESC
    """
    label_field = "driection_country_id"
    value_field = "count"

class MigrantsByRegion(BaseChartAPIView):
    query = """
        SELECT m.region_id, COUNT(*) as count
        FROM (
            SELECT
                migrant_id,
                ROW_NUMBER() OVER (PARTITION BY migrant_id ORDER BY created_at DESC) AS rn
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
        ) AS latest
        INNER JOIN migrant_data m ON latest.migrant_id = m.id
        WHERE latest.rn = 1
        GROUP BY m.region_id
        ORDER BY count DESC
    """
    label_field = "region_id"
    value_field = "count"

class MigrationPurposeStats(BaseChartAPIView):
    query = """
        SELECT trip_purpose_id, COUNT(*) as count
        FROM (
            SELECT trip_purpose_id,
                   ROW_NUMBER() OVER (PARTITION BY migrant_id ORDER BY created_at DESC) AS rn
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
        )
        WHERE rn = 1 AND trip_purpose_id IS NOT NULL
        GROUP BY trip_purpose_id
        ORDER BY count DESC
    """
    label_field = "trip_purpose_id"
    value_field = "count"


class TransportStats(BaseChartAPIView):
    query = """
            SELECT transport_type_code_id, COUNT(*) as count
            FROM (
                SELECT
                    transport_type_code_id,
                    ROW_NUMBER() OVER (PARTITION BY migrant_id ORDER BY created_at DESC) AS rn
                FROM border_cross_data
                WHERE direction_type_code = 'OUT'
            )
            WHERE rn = 1
            GROUP BY transport_type_code_id
            ORDER BY count DESC
        """
    label_field = "transport_type_code_id"
    value_field = "count"


@chart_stats_schema_all
class ChartStatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        stat_name = request.query_params.get("stat_name")
        config = get_chart_config(stat_name)
        if not config:
            raise NotFound(f"Stat '{stat_name}' not found.")

        rows = execute_clickhouse_query(config["query"])
        return Response({
            "title": config["title"],
            "data": [{"label": str(r[0]), "value": r[1]} for r in rows if len(r) >= 2]
        })


class GeneralStatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        stats = client.execute("""
            SELECT
                COUNT(DISTINCT bcd.migrant_id) AS total_migrants,
                (SELECT COUNT(DISTINCT region_id) FROM migrant_data) AS total_regions,
                (
                    SELECT driection_country_id
                    FROM border_cross_data
                    WHERE direction_type_code = 'OUT'
                    GROUP BY driection_country_id
                    ORDER BY COUNT(DISTINCT migrant_id) DESC
                    LIMIT 1
                ) AS top_country_id,
                (
                    SELECT COUNT(DISTINCT migrant_id)
                    FROM border_cross_data
                    WHERE direction_type_code = 'OUT' AND reg_date <= today() - 30
                ) AS over_30_days,
                (
                    SELECT COUNT(DISTINCT migrant_id)
                    FROM border_cross_data
                    WHERE direction_type_code = 'OUT' AND reg_date <= today() - 90
                ) AS over_90_days,
                AVG(toInt32((toDateTime(bcd.reg_date) - bcd.created_at) / 86400)) AS avg_duration
            FROM border_cross_data AS bcd
            WHERE bcd.direction_type_code = 'OUT'
        """)[0]

        gender_data = client.execute("""
            SELECT gender, COUNT(id) as count
            FROM migrant_data
            WHERE gender IS NOT NULL
            GROUP BY gender
        """)
        total_gender = sum([row[1] for row in gender_data])
        gender_stats = [
            {"gender": row[0], "count": row[1], "percent": round((row[1] / total_gender) * 100, 1)}
            for row in gender_data
        ]

        age_data = client.execute("""
            SELECT (toYear(now()) - toYear(birth_date)) AS age, COUNT(id) as count
            FROM migrant_data
            WHERE birth_date IS NOT NULL
            GROUP BY age
            ORDER BY count DESC
            LIMIT 1
        """)
        age_group = {"age": age_data[0][0], "count": age_data[0][1]} if age_data else None

        transport = client.execute("""
            SELECT transport_type_code_id, COUNT(DISTINCT migrant_id) as count
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
            GROUP BY transport_type_code_id
            ORDER BY count DESC
            LIMIT 1
        """)
        transport_type = {"transport_type": transport[0][0], "count": transport[0][1]} if transport else None

        return Response({
            "total_migrants": stats[0],
            "total_regions": stats[1],
            "top_country": {"country_id": stats[2]},
            "migrants_over_30_days": stats[3],
            "migrants_over_90_days": stats[4],
            "average_trip_duration_days": int(stats[5]) if stats[5] else None,
            "gender_ratio": gender_stats,
            "top_age_group": age_group,
            "top_transport_type": transport_type,
        })
