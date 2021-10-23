from rest_framework.test import APITestCase

from handmade.models import PedidoModel
from facturacion.models import ComprobanteModel

class TestComprobante(APITestCase):

    @classmethod
    def setUp(self):
        ComprobanteModel(comprobanteSerie='BBB1',comprobanteNumero = '1',comprobanteTipo='B', pedidoId= 1).save()
        ComprobanteModel(comprobanteSerie='FFF1',comprobanteNumero = '2',comprobanteTipo='F', pedidoId= 1).save()
    def test_post_fail(self):
        request = self.client.post('/facturacion/generar-comprobante')
        message = request.data.get('message')

        self.assertEqual(request.status_code,400)
        self.assertEqual(message, 'Error al guardar comprobante')

    def test_post_success(self):
        request = self.client.post('/facturacion/generar-comprobante', data={
            "comprobanteSerie": "FFF1",
            "comprobanteNumero": '4',
            "comprobanteTipo":'B'

        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('comprobanteId')

        comprobanteEncontrado = ComprobanteModel.objects.filter(comprobanteId=id).first()

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, 'Comprobante creado exitosamente')
        self.assertIsNotNone(comprobanteEncontrado)
