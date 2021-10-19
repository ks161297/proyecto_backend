
import requests
from rest_framework import request
from rest_framework.test import APITestCase
from .models import ClienteModel, ProductoModel

class ProductosTestCase(APITestCase):
    def setUp(self):
        ProductoModel(productoNombre='Producto 01',
                      productoPrecio=20.40).save()
        ProductoModel(productoNombre='Producto 02',
                      productoPrecio=20.40).save()
        ProductoModel(productoNombre='Producto 03',
                      productoPrecio=20.40).save()
        ProductoModel(productoNombre='Producto 04',
                      productoPrecio=20.40).save()

    def test_post_fail(self):

        print (self.shortDescription())
        request = self.client.post('/handmade/productos/')
        message = request.data.get('message')
        
        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al guardar el producto')
    
    def test_post_sucess(self):

        print(self.shortDescription())
        request = self.client.post('/handmade/productos/', data={
            "productoNombre":"Caja Trupan",
            "productoPrecio": 1.50
        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('productoId')
        print(id)
        productoEncontrado = ProductoModel.objects.filter(productoId = id).first()

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, 'Producto creado exitosamente')
        self.assertIsNotNone(productoEncontrado)

    def test_get_success(self):
   
        productoEncontrado = ProductoModel.objects.all()
        request = self.client.get('/handmade/productos/',data={'pagina': 1, 'cantidad': 2})
        print(request.data)
        paginacion = request.data.get('paginacion')
        content = request.data.get('data').get('content')
        self.assertIsNone(paginacion.get('paginaPrevia'))
        self.assertIsNotNone(paginacion.get('paginaContinua'))
        self.assertEqual(paginacion.get('porPagina'), 2)
        self.assertEqual(len(content), 2)
      

class ClienteTestCase(APITestCase):
    def setUp(self):
        ClienteModel(clienteNombre = 'SILVA SALAS MARIGRACE KIMBERLY STEFANIA', clienteDocumento='72750134', clienteDireccion='Mz M Lote 33 Cayma').save
    
    def test_post_cliente_fail(self):
       
        request = self.client.post('/handmade/clientes/')
        self.assertEqual(request.status_code, 400)

    def test_post_cliente_success(self):
        
        nuevoCliente = {
            "clienteDocumento":"72750134",
            "clienteDireccion":"Mz M Lote 33 Cayma"
        }
        request = self.client.post('/handmade/clientes/', data=nuevoCliente, format='json')
        self.assertEqual(request.data.get('content').get('clienteDocumento'),
                        nuevoCliente.get('clienteDocumento'))

    def test_post_client_exists_fail(self):

        nuevoCliente = {
            "clienteDocumento":"72750134",
            "clienteDireccion":"Mz M Lote 33 Cayma"
        }
        self.client.post('/gestion/clientes/', data=nuevoCliente, format='json')
        request = self.client.post('/handmade/clientes/', data=nuevoCliente, format='json')
        self.assertEqual(request.status_code,400)