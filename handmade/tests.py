from rest_framework.test import APITestCase
from .models import CategoriaModel, ProductoModel,ClienteModel,OrdenCompraModel, OrdenDetalleModel


class clientes(APITestCase):
    pass
class categorias(APITestCase):
    def setUp(self):
        CategoriaModel(
            categoriaId = 6,
            categoriaNombre = 'Dia de la madre',
            categoriaEstado = True).save()
        CategoriaModel(
            categoriaId = 10,
            categoriaNombre = 'Dia del padre',
            categoriaEstado = False).save()

    def test_post_fail(self):
        request = self.client.post('/handmade/categorias/')
        message = request.data.get('message')

        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al registrar la categoria')

    def test_post_sucess(self):
        request = self.client.post('/handmade/categorias/', data={
            "categoriaId":6,
            "categoriaNombre":"Dia de la madrel",
            "categoriaEstado":True,
        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('categoriaId')
        categoriaEncontrado = CategoriaModel.objects.filter(categoriaId  = id).first();

        self.assertEqual(request.status_code, 200)
        self.assertEqual(message, 'Categoria registrada con exito')
        self.assertIsNotNone(categoriaEncontrado)

    def test_get_sucess(self):
        categoriasEncontradas = CategoriaModel.objects.all()
        request = self.client.get('/handmade/categorias/')
        message = request.data.get('message')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(message, 'Categorías encontradas')
        self.assertIsNotNone(categoriasEncontradas)
    

class productos(APITestCase):
    def setUp(self):
        ProductoModel(
            productoId = 14,
            productoNombre = 'Caja Artesanal x 24',
            productoDescripcion = 'Caja Artesanal z 24',
            productoCantidad = 20,
            productoEstado = True,
            productoImagen = 'cajaartesanal.jpg',
            productoPrecio = 60.90).save()
        ProductoModel(
            productoId = 19,
            productoNombre = 'Caja Artesanal x 32',
            productoDescripcion = 'Caja Artesanal x 32',
            productoCantidad = 40,
            productoEstado = False,
            productoImagen = 'cajaartesanal32.jpg',
            productoPrecio = 80.90).save()
    
    def test_post_fail(self):
        request = self.client.post('/handmade/productos/')
        message = request.data.get('message')

        self.assertEqual(request.status_code, 400)
        self.assertEqual(message, 'Error al registrar el producto')

    def test_post_sucess(self):
        request = self.client.post('/handmade/productos/', data={
            "productoId":1,
            "productoNombre":"Caja Artesanal",
            "productoDescripcion":"Caja Artesanal",
            "productoCantidad":20,
            "productoEstado": True,
            "productoImagen":"cajaartesanal.jpg",
            "productoPrecio":60.90
        }, format='json')
        message = request.data.get('message')
        id = request.data.get('content').get('productoId')
        productoEncontrado = ProductoModel.objects.filter(productoId  = id).first();

        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, 'Producto creado con exito')
        self.assertIsNotNone(productoEncontrado)

    def test_get_sucess(self):
        productosEncontrados = ProductoModel.objects.all()
        request = self.client.get('/handmade/productos/')
        message = request.data.get('message')
        self.assertEqual(request.status_code, 201)
        self.assertEqual(message, 'Productos encontrados')
        self.assertIsNotNone(productosEncontrados)
