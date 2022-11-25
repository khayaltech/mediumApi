from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title=_("My Medium Api"),
        default_version="v1",
        description="API endpoints for the Medium API Clone",
        contact=openapi.Contact(email="khayalfarajov@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


admin.site.site_header = "Medium Api Admin"
admin.site.site_title = "Medium Api Admin Portal"
admin.site.index_title = "Welcome to the Medium Api Portal"
