from django.http import request
from django.utils.encoding import force_text
from rest_framework.test import APITestCase
from .models import CategoriaModel, ProductoModel,ClienteModel,OrdenCompraModel, OrdenDetalleModel


class ClientesTestCase(APITestCase):
    def setUp(self):
        ClienteModel(
            clienteNombre='Marigrace Silva',
            clienteTipoDoc=1,
            clienteNroDoc=87854963,
            clienteDireccion="cayma",
            clienteTipo=2,
            clienteEstado=True,
            clienteCorreo="mkss611297@gmail.com",
            password="Weelcome1!").save()
        ClienteModel(
            clienteNombre='Kim',
            clienteTipoDoc=1,
            clienteNroDoc=987459633,
            clienteDireccion="cayma",
            clienteTipo=2,
            clienteEstado=True,
            clienteCorreo="mkss11297@gmail.com",
            password="Weelcome1!").save()
    
    def  test_post_fail(self):
        request = self.client.post('/handmade/registrar/')
        message = request.data.get('message')

        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al crear el cliente')

    def test_post_sucess(self):
        request = self.client.post('/handmade/registrar/', data={
            "clienteNombre":"Kim",
            "clienteTipoDoc":1,
            "clienteNroDoc":987959633,
            "clienteDireccion":"cayma",
            "clienteTipo":2,
            "clienteEstado":True,
            "clienteCorreo":"mkss711297@gmail.com",
            "password":"Weelcome1!"
        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('clienteId')
        clienteEncontrado = ClienteModel.objects.filter(clienteId = id).first()

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, 'Cliente creado con exito')
        self.assertIsNone(clienteEncontrado)
    
    def test_post_client_exists_fail(self):
        nuevoCliente = {
            "clienteNombre":"Kimberly",
            "clienteTipoDoc":1,
            "clienteNroDoc":988889633,
            "clienteDireccion":"cayma",
            "clienteTipo":2,
            "clienteEstado":True,
            "clienteCorreo":"mksssss711297@gmail.com",
            "password":"Weelcome1!"
        }
        self.client.post('/handmade/registrar/', data=nuevoCliente, format='json')
        request = self.client.post('/handmade/registrar/', data=nuevoCliente, format='json')
        self.assertEqual(request.status_code,400)

class CategoriaTestCase(APITestCase):
    def setUp(self):
        CategoriaModel(
            categoriaNombre='Categoria 1',
            categoriaEstado=True).save()
        CategoriaModel(
            categoriaNombre='Categoria 2',
            categoriaEstado=False).save()
    
    def  test_post_cat_fail(self):
        request = self.client.post('/handmade/categorias/')
        message = request.data.get('message')

        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al registrar la categoria')

    def test_post_cat_sucess(self):
        nuevaCategoria = {
           "categoriaNombre":"Categoria 1",
           "categoriaEstado":True
        }
        request = self.client.post('/handmade/categorias/', data=nuevaCategoria, format='json')
        self.assertEqual(request.data.get('content').get('categoriaId'),
                            nuevaCategoria.get('categoriaId'))
    
    def test_post_categoria_exists_fail(self):
        nuevaCategoria = {
           "categoriaNombre":"Categoria 1",
           "categoriaEstado":True
        }
        self.client.post('/handmade/categorias/', data=nuevaCategoria, format='json')
        request = self.client.post('/handmade/categorias/', data=nuevaCategoria, format='json')
        self.assertEqual(request.status_code,400)



