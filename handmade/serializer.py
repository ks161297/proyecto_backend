
from rest_framework import serializers
from .models import CategoriaModel, ClienteModel, OrdenCompraModel, OrdenDetalleModel, ProductoModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        exclude = ['groups','user_permissions','last_login','is_active','is_staff']
        extra_kwargs = {
            'password':{
                'write_only':True
            },
           'is_active':{
                'write_only': True,    
            },
            'groups':{
                'write_only': True,    
            },
            'user_permissions':{
                'write_only': True,    
            },
            'is_staff':{
                'write_only': True,    
            },
            'clienteTipo':{
                'write_only': True,    
            }
        }

class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteModel
        fields = '__all__'
        extra_kwargs = {
            'clientePassword':{
                'write_only':True
            }
        }

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CategoriaModel
        fields = '__all__'
        lookup_field = 'categoriaId'

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        fields = '__all__'
        
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoModel
        #fields = '__all__'
        exclude = ['categoria']
        lookup_field = 'productoId'

class DetalleOrdenSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(required=True)
    producto_id = serializers.IntegerField(required=True)

class OrdenCompraSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(min_value=0, required=True)
    detalle = DetalleOrdenSerializer(many=True)

class DetallesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDetalleModel
        exclude = ['ordenCompra']
        depth = 1

class OperacionOrdenSerializer(serializers.ModelSerializer):
    detallePedido = DetallesModelSerializer(many=True)
    class Meta:
        model = OrdenCompraModel
        fields = '__all__'
        depth = 1

class OrdenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenCompraModel
        fields = '__all__'

class CustomPayloadSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user: ClienteModel):
        token = super(CustomPayloadSerializer, cls).get_token(user)
        # print(token)
        token['user_mail'] = user.clienteCorreo
        token['mensaje'] = 'Custom'
        return token