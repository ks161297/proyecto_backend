from os import remove
import cloudinary
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CategoriaSerializer, OrdenCompraSerializer, ProductosSerializer, RegistroClienteSerializer
from .models import CategoriaModel, ClienteModel, OrdenCompraModel, OrdenDetalleModel, ProductoModel
import cloudinary.uploader
from rest_framework import serializers, status
from django.conf import settings
from django.db import transaction


class RegistroClienteController(ListCreateAPIView):
    serializer_class = RegistroClienteSerializer
    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Cliente creado con exito',
                'content':data.data
            })
        else:
            return Response(data={
                'message':'Error al crear el cliente',
                'content':data.errors
            })


    queryset = ClienteModel.objects.all()
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
class CategoriaController(ListCreateAPIView):
    queryset = CategoriaModel.objects.all()
    serializer_class = CategoriaSerializer
    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Categoria registrada con exito',
                'content': data.data
            })
        else:
            return Response(data={
                'message':'Error al registrar la categoria',
                'content': data.errors 
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
    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
            'message':'Las categorias que existen son:',
            'content': data.data
        })
class ProductosController(RetrieveUpdateDestroyAPIView):
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
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        return Response(data={
            'message':'Los productos que existen son:',
            'content':data.data
        })

class SubirImagenController(APIView):
    def post(self, request):
        file = request.data.get('picture')
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
        productoEncontrado = self.get_queryset().filter(productoId=id).first()
        if not productoEncontrado:
            return Response(data={
                'message':'Producto no encontrado',
                'content':None
            })
        try:
            data = productoEncontrado.delete()
            remove(settings.DEFAULT_FILE_STORAGE/str(productoEncontrado.productoImagen))
        except Exception as e:
            print(e)
        
        return Response(data={
            'message':'Producto eliminado con exito',
            'content':data
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
                    cliente = ClienteModel.objects.filter(clienteId=cliente_id).first()

                    if not cliente:
                        raise Exception('Cliente Incorrecto')
                    orden = OrdenCompraModel(pedidoTotal = 0, cliente = cliente)
                    orden.save()
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
                        detalleOrden = OrdenDetalleModel(ordenDetalleCantidad=cantidad,ordenDetallePrecioUnitario=producto.productoPrecio, ordenDetallePrecioTotal=producto.productoPrecio*cantidad, producto=producto, detalleOrden=detalleOrden)
                        detalleOrden.save()
                        orden.save()
                return Response(data={
                    'message':'Orden exitosa'
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


    def get(self, request:Request):
        pass 