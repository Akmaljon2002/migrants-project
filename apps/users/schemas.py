from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.users import serializers as slr
from apps.users.choices import UserRoleChoice
from utils.exceptions import resp

login_scm = extend_schema(
    tags=["Users"],
    summary="Login",
    request=slr.LoginSerializer(),
    responses=resp(200, slr.LoginResponseSerializer())
)

logout_scm = extend_schema(
    tags=["Users"],
    summary="Login",
    request=slr.LogoutSerializer(),
    responses=resp(204)
)

create_user_scm = extend_schema(
    tags=["Users"],
    summary="Create User",
    description="Allows admin to create a new user by providing phone, full name, role, and password.",
    request=slr.CustomUserCreateSerializer(),
    responses=resp(201, slr.CustomUserSerializer())
)

list_users_scm = extend_schema(
    tags=["Users"],
    summary="List Users",
    description="Returns a list of all registered users.",
    responses=resp(200, slr.CustomUserSerializer()),
    parameters=[
    OpenApiParameter(
            name="role",
            description="Filter by user role",
            required=False,
            type=str,
            enum=[choice.value for choice in UserRoleChoice]
        ),
        OpenApiParameter(
            name="date",
            description="Filter by user created at",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="search",
            description="Search by full_name and phone",
            required=False,
            type=str
        ),
        # Pagination parameters
        OpenApiParameter(
            name="page",
            description="Page number for pagination",
            required=False,
            type=int
        ),
        OpenApiParameter(
            name="limit",
            description="Number of results per page",
            required=False,
            type=int
        ),
    ]
)

get_user_schema = extend_schema(
    tags=["Users"],
    summary='User',
    request=None,
    responses=resp(200, slr.CustomUserSerializer)
)

get_current_user_schema = extend_schema(
    tags=["Users"],
    summary='Current User',
    request=None,
    responses=resp(200, slr.CustomUserSerializer)
)

update_user_schema = extend_schema(
    tags=["Users"],
    summary='Update User',
    request=slr.CustomUserUpdateSerializer(),
    responses=resp(200)
)

delete_user_schema = extend_schema(
    tags=["Users"],
    summary='Delete User',
    request=None,
    responses=resp(204)
)