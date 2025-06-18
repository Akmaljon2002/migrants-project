def get_chart_config(stat_name: str):
    configs = {
        "migrants_by_country": {
            "query": """
                SELECT driection_country_id, COUNT(*) as count
                FROM border_cross_data
                WHERE direction_type_code = 'OUT'
                GROUP BY driection_country_id
                ORDER BY count DESC
            """,
            "label": "driection_country_id",
            "value": "count",
            "title": "Migrants by Country",
        },
        "migrants_by_region": {
            "query": """
                SELECT region_id, COUNT(*) as count
                FROM migrant_data
                GROUP BY region_id
                ORDER BY count DESC
            """,
            "label": "region_id",
            "value": "count",
            "title": "Migrants by Region",
        },
        "migration_purpose": {
            "query": """
                SELECT trip_purpose_id, COUNT(*) as count
                FROM border_cross_data
                GROUP BY trip_purpose_id
                ORDER BY count DESC
            """,
            "label": "trip_purpose_id",
            "value": "count",
            "title": "Migration Purpose",
        },
        "transport_type": {
            "query": """
                SELECT transport_type_code_id, COUNT(*) as count
                FROM border_cross_data
                GROUP BY transport_type_code_id
                ORDER BY count DESC
            """,
            "label": "transport_type_code_id",
            "value": "count",
            "title": "Transport Type",
        },
    }
    return configs.get(stat_name)