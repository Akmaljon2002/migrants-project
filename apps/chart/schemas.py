from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.chart.serializers import ChartResponseSerializer

chart_stats_schema = extend_schema(
    tags=["Chart Statistics"],
    operation_id="Chart Statistics",
    description="Retrieve chart statistics for border crosses.",
    responses={
        200: "Chart statistics data.",
        400: "Bad request."
    }
)

AVAILABLE_STATS = [
    "migrants_by_country",
    "migrants_by_region",
    "migration_purpose",
    "transport_type",
]

chart_stats_schema_all = extend_schema(
    tags=["Chart Statistics"],
    operation_id="Chart Statistics All",
    description="Retrieve chart statistics for a specific metric.",
    parameters=[
        OpenApiParameter(
            name="stat_name",
            type=str,
            required=True,
            description="Name of the statistic",
            enum=AVAILABLE_STATS
        ),
    ],
    responses={200: ChartResponseSerializer},
)