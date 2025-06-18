from apps.chart.constants import ChartStatChoices

CHART_CONFIGS = {
    ChartStatChoices.MIGRANTS_BY_COUNTRY: {
        "query": """
            SELECT driection_country_id, COUNT(*) as count
            FROM border_cross_data
            WHERE direction_type_code = 'OUT'
            GROUP BY driection_country_id
            ORDER BY count DESC
        """,
        "label": "driection_country_id",
        "value": "count",
        "title": ChartStatChoices.MIGRANTS_BY_COUNTRY.label,
    },
    ChartStatChoices.MIGRANTS_BY_REGION: {
        "query": """
            SELECT region_id, COUNT(*) as count
            FROM migrant_data
            GROUP BY region_id
            ORDER BY count DESC
        """,
        "label": "region_id",
        "value": "count",
        "title": ChartStatChoices.MIGRANTS_BY_REGION.label,
    },
    ChartStatChoices.MIGRATION_PURPOSE: {
        "query": """
            SELECT trip_purpose_id, COUNT(*) as count
            FROM border_cross_data
            GROUP BY trip_purpose_id
            ORDER BY count DESC
        """,
        "label": "trip_purpose_id",
        "value": "count",
        "title": ChartStatChoices.MIGRATION_PURPOSE.label,
    },
    ChartStatChoices.TRANSPORT_TYPE: {
        "query": """
            SELECT transport_type_code_id, COUNT(*) as count
            FROM border_cross_data
            GROUP BY transport_type_code_id
            ORDER BY count DESC
        """,
        "label": "transport_type_code_id",
        "value": "count",
        "title": ChartStatChoices.TRANSPORT_TYPE.label,
    },
}

def get_chart_config(stat_name: str):
    if stat_name not in ChartStatChoices.values:
        return None
    return CHART_CONFIGS.get(stat_name)
