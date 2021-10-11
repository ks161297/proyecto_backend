from django.shortcuts import render
from rest_framework import serializers 
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializer import CategoriaSerializer
from .models import CategoriaModel


class CategoriaController(ListCreateAPIView):
    queryset = CategoriaModel.objects.all()
    serializer_class = CategoriaSerializer
    def post(self, request:Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                'message':'Categoria registrada con exito',
                'content': data.data
            })
        else:
            return Response(data={
                'message':'Error al registrar la categoria',
                'content': data.errors 
            })
    def put(self, request:Request, id):
        categoriaEncontrada = CategoriaModel.objects.filter(categoriaId = id).first()
        if categoriaEncontrada is None:
            return Response(data={
                'message':'Esta categoria no existe',
                'content':None
            })
        serializador = CategoriaSerializer(data=request.data)
        if serializador.is_valid():
            serializador.update(instance=categoriaEncontrada, validated_data=serializador.validated_data)
            return Response(data={
                'message':'La categoría fue actualizada con exito',
                'content':serializador.data
            })
        else:
            return Response(data={
                'message':'Error al actualizar la categoria',
                'content':serializador.errors
            })
    def get(self, request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        return Response(data={
            'message':'Las categorias que existen son:',
            'content': data.data
        })