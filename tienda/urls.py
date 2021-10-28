from django.urls import path, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('handmade/', include('handmade.urls')),
    path('facturacion/', include('facturacion.urls')),

]