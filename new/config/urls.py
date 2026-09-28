from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from drf_spectacular.views import SpectacularSwaggerView
from starter.api.views import DynamicSpectacularAPIView, ScalarAPIView

urlpatterns = [
    path("", include("starter.urls")),
    path("admin/", admin.site.urls),
    # User management
    path("users/", include("makalek.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Django Browser Reload
    path("__reload__/", include("django_browser_reload.urls")),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# API URLS
urlpatterns += [
    # API base url
    path(f"api/{settings.API_VERSION}/", include("config.api_router")),
    # DRF auth token
    path(
        "api/schema/",
        DynamicSpectacularAPIView.as_view(permission_classes=[], throttle_classes=[]),
        name="api-schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/docs/scalar/", ScalarAPIView.as_view(), name="scalar"),
    path(f"api/{settings.API_VERSION}/auth/", include("bunifu_django_auth.urls")),
]
if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        *staticfiles_urlpatterns(),
    ]
