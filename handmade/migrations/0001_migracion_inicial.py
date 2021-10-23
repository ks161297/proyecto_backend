# Generated by Django 3.2.7 on 2021-10-23 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('clienteId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('clienteNombre', models.CharField(db_column='nombre', max_length=50)),
                ('clienteTipoDoc', models.TextField(choices=[(1, 'DNI'), (2, 'PASAPORTE')], db_column='tipo_doc')),
                ('clienteNroDoc', models.IntegerField(db_column='nro_doc', unique=True)),
                ('clienteDireccion', models.CharField(db_column='direccion', max_length=100)),
                ('clienteTipo', models.TextField(choices=[(1, 'ADMINISTRADOR'), (2, 'CLIENTE')], db_column='tipo')),
                ('clienteEstado', models.BooleanField(db_column='estado', default=True)),
                ('clienteCorreo', models.EmailField(db_column='correo', max_length=50, unique=True)),
                ('password', models.TextField()),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='CategoriaModel',
            fields=[
                ('categoriaId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('categoriaNombre', models.CharField(db_column='nombre', max_length=50, unique=True)),
                ('categoriaEstado', models.BooleanField(db_column='estado', default=True)),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='OrdenCompraModel',
            fields=[
                ('ordenId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('ordenFecha', models.DateTimeField(auto_now_add=True, db_column='fecha')),
                ('ordenDireccion', models.CharField(db_column='direccion', max_length=100)),
                ('ordenCorreo', models.CharField(db_column='correo', max_length=50)),
                ('ordenEstado', models.BooleanField(db_column='estado', default=True)),
                ('ordenTotal', models.DecimalField(db_column='total', decimal_places=2, max_digits=5)),
                ('cliente', models.ForeignKey(db_column='cliente_id', on_delete=django.db.models.deletion.PROTECT, related_name='pedidoCliente', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orden_compra',
            },
        ),
        migrations.CreateModel(
            name='ProductoModel',
            fields=[
                ('productoId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('productoNombre', models.CharField(db_column='nombre', max_length=50)),
                ('productoDescripcion', models.CharField(db_column='descripcion', max_length=100)),
                ('productoCantidad', models.IntegerField(db_column='cantidad', default=0)),
                ('productoEstado', models.BooleanField(db_column='estado', default=True)),
                ('productoImagen', models.TextField(db_column='imagen')),
                ('productoPrecio', models.DecimalField(db_column='precio', decimal_places=2, max_digits=5)),
                ('updateAt', models.DateTimeField(auto_now=True, db_column='updated_at')),
                ('created_At', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('categoria', models.ForeignKey(db_column='categoria_id', on_delete=django.db.models.deletion.PROTECT, related_name='categoriaProducto', to='handmade.categoriamodel')),
            ],
            options={
                'db_table': 'productos',
            },
        ),
        migrations.CreateModel(
            name='OrdenDetalleModel',
            fields=[
                ('ordenDetalleId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('ordenDetalleCantidad', models.IntegerField(db_column='cantidad', default=0)),
                ('ordenDetalleSubTotal', models.DecimalField(db_column='sub_total', decimal_places=2, max_digits=5)),
                ('ordenCompra', models.ForeignKey(db_column='pedido_id', on_delete=django.db.models.deletion.PROTECT, related_name='detallePedido', to='handmade.ordencompramodel')),
                ('producto', models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.PROTECT, related_name='detalleProducto', to='handmade.productomodel')),
            ],
            options={
                'verbose_name': 'detalle',
                'db_table': 'orden_detalle',
            },
        ),
    ]