from django.urls import path, include
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="HANDMADE M&A",
      default_version='Vx',
      description="API HANDMADE",
      contact=openapi.Contact(email="mksss16129@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(''.schema_view.with_ui('swagger',cache_timeout=0)),
    path('admin/', admin.site.urls),
    path('handmade/', include('handmade.urls')),
    path('facturacion/', include('facturacion.urls')),

]