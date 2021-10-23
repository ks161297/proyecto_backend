from django.http import request
from rest_framework.test import APITestCase
from .models import CategoriaModel, ProductoModel,ClienteModel,OrdenCompraModel, OrdenDetalleModel





# class productos(APITestCase):
#     def setUp(self):
#         CategoriaModel(
#             categoriaId = 6,
#             categoriaNombre = 'Dia de la madre').save()
#         ProductoModel(
#             productoNombre = 'Caja Artesanal x 24',
#             productoDescripcion = 'Caja Artesanal z 24',
#             productoCantidad = 20,
#             productoEstado = True,
#             productoImagen = 'cajaartesanal.jpg',
#             productoPrecio = 60.90,
#             categoria=6).save()

#         ProductoModel(
#             productoNombre = 'Caja Artesanal x 32',
#             productoDescripcion = 'Caja Artesanal x 32',
#             productoCantidad = 40,
#             productoEstado = False,
#             productoImagen = 'cajaartesanal32.jpg',
#             productoPrecio = 80.90,
#             categoria=6).save()
    
#     def test_post_fail(self):
#         request = self.client.post('/handmade/productos/')
#         message = request.data.get('message')

#         self.assertEqual(request.status_code, 400)
#         self.assertEqual(message, 'Error al registrar el producto')

#     def test_post_sucess(self):
#         request = self.client.post('/handmade/productos/', data={
#             "productoId":1,
#             "productoNombre":"Caja Artesanal",
#             "productoDescripcion":"Caja Artesanal",
#             "productoCantidad":20,
#             "productoEstado": True,
#             "productoImagen":"cajaartesanal.jpg",
#             "productoPrecio":60.90,
#             "categoria":10
#         }, format='json')
#         message = request.data.get('message')
#         id = request.data.get('content').get('productoId')
#         productoEncontrado = ProductoModel.objects.filter(productoId  = id).first();

#         self.assertEqual(request.status_code, 201)
#         self.assertEqual(message, 'Producto creado con exito')
#         self.assertIsNotNone(productoEncontrado)

#     def test_get_sucess(self):
#         productosEncontrados = ProductoModel.objects.all()
#         request = self.client.get('/handmade/productos/')
#         message = request.data.get('message')
#         self.assertEqual(request.status_code, 201)
#         self.assertEqual(message, 'Productos encontrados')
#         self.assertIsNotNone(productosEncontrados)
