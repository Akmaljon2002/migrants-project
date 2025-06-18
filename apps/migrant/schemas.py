from drf_spectacular.utils import extend_schema_view, extend_schema

migrant_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Migrants"],
        operation_id="List All Migrants",
        description="Retrieve all migrants with pagination.",
        responses={200: "List of migrants."},
    ),
    retrieve=extend_schema(
        tags=["Migrants"],
        operation_id="Retrieve Single Migrant",
        description="Retrieve a single migrant by their ID.",
        responses={200: "Details of a migrant."},
    ),
    create=extend_schema(
        tags=["Migrants"],
        operation_id="Create Migrant",
        description="Create a new migrant entry.",
        responses={201: "Migrant created successfully."},
    ),
    update=extend_schema(
        tags=["Migrants"],
        operation_id="Update Migrant",
        description="Update an existing migrant entry by their ID.",
        responses={
            200: "Migrant updated successfully.",
            404: "Migrant not found.",
            400: "Bad request."
        }
    ),
    destroy=extend_schema(
        tags=["Migrants"],
        operation_id="Delete Migrant",
        description="Delete a migrant entry by their ID.",
        responses={
            204: "Migrant deleted successfully.",
            404: "Migrant not found."
        }
    ),
    partial_update=extend_schema(
        tags=["Migrants"],
        operation_id="Partially Update Migrant",
        description="Partially update a migrant entry by their ID.",
        responses={
            200: "Migrant partially updated successfully.",
            404: "Migrant not found.",
            400: "Bad request."
        }
    )
)