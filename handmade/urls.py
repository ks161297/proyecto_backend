from django.urls import path

from .views import CategoriaController, OrdenCompraController, ProductoController, ProductosController, RegistroClienteController, SubirImagenController

urlpatterns = [
    path('registrar/', RegistroClienteController.as_view()),
    path('buscar-cliente/<int:id>', RegistroClienteController.as_view()),
    path('categorias/', CategoriaController.as_view()),
    path('categoria/<int:id>', CategoriaController.as_view()),
    path('productos/', ProductosController.as_view()),
    path('subir-imagen/',SubirImagenController.as_view()),
    path('producto/<int:id>', ProductoController.as_view()),
    path('orden/', OrdenCompraController.as_view())
]