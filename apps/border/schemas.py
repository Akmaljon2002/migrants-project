from drf_spectacular.utils import extend_schema, extend_schema_view

border_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Border Crosses"],
        operation_id="List All Border Crosses",
        description="Retrieve all border crosses with pagination.",
        responses={200: "List of border crosses."},
    ),
    retrieve=extend_schema(
        tags=["Border Crosses"],
        operation_id="Retrieve Single Border Cross",
        description="Retrieve a single border cross by its ID.",
        responses={200: "Details of a border cross."},
    ),
    create=extend_schema(
        tags=["Border Crosses"],
        operation_id="Create Border Cross",
        description="Create a new border cross entry.",
        responses={201: "Border cross created successfully."},
    ),
    update=extend_schema(
        tags=["Border Crosses"],
        operation_id="Update Border Cross",
        description="Update an existing border cross entry by its ID.",
        responses={
            200: "Border cross updated successfully.",
            404: "Border cross not found.",
            400: "Bad request."
        }
    ),
    destroy=extend_schema(
        tags=["Border Crosses"],
        operation_id="Delete Border Cross",
        description="Delete a border cross entry by its ID.",
        responses={
            204: "Border cross deleted successfully.",
            404: "Border cross not found."
        }
    ),
    partial_update=extend_schema(
        tags=["Border Crosses"],
        operation_id="Partially Update Border Cross",
        description="Partially update a border cross entry by its ID.",
        responses={
            200: "Border cross partially updated successfully.",
            404: "Border cross not found.",
            400: "Bad request."
        }
    )
)