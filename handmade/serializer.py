from django.db import models
from django.db.models import fields
from rest_framework import request, serializers
from .models import CategoriaModel, ClienteModel, OrdenCompraModel, OrdenDetalleModel, ProductoModel


class RegistroClienteSerializer(serializers.ModelSerializer):
    def save(self):
        clienteNombre = self.validated_data.get('clienteNombre')
        clienteTipoDoc = self.validated_data.get('clienteTipoDoc')
        clienteNroDoc = self.validated_data.get('clienteNroDoc')
        clienteDireccion = self.validated_data.get('clienteDireccion')
        clienteTipo = self.validated_data.get('clienteTipo')
        clienteCorreo = self.validated_data.get('clienteCorreo')
        password = self.validated_data.get('password')

        nuevoCliente = ClienteModel(clienteNombre=clienteNombre,clienteTipoDoc=clienteTipoDoc,clienteNroDoc=clienteNroDoc,clienteDireccion=clienteDireccion, clienteTipo=clienteTipo, clienteCorreo=clienteCorreo)

        nuevoCliente.set_password(password)
        nuevoCliente.save()
        return nuevoCliente
    
    class Meta:
        model = ClienteModel
        #fields = '__all__'
        exclude = ['groups','user_permissions','is_superuser','last_login','is_active','is_staff']
        extra_kwargs = {
            'clientePassword':{
                'write_only':True
            }
        }

class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteModel
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CategoriaModel
        fields = '__all__'

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        fields = '__all__'
        
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        #fields = '__all__'
        exclude = ['categoria']

class DetalleOrdenSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(required=True)
    producto_id = serializers.IntegerField(required=True)
    metodo_id = serializers.IntegerField(required=True)

class OrdenCompraSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(min_value=0, required=True)
    detalle = DetalleOrdenSerializer(many=True, required=True)

class DetallesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDetalleModel
        exclude = ['ordenCompra']
        depth = 1

class OperacionOrdenSerializer(serializers.ModelSerializer):
    detalle = DetallesModelSerializer(many=True)
    class Meta:
        model = OrdenCompraModel
        fields = '__all__'

class OrdenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenCompraModel
        fields = '__all__'