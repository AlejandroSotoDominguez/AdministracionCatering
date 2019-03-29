from sqlite3 import dbapi2

import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class FiestraPrincipal(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Gestión Clientes")

        self.baseDatos = dbapi2.connect("database")
        self.cursor = self.baseDatos.cursor()
        self.set_border_width(10)
        self.baseDatos.commit()

        try:
            boxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            modelo = Gtk.ListStore (str,str,str,str,str,str)
            self.filtro_categoria = modelo.filter_new()
            self.filtro_categoria.set_visible_func(self.categoria_filtro)
            self.parametro_filtro_categoria = None

            cursorCodCliente = self.cursor.execute("select * from clientes")

            for codCliente in cursorCodCliente:
                modelo.append(codCliente)


            vista = Gtk.TreeView(model = self.filtro_categoria)
            seleccion = vista.get_selection()
            seleccion.connect("changed", self.on_seleccion_changed)
            boxV.pack_start(vista, True, True, 0)

            celdaText = Gtk.CellRendererText()
            celdaText.set_property("editable", True)
            celdaText.connect("edited", self.on_celdaText_edited, modelo)

            columnaCod = Gtk.TreeViewColumn ('Cod cliente', celdaText, text = 0)
            columnaCod.set_sort_column_id (0)
            vista.append_column (columnaCod)

            celdaNombre = Gtk.CellRendererText (xalign = 0.5, width=150)
            columnaNombre = Gtk.TreeViewColumn ('Nombre', celdaNombre, text = 1)
            vista.append_column (columnaNombre)

            celdaApellidos = Gtk.CellRendererText (xalign = 0.5, width=150)
            columnaApellidos = Gtk.TreeViewColumn ('Apellidos', celdaApellidos, text = 2)
            vista.append_column (columnaApellidos)

            celdaTelefono = Gtk.CellRendererText (xalign = 0.5, width=150)
            columnaTelefono = Gtk.TreeViewColumn ('Teléfono', celdaTelefono, text = 3)
            vista.append_column (columnaTelefono)

            celdaDireccion = Gtk.CellRendererText(width=200)
            columnaDireccion = Gtk.TreeViewColumn ('Dirección', celdaDireccion, text = 4)
            vista.append_column (columnaDireccion)

            celdaEmail = Gtk.CellRendererText()
            columnaEmail = Gtk.TreeViewColumn ('Email', celdaEmail, text = 5)
            vista.append_column (columnaEmail)

            boxH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.codCliente = Gtk.Entry()
            self.nombre = Gtk.Entry()
            self.apellidos = Gtk.Entry()
            self.telefono = Gtk.Entry()
            self.direccion = Gtk.Entry()
            self.email = Gtk.Entry()

            self.codCliente.set_placeholder_text("Código Cliente")
            self.nombre.set_placeholder_text("Nombre")
            self.apellidos.set_placeholder_text("Apellidos")
            self.telefono.set_placeholder_text("Teléfono")
            self.direccion.set_placeholder_text("Dirección")
            self.email.set_placeholder_text("Email")


            boxH.pack_start(self.codCliente, True, True, 0)
            boxH.pack_start(self.nombre, True, True, 0)
            boxH.pack_start(self.apellidos, True, True, 0)
            boxH.pack_start(self.telefono, True, True, 0)
            boxH.pack_start(self.direccion, True, True, 0)
            boxH.pack_start(self.email, True, True, 0)
            btnEngadir = Gtk.Button(label = "Añadir")
            btnModificar = Gtk.Button(label = "Modificar")
            btnEngadir.connect("clicked", self.on_btnEngadir_clicked, modelo)
            btnModificar.connect("clicked", self.on_btnModificar_clicked, modelo)
            boxH.pack_start(btnEngadir, True, True, 0)
            boxH.pack_start(btnModificar, True, True, 0)

            boxV.pack_start(boxH, True, True, 0)

            boxHFiltro = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

            boxV.pack_start(boxHFiltro, True, True, 0)

            btnBorrar = Gtk.Button(label="Borrar")
            boxHFiltro.pack_start(btnBorrar, False, False, 0)
            btnBorrar.connect("clicked", self.on_btnBorrar_clicked, modelo)

            btnLimpiar = Gtk.Button(label="Limpiar")
            boxHFiltro.pack_start(btnLimpiar, False, False, 0)
            btnLimpiar.connect("clicked", self.on_btnLimpiar_clicked, modelo)

            btnInforme = Gtk.Button(label="Sacar Informe Clientes")
            boxHFiltro.pack_start(btnInforme, False, False, 20)
            btnInforme.connect("clicked", self.on_btnInforme_clicked, modelo)

            btnFactura = Gtk.Button(label="Sacar Factura")
            boxHFiltro.pack_start(btnFactura, False, False, 0)
            btnInforme.connect("clicked", self.on_btnFactura_clicked, modelo)


            self.add(boxV)

            self.connect("destroy", Gtk.main_quit)
            self.show_all()

        except Exception as e:
            print(e)

    def on_btnEngadir_clicked(self, punteiro, modelo):
        datos = [self.codCliente.get_text(), self.nombre.get_text(), self.apellidos.get_text(),self.telefono.get_text(),self.direccion.get_text(),self.email.get_text()]
        modelo.append(datos)

        self.cursor.execute("insert into clientes(codCliente,nombre,apellidos,telefono,direccion,email) values(?,?,?,?,?,?)", (self.codCliente.get_text(), self.nombre.get_text(), self.apellidos.get_text(),self.telefono.get_text(),self.direccion.get_text(),self.email.get_text()))
        self.baseDatos.commit()


    def on_seleccion_changed(self,seleccion):
        modelo,punteiro = seleccion.get_selected()
        if punteiro is not None:
            self.codCliente.set_text(modelo[punteiro][0])
            self.nombre.set_text(modelo[punteiro][1])
            self.apellidos.set_text(modelo[punteiro][2])
            self.telefono.set_text(modelo[punteiro][3])
            self.direccion.set_text(modelo[punteiro][4])
            self.email.set_text(modelo[punteiro][5])


    def on_celdaText_edited(self, control, punteiro, texto, modelo):
        modelo[punteiro][0] = texto

    def categoria_filtro(self, modelo, punteiro, datos):
        if self.parametro_filtro_categoria is None:
            return True
        else:
            if modelo[punteiro][4] == self.parametro_filtro_categoria:
                return True
            else:
                return False

    def on_btnBorrar_clicked(self, punteiro, modelo):
        self.cursor.execute("delete from clientes where codCliente = ?", self.codCliente.get_text())
        modelo.clear()

        cursorCodCliente = self.cursor.execute("select * from clientes")

        for codCliente in cursorCodCliente:
            modelo.append(codCliente)

        self.baseDatos.commit()

    def on_btnLimpiar_clicked(self, punteiro, modelo):
        self.codCliente.set_text("")
        self.nombre.set_text("")
        self.apellidos.set_text("")
        self.telefono.set_text("")
        self.direccion.set_text("")
        self.email.set_text("")

    def on_btnModificar_clicked(self, punteiro, modelo):
        self.cursor.execute("update clientes set codCliente = ?, nombre = ?, apellidos = ?, telefono = ?, direccion = ?, email = ? where codCliente = ?", (self.codCliente.get_text(), self.nombre.get_text(), self.apellidos.get_text(),self.telefono.get_text(), self.direccion.get_text(), self.email.get_text(), self.codCliente.get_text()))

        modelo.clear()

        cursorCodCliente = self.cursor.execute("select * from clientes")

        for codCliente in cursorCodCliente:
            modelo.append(codCliente)


        self.baseDatos.commit()

    def on_btnInforme_clicked(self, punteiro, modelo):
        """
        Función que llama al script que genera un informe
        :param punteiro:
        :param modelo:
        :return:
        """
        os.system("python3 InformeClientes.py")
        print("Informe generado")

    def on_btnFactura_clicked(self, punteiro, modelo):
        """
        Función que llama al script que genera la factura
        :param punteiro:
        :param modelo:
        :return:
        """
        os.system("python3 Factura.py")
        print("Factura generada")


if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()
