from rest_framework import serializers
from handmade.models import OrdenCompraModel
from .models import ComprobanteModel

class ComprobanteSerializer(serializers.Serializer):
    ordenId = serializers.IntegerField()
    tipoComprobante = serializers.ChoiceField(choices=['BOLETA', 'FACTURA'])
    numeroDocumento = serializers.CharField(min_length=8, max_length=11)

    def validate(self, data):
        try:
            data['ordenId'] = OrdenCompraModel.objects.filter(
                ordenId=data.get('ordenId')).first()
            if data.get('ordenId') is None:
                raise Exception()

            return data
        except:
            raise serializers.ValidationError(detail='Error en el pedido')


class ComprobanteModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ComprobanteModel