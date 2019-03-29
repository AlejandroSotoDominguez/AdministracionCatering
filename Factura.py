import os

from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, TableStyle, Table)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from sqlite3 import dbapi2

try:
    baseDatos = dbapi2.connect("database")
    cursor = baseDatos.cursor()

    detallePedido = []
    pedidos = []

    cursorConsultaNumPedidos = cursor.execute("select codPedido from pedidos")
    listaPedidos = []
    for codPedido in cursorConsultaNumPedidos:
        if codPedido[0] not in listaPedidos:
            listaPedidos.append(codPedido[0])


    for codPedido in listaPedidos:
        codCliente = None
        consultaPedido = None
        cursorConsultaPedidos = cursor.execute("select codCliente from pedidos where codPedido=?",(int(codPedido),))
        codCliente = cursorConsultaPedidos.fetchone()[0]

        detallePedido.append(['Codigo Cliente: ',codCliente,'','Num Pedido: ',codPedido])

        cursorConsultaPedido = cursor.execute("select nombre,direccion from clientes where codCliente=?",(codCliente,))
        rexistroCliente = cursorConsultaPedido.fetchone()

        detallePedido.append(['Nombre: ', rexistroCliente[0],'','','' ])
        detallePedido.append(['Direccion: ', rexistroCliente[1], '', '', ''])

        cursorConsultaDetallePedido = cursor.execute("select codProducto,cantidad from pedidos where codPedido=?",(int(codPedido),))
        consultaDetallePedido = []
        for elementoPedido in cursorConsultaDetallePedido:
            consultaDetallePedido.append([elementoPedido[0],elementoPedido[1]])

        detallePedido.append(["CÓDIGO", "PRODUCTO", "CANTIDAD", "PRECIO UNIDAD:", "PRECIO"])

        precioTotal = 0
        for elemento in consultaDetallePedido:
            cursorConsultaProducto = cursor.execute("select descripcion,precio from productos where codProducto=?",(elemento[0]))
            registroProducto = cursorConsultaProducto.fetchone()
            precio = elemento[1]*registroProducto[1]
            detallePedido.append([elemento[0], registroProducto[0], elemento[1], registroProducto[1], round(elemento[1]*registroProducto[1],2)])
            precioTotal = precioTotal + precio


    detallePedido.append(["","","","Precio total:", precioTotal])

    pedidos.append(list(detallePedido))
    detallePedido.clear()



except (dbapi2.DatabaseError):
    print("ERROR EN LA BASE DE DATOS")
finally:
    print("Cerramos la conexion a la BD")
    cursor.close()
    baseDatos.close()

doc = SimpleDocTemplate("Factura.pdf", pagesize=A4)

guion = []

for pedido in pedidos:

    taboa = Table(pedido, colWidths=90, rowHeights=30)
    taboa.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 2), colors.blue),

        ('TEXTCOLOR', (0, 4), (-1, -1), colors.green),

        ('BACKGROUND', (0, 4), (-1, -1), colors.lightcyan),

        ('ALIGN', (2, 5), (-1, -1), 'RIGHT'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('BOX', (0, 0), (-1, 2), 1, colors.black),

        ('BOX', (0, 3), (-1, -2), 1, colors.black),

        ('INNERGRID', (0, 3), (-1, -2), 0.5, colors.grey),

    ]))

    guion.append(taboa)
    guion.append(Spacer(0,20))


doc.build(guion)
