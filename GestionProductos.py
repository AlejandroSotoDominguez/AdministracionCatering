from sqlite3 import dbapi2

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class FiestraPrincipal(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Gestión Productos")

        self.baseDatos = dbapi2.connect("database")
        self.cursor = self.baseDatos.cursor()
        self.set_border_width(10)

        try:
            boxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            modelo = Gtk.ListStore (str,str,str,float,int)
            self.filtro_categoria = modelo.filter_new()
            self.filtro_categoria.set_visible_func(self.categoria_filtro)
            self.parametro_filtro_categoria = None

            cursorCodCliente = self.cursor.execute("select * from productos")

            for codProducto in cursorCodCliente:
                modelo.append(codProducto)

            """TreeView"""
            vista = Gtk.TreeView(model = self.filtro_categoria)
            seleccion = vista.get_selection()
            seleccion.connect("changed", self.on_seleccion_changed)
            boxV.pack_start(vista, True, True, 0)

            celdaText = Gtk.CellRendererText()
            celdaText.set_property("editable", True)
            celdaText.connect("edited", self.on_celdaText_edited, modelo)

            columnaCod = Gtk.TreeViewColumn ('Código Producto', celdaText, text = 0)
            columnaCod.set_sort_column_id (0)
            vista.append_column (columnaCod)

            celdaNombre = Gtk.CellRendererText (xalign = 0.5, width=250)
            columnaNombre = Gtk.TreeViewColumn ('Nombre', celdaNombre, text = 1)
            vista.append_column (columnaNombre)

            celdaDescripcion = Gtk.CellRendererText (xalign = 0.5, width=150)
            columnaDescripcion = Gtk.TreeViewColumn ('Descripción', celdaDescripcion, text = 2)
            vista.append_column (columnaDescripcion)

            celdaPrecio = Gtk.CellRendererText (xalign = 0.5, width=150)
            columnaPrecio = Gtk.TreeViewColumn ('Precio', celdaPrecio, text = 3)
            vista.append_column (columnaPrecio)

            celdaCantidad = Gtk.CellRendererText(width=200)
            columnaCantidad = Gtk.TreeViewColumn ('Cantidad', celdaCantidad, text = 4)
            vista.append_column (columnaCantidad)

            """Campos de texto"""
            boxH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            self.codProducto = Gtk.Entry()
            self.nombre = Gtk.Entry()
            self.descripcion = Gtk.Entry()
            self.precio = Gtk.Entry()
            self.cantidad = Gtk.Entry()

            self.codProducto.set_placeholder_text("Código Producto")
            self.nombre.set_placeholder_text("Nombre")
            self.descripcion.set_placeholder_text("Descripción")
            self.precio.set_placeholder_text("Precio")
            self.cantidad.set_placeholder_text("Cantidad")

            boxH.pack_start(self.codProducto, True, True, 0)
            boxH.pack_start(self.nombre, True, True, 0)
            boxH.pack_start(self.descripcion, True, True, 0)
            boxH.pack_start(self.precio, True, True, 0)
            boxH.pack_start(self.cantidad, True, True, 0)
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
            
            self.add(boxV)

            self.connect("destroy", Gtk.main_quit)
            self.show_all()

        except Exception as e:
            print(e)

    def on_btnEngadir_clicked(self, punteiro, modelo):
        """
        Función que inserta los datos en la base de datos
        :param punteiro
        :param modelo de la tabla
        """
        datos = [self.codProducto.get_text(), self.nombre.get_text(), self.descripcion.get_text(),float(self.precio.get_text()), int(self.cantidad.get_text())]
        modelo.append(datos)

        self.cursor.execute("insert into productos(codProducto,nombre,descripcion,precio,cantidad) values(?,?,?,?,?)", (self.codProducto.get_text(), self.nombre.get_text(), self.descripcion.get_text(), float(self.precio.get_text()), int(self.cantidad.get_text())))
        self.baseDatos.commit()


    def on_seleccion_changed(self,seleccion):
        """
        Función que añade los registros de la base de datos al treeview
        :param seleccion: campo seleccionado
        """
        modelo,punteiro = seleccion.get_selected()
        if punteiro is not None:
            self.codProducto.set_text(modelo[punteiro][0])
            self.nombre.set_text(modelo[punteiro][1])
            self.descripcion.set_text(modelo[punteiro][2])
            self.precio.set_text(str(modelo[punteiro][3]))
            self.cantidad.set_text(str(modelo[punteiro][4]))


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
        """
        Función que permite borrar una fila
        :param punteiro: campo seleccionado
        :param modelo: modelo de la tabla
        :return:
        """
        self.cursor.execute("delete from productos where codProducto = ?", self.codProducto.get_text())
        modelo.clear()

        cursorCodProducto = self.cursor.execute("select * from productos")

        for codProducto in cursorCodProducto:
            modelo.append(codProducto)

        self.baseDatos.commit()

    def on_btnLimpiar_clicked(self, punteiro, modelo):
        """
        Función que borra el contenido de los campos de texto
        :param punteiro:
        :param modelo:
        :return:
        """
        self.codProducto.set_text("")
        self.nombre.set_text("")
        self.descripcion.set_text("")
        self.precio.set_text("")
        self.cantidad.set_text("")

    def on_btnModificar_clicked(self, punteiro, modelo):
        """
        Función que actualiza los datos en el treeview y en la base de datos
        :param punteiro:
        :param modelo: modelo de la tabla
        :return:
        """
        self.cursor.execute("update productos set codProducto = ?, nombre = ?, descripcion = ?, precio = ?, cantidad = ? where codProducto = ?", (self.codProducto.get_text(), self.nombre.get_text(), self.descripcion.get_text(),float(self.precio.get_text()), int(self.cantidad.get_text()), self.codProducto.get_text()))

        modelo.clear()

        cursorCodProducto = self.cursor.execute("select * from productos")

        for codProducto in cursorCodProducto:
            modelo.append(codProducto)

        self.baseDatos.commit()




if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()
