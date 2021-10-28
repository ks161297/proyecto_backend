from django.db.models.query import QuerySet
import cloudinary
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import CorreoPermission
from .serializer import CategoriaSerializer, CustomPayloadSerializer, OperacionOrdenSerializer, OrdenCompraSerializer, OrdenesSerializer, ProductoSerializer, ProductosSerializer, RegistroClienteSerializer, clienteSerializer
from .models import CategoriaModel, ClienteModel, OrdenCompraModel, OrdenDetalleModel, ProductoModel
import cloudinary.uploader
from rest_framework import status
from django.conf import settings
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class RegistroClienteController(CreateAPIView):
    serializer_class = RegistroClienteSerializer
    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Cliente creado con exito',
                'content':data.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al crear el cliente',
                'content':data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ClientesController(RetrieveAPIView):
    serializer_class = clienteSerializer
    queryset = ClienteModel.objects.all()
    def get(self, request:Request):
        registros =ClienteModel.objects.filter(clienteEstado=True).values()
        return Response(data={
            'message':'Los clientes activos son:',
            'content': registros
        })

    
class BusquedaCliente(RetrieveAPIView):
    queryset = ClienteModel.objects.all()
    serializer_class =clienteSerializer

    def get(self, request:Request):
        nombre = request.query_params.get('nombre')
        nro_doc = request.query_params.get('nro_doc')
        clienteEncontrado = None
        if nro_doc:
            clienteEncontrado: QuerySet = ClienteModel.objects.filter(clienteNroDoc=nro_doc)
        if nombre:
            if clienteEncontrado is not None:
                clienteEncontrado = clienteEncontrado.filter(clienteNombre__icontains=nombre).all()
            else:
                clienteEncontrado = ClienteModel.objects.filter(clienteNombre__icontains=nombre).all()
        data = self.serializer_class(instance=clienteEncontrado, many=True)

        return Response(data={
            'message': 'Usuario:',
            'content':data.data
        })

class CustomPayloadController(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomPayloadSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            print(data.validated_data)
            return Response(data={
                "success": True,
                "content": data.validated_data,
                "message": "Login exitoso"
            })

        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "error de generacion de la jwt"
            })


class PerfilUsuario(RetrieveAPIView):

    permission_classes = [IsAuthenticated, CorreoPermission]

    def get(self, request: Request):
        
        print(request.user)
        print(request.auth) 
        return Response(data={
            'message': 'El usuario es',
            'content': request.user.clienteCorreo
        })


class OpcionesAdministrador(RetrieveUpdateDestroyAPIView):
    serializer_class = clienteSerializer
    queryset = ClienteModel.objects.all()
    #Filtrar x id
    def get(self, request:Request, id):
        clienteEncontrado = self.get_queryset().filter(clienteId=id).first()
        if not clienteEncontrado:
            return Response(data={
                'message':'El cliente no existe'
            })
        data = self.serializer_class(instance=clienteEncontrado)
        return Response(data={
            'message':'El cliente buscado es:',
            'content':data.data
        })
    
    def put(self, request:Request, id):
        clienteEncontrado = ClienteModel.objects.filter(clienteId=id).first()
        if clienteEncontrado is None:
            return Response(data={
                'message':'Cliente no existe',
                'content':None
            })
        serializador = RegistroClienteSerializer(data=request.data)
        if serializador.is_valid():
            serializador.update(instance=clienteEncontrado, validated_data=serializador.validated_data)
            return Response(data={
                'message':'Cliente actualizado con exito',
                'content':serializador.data
            })
        else:
            return Response(data={
                'message':'Error al actualizar el cliente',
                'content':serializador.errors
            })
    
    def patch(self, request:Request, id):
        clienteEncontrado = ClienteModel.objects.filter(clienteId=id).first()
        if clienteEncontrado is None:
            return Response(data={
                'message':"Cliente no existe",
                'content': None
            }, status=status.HTTP_404_NOT_FOUND)
        serializador = clienteSerializer(clienteEncontrado, data=request.data, partial=True)
        if serializador.is_valid():
            serializador.save()
            return Response(data={
                'message':'Actualizado con exito',
                'content': serializador.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al actualizar el registro',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    #Actualizar
 

    
    #Eliminar
    def delete(self, request:Request, id):
        clienteEncontrado = ClienteModel.objects.filter(clienteId = id).first()
        if clienteEncontrado is None:
            return Response(data={
                'message':'Cliente no existe',
                'content':None
            })
        clienteEncontrado.clienteEstado = False
        clienteEncontrado.save()
        serializador = RegistroClienteSerializer(instance=clienteEncontrado)
        return Response(data={
            'message':"Cliente eliminado con exito",
            'content': serializador.data
        })

class CategoriasController(ListCreateAPIView):
    queryset = CategoriaModel.objects.all()
    serializer_class = CategoriaSerializer
    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Categoria registrada con exito',
                'content': data.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al registrar la categoria',
                'content': data.errors 
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
            'message':'Las categorias que existen son:',
            'content': data.data
        })
    
