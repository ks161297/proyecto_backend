from django.urls import path
from .views import CategoriaController

urlpatterns = [
    path('categorias/', CategoriaController.as_view()),
    path('categoria/<int:id>', CategoriaController.as_view()),
]