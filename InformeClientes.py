import os

from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer, Paragraph, TableStyle, Table)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from sqlite3 import dbapi2

try:
    baseDatos = dbapi2.connect("database")
    cursor = baseDatos.cursor()

    detalleCliente = []
    pedidos = []

    detalleCliente.append(["CÓDIGO", "NOMBRE", "APELLIDOS", "TELÉFONO", "DIRECCIÓN", "EMAIL"])

    cursorConsultaDetalleCliente = cursor.execute("select codCliente,nombre,apellidos,telefono,direccion,email from clientes")
    consultaDetalleCliente = []
    for elementoCliente in cursorConsultaDetalleCliente:
        detalleCliente.append([elementoCliente[0], elementoCliente[1],elementoCliente[2],elementoCliente[3],elementoCliente[4],elementoCliente[5]])

    pedidos.append(list(detalleCliente))
    detalleCliente.clear()



except (dbapi2.DatabaseError):
    print("ERROR EN LA BASE DE DATOS")
finally:
    print("Cerramos la conexion a la BD")
    cursor.close()
    baseDatos.close()

doc = SimpleDocTemplate("InformeClientes.pdf", pagesize=A4)

guion = []

for pedido in pedidos:

    taboa = Table(pedido, colWidths=95, rowHeights=20)
    taboa.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 1), (0, 0), colors.blue),

        ('TEXTCOLOR', (0, 0), (5, 0), colors.green),

        ('BACKGROUND', (0, 1), (5, 3), colors.lightcyan),

        ('ALIGN', (5, 0), (5, 1), 'LEFT'),

        ('VALIGN', (1, 0), (5, -1), 'MIDDLE'),

        ('BOX', (0, 0), (-1, 2), 1, colors.black),

        ('BOX', (0, 2), (-1, -1), 1, colors.black),

        ('INNERGRID', (0, 3), (5, -2), 0.9, colors.grey),

    ]))

    guion.append(taboa)
    guion.append(Spacer(0,20))


doc.build(guion)