class CategoriaController(RetrieveUpdateDestroyAPIView):
    queryset = CategoriaModel.objects.all()
    serializer_class = CategoriaSerializer

    def get(self, request:Request, id):
        categoriaEncontrada = self.get_queryset().filter(categoriaId = id).first()
        if not categoriaEncontrada:
            return Response(data={
                'message':'El producto no existe'
            })
        data = self.serializer_class(instance=categoriaEncontrada)
        return Response(data={
            'message':'La categoria buscada es:',
            'content':data.data
        })

    def put(self, request:Request, id):
        categoriaEncontrada = CategoriaModel.objects.filter(categoriaId = id).first()
        if categoriaEncontrada is None:
            return Response(data={
                'message':'Esta categoria no existe',
                'content':None
            })
        serializador = CategoriaSerializer(data=request.data)
        if serializador.is_valid():
            serializador.update(instance=categoriaEncontrada, validated_data=serializador.validated_data)
            return Response(data={
                'message':'La categoría fue actualizada con exito',
                'content':serializador.data
            })
        else:
            return Response(data={
                'message':'Error al actualizar la categoria',
                'content':serializador.errors
            })
    def delete(self, request:Request, id):
        categoriaEncontrada = CategoriaModel.objects.filter(categoriaId = id).first()
        if categoriaEncontrada is None: 
            return Response(data={
                'message':'Categoría no encontrada',
                'content':None
            })
        categoriaEncontrada.categoriaEstado = False
        categoriaEncontrada.save()
        serializador = CategoriaSerializer(instance=categoriaEncontrada)
        return Response(data={
            'message':'Categoría eliminada con exito',
            'content': serializador.data
        })
    

class ProductosController(ListCreateAPIView):
    serializer_class = ProductosSerializer
    queryset = ProductoModel.objects.all()

    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Producto creado con exito',
                'content':data.data
            })
        else:
            return Response(data={
                'message':'Error al crear el producto',
                'content': data.errors
            })

    def get(self, request:Request):
        data = ProductoModel.objects.filter(productoEstado=True).values()
        return Response(data={
            'message':'Los productos activos que existen son:',
            'content':data
        })

class SubirImagenController(APIView):

    def post(self, request):
        file = request.data.get('imagen')
        upload_data = cloudinary.uploader.upload(file)
        return Response ({
            'message':'Imagen subida con exito',
            'data': upload_data
        })

