from drf_spectacular.utils import extend_schema
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

chart_stats_schema_all = extend_schema(
    tags=["Chart Statistics"],
    operation_id="Chart Statistics All",
    description="Retrieve all chart statistics for border crosses.",
    responses={200: ChartResponseSerializer},
)