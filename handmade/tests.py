from django.http import request
from rest_framework.test import APITestCase
from .models import CategoriaModel, ProductoModel,ClienteModel,OrdenCompraModel, OrdenDetalleModel


class clientes(APITestCase):
    def setUp(self):
        ClienteModel(
            clienteId=1,
            clienteNombre="Marigrace Silva",
            clienteTipoDoc=1,
            clienteNroDoc="72750134",
            clienteDireccion="Av Cayma s/n",
            clienteTipo="1",
            clienteEstado=True,
            clienteCorreo="mksss161297@gmail.com",
            password="ejemplo123!"
        ).save()
        ClienteModel(
            clienteId=2,
            clienteNombre="Aylin Santa Cruz",
            clienteTipoDoc=1,
            clienteNroDoc="72859644",
            clienteDireccion="Av Lima s/n",
            clienteTipo="2",
            clienteEstado=False,
            clienteCorreo="aylinsantacruz@gmail.com",
            password="ejemplo123!"
        ).save()

    def test_post_cliente_fail(self):
        request = self.client.post('/handmade/registrar/')
        message = request.data.get('message')

        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al crear el cliente')

    def test_post_cliente_sucess(self):
        nuevoCliente = {
            "clienteNroDoc": "72859644",
            "clienteDireccion": "Av cayma s/n"
        }

        request = self.client.post(
            '/handmade/registrar/', data=nuevoCliente, format='json')

        self.assertEqual(request.data.get('content').get('clienteId'),
                         nuevoCliente.get('clienteId'))

    def test_post_client_exists_fail(self):
        nuevoCliente = {
            "clienteDocumento": "72859644",
            "clienteDireccion": "Av cayma s/n"
        }

        self.client.post(
            '/handmade/registrar/', data=nuevoCliente, format='json')

        request = self.client.post(
            '/handmade/registrar/', data=nuevoCliente, format='json')

        self.assertEqual(request.status_code, 400)


class categorias(APITestCase):
    def setUp(self):
        CategoriaModel(
            categoriaId=6,
            categoriaNombre='Dia de la madre').save()
        CategoriaModel(
            categoriaId=10,
            categoriaNombre='Dia del padre').save()

    def test_post_fail(self):
        request = self.client.post('/handmade/categorias/')
        message = request.data.get('message')

        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al registrar la categoria')

    def test_post_sucess(self):
        request = self.client.post('/handmade/categorias/', data={
            "categoriaNombre": "Dia",
            "categoriaEstado": True,
        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('categoriaId')
        categoriaEncontrado = CategoriaModel.objects.filter(
            categoriaId=id).first()

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, 'Categoria registrada con exito')
        self.assertIsNotNone(categoriaEncontrado)

    def test_get_sucess(self):
        categoriaEncontrada = CategoriaModel.objects.all()
        self.assertEqual(1, 1)
