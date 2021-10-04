from django.db import models

class CategoriaModel(models.Model):
    categoriaId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    categoriaNombre = models.CharField(db_column='nombre', max_length=50, null=False)
    class Meta:
        db_table = 'categoria'
class ProductoModel(models.Model):
    productoId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    productoNombre = models.CharField(db_column='nombre', max_length=50, null=False)
    productoDescripcion = models.CharField(db_column='descripcion', max_length=100)
    productoCantidad = models.IntegerField(db_column='cantidad', null=False, default=0)
    productoEstado = models.BooleanField(db_column='estado', null=False, default=True)
    productoImagen = models.ImageField(upload_to='productos/', db_column='foto', null=False)
    productoPrecio = models.DecimalField(db_column='precio', max_digits=5, decimal_places=2 )
    updateAt = models.DateTimeField(db_column='updated_at', auto_now=True) 
    created_At = models.DateTimeField(db_column='created_at', auto_now_add=True)

    # *** RELACIONES

    categoria = models.ForeignKey(to=CategoriaModel, db_column='categoria_id', related_name='categoriaProducto', null=False, on_delete=models.PROTECT) 

    class Meta:
        db_table = 'productos'
class ClienteModel(models.Model):
   
    TIPO_DOCUMENTO = [(1, 'DNI'), (2,'PASAPORTE')]
    TIPO_USUARIO   = [(1, 'ADMINISTRADOR'), (2, 'CLIENTE')]

    clienteId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    clienteNombre = models.CharField(db_column='nombre', max_length=50, null=False)
    clienteTipoDoc = models.TextField(db_column='tipo_doc',choices=TIPO_DOCUMENTO)
    clienteNroDoc = models.IntegerField(db_column='nro_doc', null=False, unique=True)
    clienteDireccion = models.CharField(db_column='direccion', max_length=100)
    clienteTipo = models.TextField(db_column='tipo', choices=TIPO_USUARIO)
    clienteCorreo = models.EmailField(db_column='correo', max_length=50, null=False, unique=True)
    clientePassword = models.TextField(null=False)

    class Meta:
        db_table = 'clientes'    
class CarritoModel(models.Model):
    carritoId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    carritoFechaCreacion = models.DateTimeField(db_column='fecha', auto_now_add=True)

     # *** RELACIONES

    productos = models.ForeignKey(to=ProductoModel, db_column='producto_id', related_name='carritoProductos', null=False, on_delete=models.PROTECT)
    cliente = models.ForeignKey(to=ClienteModel, db_column='cliente_id', related_name='carritoCliente', null=False, on_delete=models.PROTECT)

    class Meta:
        db_table = 'carrito'

class ListaModel(models.Model):
    listaId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    listaFechaCreacion = models.DateTimeField(db_column='fecha', auto_now_add=True)

     # *** RELACIONES

    productos = models.ForeignKey(to=ProductoModel, db_column='producto_id', related_name='listaProductos', null=False, on_delete=models.PROTECT)
    cliente = models.ForeignKey(to=ClienteModel, db_column='cliente_id', related_name='listaCliente', null=False, on_delete=models.PROTECT)

    class Meta:
        db_table = 'lista'
class OrdenCompraModel(models.Model):
    ordenId = models.AutoField(db_column='id', primary_key=True, unique=True, null=False)
    ordenFecha = models.DateTimeField(db_column='fecha',auto_now_add=True)
    ordenDireccion = models.CharField(db_column='direccion',max_length=100, null=False)
    ordenCorreo = models.CharField(db_column='correo', max_length=50, null=False)
    ordenEstado = models.BooleanField(db_column='estado', default=True)

    # *** RELACIONES

    cliente = models.ForeignKey(to=ClienteModel, db_column='cliente_id', related_name='pedidoCliente', null=False, on_delete=models.PROTECT)

    class Meta:
        db_table = 'orden_compra'

class MetodoPagoModel(models.Model):
    TIPO_METODO = [(1, 'EFECTIVO'), (2,'TARJETA')]

    metodoId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    metodoTipo = models.TextField(db_column='tipoDoc', choices=TIPO_METODO)
    metodoNro = models.IntegerField(db_column='nro')

    class Meta: 
        db_table = 'metodo_pago'
class OrdenDetalleModel(models.Model):
    ordenDetalleId = models.AutoField(db_column='id', primary_key=True, null=False, unique=True)
    ordenDetalleCantidad = models.IntegerField(db_column='cantidad', null=False, default=0)
    ordenDetallePrecioUnitario = models.DecimalField(db_column='precioUnitario', max_digits=5, decimal_places=2 )
    ordenDetallePrecioTotal = models.DecimalField(db_column='precioTotal', max_digits=5, decimal_places=2 )


    # *** RELACIONES

    ordenCompra = models.ForeignKey(to=OrdenCompraModel, db_column='pedido_id', related_name='detallePedido', null=False, on_delete=models.PROTECT)
    producto = models.ForeignKey(to=ProductoModel, db_column='producto_id', related_name='detalleProducto', null=False, on_delete=models.PROTECT)
    metodoPago = models.ForeignKey(to=MetodoPagoModel, db_column='metodo_id', null=False, related_name='ordenMetodo', on_delete=models.PROTECT)
    class Meta:
        db_table = 'orden_detalle'
