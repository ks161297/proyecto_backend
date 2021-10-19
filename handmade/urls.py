from django.urls import path
from .views import  BusquedaCliente, CategoriaController, DetallesController, FiltrosDetalleController, FiltrosOrdenesController, FiltrosProductosController, OpcionesAdministrador, OrdenCompraController, OrdenxClienteController, ProductoController, ProductosController, ProductoxCategoriaController, RegistroClienteController, SubirImagenController

urlpatterns = [
    # Registro Cliente
    path('registrar/', RegistroClienteController.as_view()),
    
    # Buscador cliente x doc 
    path('buscar-cliente/<int:id>', RegistroClienteController.as_view()),
    
    # Opciones de admin
    path('cliente/<int:id>', OpcionesAdministrador.as_view()),
     # Listar Prod
    path('listar/', OpcionesAdministrador.as_view()),




    path('categorias/', CategoriaController.as_view()),
    path('categoria/<int:id>', CategoriaController.as_view()),
    path('productos/', ProductosController.as_view()),
    path('subir-imagen/',SubirImagenController.as_view()),
    path('producto/<int:id>', ProductoController.as_view()),
    path('orden/', OrdenCompraController.as_view()),

    path('orden/<int:id>', DetallesController.as_view()),

    path('filtros', FiltrosProductosController.as_view()),

    path('forden', FiltrosOrdenesController.as_view()),
    path('fdetalle', FiltrosDetalleController.as_view()),

    path('prodCat', ProductoxCategoriaController.as_view()),

    path('ordenCli', OrdenxClienteController.as_view()),

    path('buscarCli', BusquedaCliente.as_view()),
    

   

   
]