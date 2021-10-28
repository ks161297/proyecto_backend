from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .authManager import ManejoCliente


class CategoriaModel(models.Model):
    categoriaId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    categoriaNombre = models.CharField(db_column='nombre', max_length=50, null=False, unique=True)
    categoriaEstado = models.BooleanField(db_column='estado', null=False, default=True)
    class Meta:
        db_table = 'categoria'
class ProductoModel(models.Model):
    productoId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    productoNombre = models.CharField(db_column='nombre', max_length=50, null=False)
    productoDescripcion = models.CharField(db_column='descripcion', max_length=100)
    productoCantidad = models.IntegerField(db_column='cantidad', null=False, default=0)
    productoEstado = models.BooleanField(db_column='estado', null=False, default=True)
    #Imagen Cloudinary
    productoImagen = models.TextField(db_column='imagen',  null=False)
    productoPrecio = models.DecimalField(db_column='precio', max_digits=5, decimal_places=2 )
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True) 
    created_At = models.DateTimeField(db_column='created_at', auto_now_add=True)

    # *** RELACIONES

    categoria = models.ForeignKey(to=CategoriaModel, db_column='categoria_id', related_name='categoriaProducto', null=False, on_delete=models.PROTECT) 

    class Meta:
        db_table = 'productos'
class ClienteModel(AbstractBaseUser, PermissionsMixin):

    TIPO_DOCUMENTO = [(1, 'DNI'), (2,'PASAPORTE')]
    TIPO_CLIENTE   = [(1, 'ADMINISTRADOR'), (2, 'CLIENTE')]

    clienteId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    clienteNombre = models.CharField(db_column='nombre', max_length=50, null=False)
    clienteTipoDoc = models.IntegerField(db_column='tipo_doc',choices=TIPO_DOCUMENTO)
    clienteNroDoc = models.IntegerField(db_column='nro_doc',unique=True)
    clienteDireccion = models.CharField(db_column='direccion', max_length=100)
    clienteTipo = models.IntegerField(db_column='tipo', choices=TIPO_CLIENTE)
    clienteEstado = models.BooleanField(db_column='estado', null=False, default=True)
    clienteCorreo = models.EmailField(db_column='correo', max_length=50, unique=True)
    password = models.TextField(null=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = ManejoCliente()

    USERNAME_FIELD = 'clienteCorreo'
    REQUIRED_FIELDS = ['clienteNombre','clienteTipoDoc','clienteNroDoc','clienteDireccion', 'clienteTipo','clienteEstado']

    class Meta:
        db_table = 'clientes'    
class OrdenCompraModel(models.Model):
    ordenId = models.AutoField(db_column='id', primary_key=True, unique=True, null=False)
    ordenFecha = models.DateTimeField(db_column='fecha',auto_now_add=True)
    ordenDireccion = models.CharField(db_column='direccion',max_length=100, null=False)
    ordenCorreo = models.CharField(db_column='correo', max_length=50, null=False)
    ordenEstado = models.BooleanField(db_column='estado', default=True)
    ordenTotal = models.DecimalField(db_column='total', max_digits=5, decimal_places=2)

    # *** RELACIONES

    cliente = models.ForeignKey(to=ClienteModel, db_column='cliente_id', related_name='pedidoCliente', null=False, on_delete=models.PROTECT)

    class Meta:
        db_table = 'orden_compra'
class OrdenDetalleModel(models.Model):
    ordenDetalleId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    ordenDetalleCantidad = models.IntegerField(db_column='cantidad', null=False, default=0)
    ordenDetalleSubTotal = models.DecimalField(db_column='sub_total', max_digits=5, decimal_places=2 )


    # *** RELACIONES

    ordenCompra = models.ForeignKey(to=OrdenCompraModel, db_column='pedido_id', related_name='detallePedido', null=False, on_delete=models.PROTECT)
    producto = models.ForeignKey(to=ProductoModel, db_column='producto_id', related_name='detalleProducto', null=False, on_delete=models.PROTECT)
    class Meta:
        db_table = 'orden_detalle'
        verbose_name = 'detalle'
