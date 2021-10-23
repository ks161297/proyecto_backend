from django.urls import path, include,url
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(API, renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
urlpatterns = [
    path('handmade/', include('handmade.urls')),
    path('facturacion/', include('facturacion.urls')),
    url(r'^docs/', schema_view, name="docs")

]