class ProductoController(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductosSerializer
    queryset = ProductoModel.objects.all()    

    def get(self, request:Request, id):
        productoEncontrado = self.get_queryset().filter(productoId = id).first()
        if not productoEncontrado:
            return Response(data={
                'message':'El producto no existe'
            })
        data = self.serializer_class(instance=productoEncontrado)
        return Response(data={
            'message':'El producto buscado es:',
            'content':data.data
        })
    
    def patch(self, request:Request, id):
        productoEncontrado = ProductoModel.objects.filter(productoId=id).first()
        if productoEncontrado is None:
            return Response(data={
                'message': 'El producto no existe',
                'content':None
            })
        serializador = ProductosSerializer(productoEncontrado, data=request.data, partial=True)
        if serializador.is_valid():
            serializador.save()
            return Response(data={
                'message':'El producto se actualizó con exito',
                'content': serializador.data
            })

    def put(self, request:Request, id):
        productoEncontrado = ProductoModel.objects.filter(productoId=id).first()
        if productoEncontrado is None:
            return Response(data={
                'message':'Producto no existe',
                'content':None
            })
        serializador = ProductosSerializer(data=request.data)
        if serializador.is_valid():
            serializador.update(instance=productoEncontrado, validated_data=serializador.validated_data)
            return Response(data={
                'message':'Producto actualizado con exito',
                'content':serializador.data
            })
        else:
            return Response(data={
                'message':'Error al actualizar el producto',
                'content':serializador.errors
            })

    def delete(self, request:Request, id):
        productoEncontrado = ProductoModel.objects.filter(productoId=id).first()
        if productoEncontrado is None:
            return Response(data={
                'message':'Producto no existe',
                'content':None
            })
        productoEncontrado.productoEstado = False
        productoEncontrado.save()
        serializador = ProductosSerializer(instance=productoEncontrado)
        return Response(data={
            'message':'Producto eliminado con exito',
            'content': serializador.data
        })

class OrdenCompraController(CreateAPIView):
    serializer_class = OrdenCompraSerializer
    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            cliente_id = data.validated_data.get('cliente_id')
            detalles = data.validated_data.get('detalle')

            try:
                with transaction.atomic():
                    clienteE = ClienteModel.objects.filter(clienteId=cliente_id).first()

                    if not clienteE:
                        raise Exception('Cliente Incorrecto')
                    pedido = OrdenCompraModel(ordenTotal = 0, cliente = clienteE)
                    pedido.save()
                    for detalle in detalles:
                        producto_id = detalle.get('producto_id')
                        cantidad = detalle.get('cantidad')
                        producto = ProductoModel.objects.filter(productoId = producto_id).first()
                    
                        if not producto:
                            raise Exception('Producto{} no existe'.format(producto_id))
                        
                        if cantidad > producto.productoCantidad:
                            raise Exception('No hay suficiente cantidad para el producto {}'.format(producto.productoNombre))
                        producto.productoCantidad = producto.productoCantidad - cantidad
                        producto.save()
                        detalleOrden = OrdenDetalleModel(ordenDetalleCantidad=cantidad,ordenDetalleSubTotal=producto.productoPrecio*cantidad, producto=producto, ordenCompra=pedido)
                        detalleOrden.save()
                        pedido.ordenTotal += detalleOrden.ordenDetalleSubTotal
                        pedido.save()
                return Response(data={
                    'message':'Orden exitosa',
                    'content': data.data
                })
            except Exception as e:
                return Response(data={
                    'message':e.args
                })
        else:
            return Response(data={
                'message':'Error al agregar la venta',
                'content':data.errors
            })

class DetallesController(RetrieveAPIView):
    serializer_class = OperacionOrdenSerializer
    def get(self, request: Request, id):
        #orden = OrdenCompraModel.objects.get(ordenId = id)
        orden = get_object_or_404(OrdenCompraModel, pk=id)
        serializador = self.serializer_class(instance=orden)
        return Response(data={
            'message':'La orden es:',
            'content':serializador.data
        })

class FiltrosProductosController(RetrieveAPIView):
    serializer_class = ProductosSerializer
    def get(self, request:Request):
        id = request.query_params.get('id')
        nombre = request.query_params.get('nombre')
        precio = request.query_params.get('precio')
        created_at = request.query_params.get('created_at')
        
        productoEncontrado = None

        if id:
            productoEncontrado: QuerySet = ProductoModel.objects.filter(productoId=id)
        if nombre:
            if productoEncontrado is not None:
                productoEncontrado = productoEncontrado.filter(productoNombre__icontains=nombre).all()
            else:
                productoEncontrado = ProductoModel.objects.filter(productoNombre__icontains=nombre).all()
        if precio:
            if productoEncontrado is not None:
                productoEncontrado = productoEncontrado.filter(productoPrecio__icontains=precio).alL()
            else:
                productoEncontrado = ProductoModel.objects.filter(productoPrecio__icontains=precio).all()
        if created_at:
            if productoEncontrado is not None:
                productoEncontrado = productoEncontrado.filter(created_At__icontains=created_at).alL()
            else:
                productoEncontrado = ProductoModel.objects.filter(created_At__icontains=created_at).all()
   
        
        data = self.serializer_class(instance=productoEncontrado, many=True)
    
        return Response(data={
            'message':'Productos:',
            'content':data.data
        })

class ProductoxCategoriaController(RetrieveAPIView):
    serializer_class = ProductoSerializer
    def get(self,request:Request):
        productosEncontrados=None

        categoria_id = request.query_params.get('categoria_id')
        if categoria_id:
            if productosEncontrados is not None:
                productosEncontrados = productosEncontrados.objects.select_related().filter(categoria_id=categoria_id).values('productoNombre', 'productoDescripcion','productoImagen','productoPrecio','categoria').all()
            else:
                productosEncontrados = ProductoModel.objects.select_related().filter(categoria_id=categoria_id).values('productoNombre', 'productoDescripcion','productoImagen','productoPrecio','categoria').all()
        data = self.serializer_class(instance=productosEncontrados, many = True)


        return Response(data={
            'message':'Productos',
            'content':data.data
        })


class FiltrosOrdenesController(RetrieveAPIView):
    serializer_class = OperacionOrdenSerializer
    def get(self, request:Request):
        id=request.query_params.get('id')
        direccion=request.query_params.get('direccion')
        correo=request.query_params.get('correo')
        estado=request.query_params.get('estado')
        fecha =request.query_params.get('fecha')
        ordenEncontrada = None

        if id:
            ordenEncontrada: QuerySet = OrdenCompraModel.objects.filter(ordenId=id)
        if direccion:
            if ordenEncontrada is not None:
                ordenEncontrada = ordenEncontrada.filter(ordenDireccion__icontains=direccion).alL()
            else:
                ordenEncontrada = OrdenCompraModel.objects.filter(ordenDireccion__icontains=direccion).all()
        if correo:
            if ordenEncontrada is not None:
                ordenEncontrada = ordenEncontrada.filter(ordenCorreo__icontains=correo).alL()
            else:
                ordenEncontrada = OrdenCompraModel.objects.filter(ordenCorreo__icontains=correo).all()
        if estado:
            if ordenEncontrada is not None:
                ordenEncontrada = ordenEncontrada.filter(ordenEstado__icontains=estado).alL()
            else:
                ordenEncontrada = OrdenCompraModel.objects.filter(ordenEstado__icontains=estado).all()

        if fecha:
            if ordenEncontrada is not None:
                ordenEncontrada = ordenEncontrada.filter(ordenFecha__icontains=fecha).alL()
            else:
                ordenEncontrada = OrdenCompraModel.objects.filter(ordenFecha__icontains=fecha).all()
     
        
        data = self.serializer_class(instance=ordenEncontrada, many=True)
    
        return Response(data={
            'message':'Ordenes:',
            'content':data.data
        })

# class FiltrosDetalleController(RetrieveAPIView):

#     serializer_class = DetallesModelSerializer
#     def get(self, request:Request):
    
#         cantidad=request.query_params.get('cantidad')
#         precioTotal=request.query_params.get('precioTotal')
#         detalleEncontrado =None

#         if cantidad: 
#             if detalleEncontrado is not None:
#                 detalleEncontrado = detalleEncontrado.filter(ordenDetalleCantidad__icontains=cantidad).all()
#             else:
#                 detalleEncontrado = OrdenDetalleModel.objects.filter(ordenDetalleCantidad__icontains=cantidad).all()
#         if precioTotal: 
#             if detalleEncontrado is not None:
#                 detalleEncontrado = detalleEncontrado.filter(ordenDetallePrecioTotal__icontains=precioTotal).all()
#             else:
#                 detalleEncontrado = OrdenDetalleModel.objects.filter(ordenDetallePrecioTotal__icontains=precioTotal).all()
        
#         data = self.serializer_class(instance=detalleEncontrado, many=True)
    
#         return Response(data={
#             'message':'Ordenes:',
#             'content':data.data
#         })

class OrdenxClienteController(RetrieveAPIView):
    serializer_class = OperacionOrdenSerializer
    def get(self, request:Request):
        ordenesEncontradas = None
        cliente_id = request.query_params.get('cliente_id')
        

        if cliente_id:
            if ordenesEncontradas is not None:
                ordenesEncontradas = ordenesEncontradas.objects.select_related().filter(cliente_id=cliente_id)
            else:
                ordenesEncontradas = OrdenCompraModel.objects.select_related().filter(cliente_id=cliente_id)

       

        data = self.serializer_class(instance=ordenesEncontradas, many=True)
        return Response(data={
            'message':'Ordenes',
            'content':data.data
        })


