from django.contrib import admin
from .models import ProductoModel, CategoriaModel
# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoriaId', 'categoriaNombre', 'categoriaEstado']
    search_fields= ['categoriaNombre', 'categoriaEstado']
    readonly_fields=['CategoriaId']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['productoId','productoNombre', 'productoDescripcion', 'productoCantidad', 'productoPrecio']
    search_fields= ['productoNombre', 'productoDescripcion']
    readonly_fields=['productoId']

admin.site.register(CategoriaModel)
admin.site.register(ProductoModel, ProductoAdmin)

