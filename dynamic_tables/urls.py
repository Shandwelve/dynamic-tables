from typing import Any

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_nested import routers

from tables.views import DynamicTablesViewSet, DynamicTableRowsViewSet

schema_view: Any = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()
router.register(r"tables", DynamicTablesViewSet, basename="tables")

table_rows_router = routers.NestedSimpleRouter(router, r"tables", lookup="table")
table_rows_router.register(r"rows", DynamicTableRowsViewSet, basename="table_rows")

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path(r"", include(router.urls)),
    path(r"", include(table_rows_router.urls)),
]
