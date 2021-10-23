from datetime import datetime

from handmade.serializer import DetalleOrdenSerializer
from .models import ComprobanteModel
from handmade.models import OrdenDetalleModel,OrdenCompraModel
from django.db import connection
from requests import post
from os import environ


def crearComprobante(tipo_de_comprobante: int, orden: OrdenCompraModel, documento_cliente: str, detalle: OrdenDetalleModel):

    comprobante_creado = ComprobanteModel.objects.filter(
        orden=orden.ordenId).first()

    if comprobante_creado:
        return 'La orden ya tiene un comprobante'

    operacion = 'generar_comprobante'
    if tipo_de_comprobante == 1:
        serie = 'FFF1'  # *
    elif tipo_de_comprobante == 2:
        serie = 'BBB1'

    ultimoComprobante = ComprobanteModel.objects.values_list('comprobanteNumero', 'comprobantePDF').filter(
        comprobanteSerie=serie).order_by('-comprobanteNumero').first()

    if not ultimoComprobante:
        numero = 1
    else:
        numero = int(ultimoComprobante[0]) + 1
    sunat_transaction = 1  # *

    cliente_tipo_de_documento = (
        1 if len(documento_cliente) == 8 else 6) if documento_cliente else 6

    cliente_numero_de_documento = documento_cliente

    cliente_denominacion = orden.cliente.clienteNombre
    cliente_direccion = ''
    cliente_email = orden.cliente.clienteCorreo
    fecha_de_emision = datetime.now()
    moneda = 1
    porcentaje_de_igv = 18

    total = float(detalle.ordenDetallePrecioTotal)

    # una vez generado el comprobante con el tipo de formato no se puede cambiar
    formato_de_pdf = 'TICKET'

    productos: list[OrdenDetalleModel] = orden.ordenDetalles.all()
    items = []
    for producto in productos:
        unidad_de_medida = 'NIU'  # *
        codigo = producto.detalleId
        descripcion = producto.producto.productoNombre
        cantidad = producto.detalleCantidad
        # valor_unitario = precio_con_igv / 1.18
        # calculadora IGV https://sibi.pe/calculadora/igv
        valor_unitario = float(producto.producto.productoPrecio) / 1.18
        precio_unitario = float(producto.producto.productoPrecio)
        subtotal = valor_unitario * cantidad
        tipo_de_igv = 1  # *
        igv = (valor_unitario * cantidad) * 0.18
        anticipo_regularizacion = False
        json = {
            'unidad_de_medida': unidad_de_medida,
            'codigo': codigo,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'valor_unitario': valor_unitario,
            'precio_unitario': precio_unitario,
            'subtotal': subtotal,
            'tipo_de_igv': tipo_de_igv,
            'igv': igv,
            'total': precio_unitario * cantidad,
            'anticipo_regularizacion': anticipo_regularizacion,
        }

        items.append(json)

    total_gravada = total / 1.18

    comprobante = {
        'operacion': operacion,
        'tipo_de_comprobante': tipo_de_comprobante,
        'serie': serie,
        'numero': numero,
        'sunat_transaction': sunat_transaction,
        'cliente_tipo_de_documento': cliente_tipo_de_documento,
        'cliente_numero_de_documento': cliente_numero_de_documento,
        'cliente_denominacion': cliente_denominacion,
        'cliente_direccion': cliente_direccion,
        'cliente_email': cliente_email,
        'fecha_de_emision': fecha_de_emision.strftime('%d-%m-%Y'),
        'moneda': moneda,
        'porcentaje_de_igv': porcentaje_de_igv,
        'total': total,
        'total_igv': total - total_gravada,
        'total_gravada': total_gravada,
        'formato_de_pdf': formato_de_pdf,
        'items': items,
        'enviar_automaticamente_a_la_sunat': True,
        'enviar_automaticamente_al_cliente': True
    }

    headers_nubefact = {
        'Authorization': environ.get('NUBEFACT_TOKEN'),
        'Content-Type': 'application/json'
    }

    respuesta = post(environ.get('NUBEFACT_URL'),
                     json=comprobante, headers=headers_nubefact)

    if respuesta.status_code == 200:
        tipo_de_comprobante = 'F' if tipo_de_comprobante == 1 else 'B'

        nuevoComprobante = ComprobanteModel(
            comprobanteSerie=serie,
            comprobanteNumero=numero,
            comprobanteTipo=tipo_de_comprobante,
            comprobantePDF=respuesta.json().get('enlace_del_pdf'),
            comprobanteXML=respuesta.json().get('enlace_del_xml'),
            comprobanteCDR=respuesta.json().get('enlace_del_cdr'),
            orden=orden)

        nuevoComprobante.save()

        return nuevoComprobante
    else:
        return respuesta.json().get('errors')


def visualizarComprobante():
    pass
