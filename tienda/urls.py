from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('handmade/', include('handmade.urls')),
    path('facturacion/', include('facturacion.urls')),

]