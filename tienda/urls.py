from django.urls import path, include
urlpatterns = [
    path('handmade/', include('handmade.urls')),
    path('facturacion/', include('facturacion.urls')),

]