from django.urls import path
from .views import (CategoriaController,
                    OrdenCompraController,
                    ProductoController,
                    ProductosController,
                    RegistroClienteController,
                    SubirImagenController)
from .views import  BusquedaCliente, CategoriaController, ClientesController, CustomPayloadController, DetallesController, FiltrosDetalleController, FiltrosOrdenesController, FiltrosProductosController, OpcionesAdministrador, OrdenCompraController, OrdenxClienteController, PerfilUsuario, ProductoController, ProductosController, ProductoxCategoriaController, RegistroClienteController, SubirImagenController
# , LoginController, LogoutController
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Registro Cliente - Buscar todos los clientes. 
    path('registrar/', RegistroClienteController.as_view()),

    #Actualización parcial perfil usuario.
    path('clientes/', ClientesController.as_view()),
    path('act-perfil/<int:id>', ClientesController.as_view()),

    # Busqueda cliente x nombre ó doc
    path('buscar-cliente', BusquedaCliente.as_view()),
    
    # Opciones de admin [GET, POST, PUT, DELETE]
    path('cliente/<int:id>', OpcionesAdministrador.as_view()),
  
    # CRUD categorias [GET, POST, PUT, DELETE]

    path('categorias/', CategoriaController.as_view()),
    path('categoria/<int:id>', CategoriaController.as_view()),

    # CRUD productos [GET, POST, PUT, DELETE]
    path('productos/', ProductosController.as_view()),
    path('producto/<int:id>', ProductoController.as_view()),
    
    #Subir imagen cloudinary [POST, DELETE]
    path('subir-imagen/',SubirImagenController.as_view()),
   
    # Ordenes [POST, GET]
    path('orden/', OrdenCompraController.as_view()),
    path('orden/<int:id>', DetallesController.as_view()),

    # Busquedas-filtros
    path('filtros', FiltrosProductosController.as_view()),
    path('forden', FiltrosOrdenesController.as_view()),
    path('fdetalle', FiltrosDetalleController.as_view()),
    path('prodCat', ProductoxCategoriaController.as_view()),
    path('ordenCli', OrdenxClienteController.as_view()),


    # path('login/', LoginController.as_view()),
    # path('logout/', LogoutController.as_view()),
    
    # path('login/', TokenObtainPairView.as_view()),
    # path('refresh-session', TokenRefreshView.as_view()),

    path('login-custom', CustomPayloadController.as_view()),
    path('refresh-token', TokenRefreshView.as_view()),
    path('verify-token', TokenVerifyView.as_view()),
    path('me', PerfilUsuario.as_view()),
    
]