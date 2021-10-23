from django.contrib.auth.models import BaseUserManager

class ManejoCliente(BaseUserManager):
    def create_user(self, correo, nombre, tipo_doc,nro_doc, tipo, direccion, clientePassword=None):
        if not correo:
            raise ValueError('El cliente debe de contar con un CORREO válido')

        email = self.normalize_email(correo)
        clienteCreado = self.model(clienteCorreo=email, clienteNombre=nombre, clienteTipoDoc=tipo_doc, clienteNroDoc=nro_doc, clienteTipo=tipo, clienteDireccion=direccion)

        clienteCreado.set_password(clientePassword)
        clienteCreado.save(using=self._db)

        return clienteCreado
    
    def create_superuser(self,clienteCorreo,clienteNombre,clienteTipoDoc, clienteNroDoc,clienteTipo, clienteDireccion, clientePassword ):
        nuevoCliente=self.create_superuser(clienteCorreo, clienteNombre, clienteTipoDoc,clienteNroDoc,clienteTipo, clienteDireccion,clientePassword)
        nuevoCliente.is_superuser=True
        nuevoCliente.is_staff=True
        nuevoCliente.save(using=self._db)