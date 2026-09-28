from django.views.generic import TemplateView
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.views import SpectacularAPIView


class ScalarAPIView(TemplateView):
    template_name = "apis/scalar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema_url"] = "/api/schema/"
        context["title"] = "SACCO Platform API"
        return context


class DynamicSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, *, public=False):
        schema = super().get_schema(request=request, public=public)

        if request:
            schema["servers"] = [
                {
                    "url": f"{request.scheme}://{request.get_host()}",
                    "description": "Current environment",
                },
            ]

        return schema


class DynamicSpectacularAPIView(SpectacularAPIView):
    generator_class = DynamicSchemaGenerator
