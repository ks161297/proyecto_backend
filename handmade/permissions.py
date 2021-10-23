from rest_framework import permissions
from rest_framework.request import Request


class CorreoPermission(permissions.BasePermission):

    def has_permission(self, request: Request, view):
        print(view)
        print(request)
        if(request.user.clienteCorreo == 'mksss161297@gmail.com'):
            return True
        else:
            return False