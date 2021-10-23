from django.db import models
from handmade.models import OrdenCompraModel

class ComprobanteModel(models.Model):

    comprobanteId = models.AutoField(
        primary_key=True, unique=True, db_column='id')

    comprobanteSerie = models.CharField(
        max_length=4, null=False, db_column='serie')

    comprobanteNumero = models.CharField(
        max_length=8, null=False, db_column='numero')

    comprobanteTipo = models.CharField(
        choices=[('F', 'FACTURA'), ('B', 'BOLETA')], max_length=1, db_column='tipo', null=False)

    comprobantePDF = models.URLField(db_column='pdf', null=False)

    comprobanteXML = models.URLField(db_column='xml', null=False)

    comprobanteCDR = models.URLField(db_column='cdr', null=True)

    ordenCompra = models.OneToOneField(to=OrdenCompraModel, on_delete=models.CASCADE,
                                  db_column='pedido_id', related_name='ordenComprobante')

    class Meta:
        db_table = 'comprobantes'

