# Generated by Django 3.2.7 on 2021-10-23 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('handmade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprobanteModel',
            fields=[
                ('comprobanteId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('comprobanteSerie', models.CharField(db_column='serie', max_length=4)),
                ('comprobanteNumero', models.CharField(db_column='numero', max_length=8)),
                ('comprobanteTipo', models.CharField(choices=[('F', 'FACTURA'), ('B', 'BOLETA')], db_column='tipo', max_length=1)),
                ('comprobantePDF', models.URLField(db_column='pdf')),
                ('comprobanteXML', models.URLField(db_column='xml')),
                ('comprobanteCDR', models.URLField(db_column='cdr', null=True)),
                ('ordenCompra', models.OneToOneField(db_column='pedido_id', on_delete=django.db.models.deletion.CASCADE, related_name='ordenComprobante', to='handmade.ordencompramodel')),
            ],
            options={
                'db_table': 'comprobantes',
            },
        ),
    ]
