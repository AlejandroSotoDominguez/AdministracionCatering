import os

import gi

gi.require_version("Gtk",'3.0')
from gi.repository import Gtk

class FiestraPrincipal(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Administración Catering")

        caja = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.add(caja)
        lblTitulo = Gtk.Label(label="Elige una opción", xalign=0.5)
        caja.pack_start(lblTitulo, True, True, 0)

        self.opcionCombo = 0

        modelo = Gtk.ListStore(str, str)
        modelo.append(["1", "Gestor de Clientes"])
        modelo.append(["2", "Gestor de Productos"])

        cmbPersoa = Gtk.ComboBox.new_with_model_and_entry(modelo)
        cmbPersoa.connect("changed", self.on_cmbPersoa_changed, self.opcionCombo)
        cmbPersoa.set_entry_text_column(1)
        caja.pack_start(cmbPersoa, False, False, 0)

        btnAceptar = Gtk.Button(label="Aceptar")
        caja.pack_start(btnAceptar, True, False, 0)
        btnAceptar.connect("clicked", self.on_btnAceptar_clicked, self.opcionCombo)

        btnSalir = Gtk.Button(label="Salir")
        caja.pack_start(btnSalir, True, False, 0)
        btnSalir.connect("clicked", self.on_btnSalir_clicked)



        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_btnClientes_clicked(self, btnClientes):
        cmd = os.path.join(os.getcwd(), "GestionClientes.py")
        os.system('{} {}'.format('python', cmd))

    def on_btnProductos_clicked(self, btnProductos):
        cmd = os.path.join(os.getcwd(), "GestionProductos.py")
        os.system('{} {}'.format('python', cmd))


    def on_btnSalir_clicked(self, btnSalir):
        ventana = Gtk.Window
        ventana.destroy(self)

    def on_cmbPersoa_changed(self, combo, opcionCombo):
        punteiro = combo.get_active_iter()
        modelo = combo.get_model()
        if punteiro is not None:
            id, menu = modelo[punteiro][:2]
            if id == "1":
                self.opcionCombo = 1
            else:
                self.opcionCombo = 2

    def on_btnAceptar_clicked(self, combo, opcionCombo):
        if self.opcionCombo == 1:
            cmd = os.path.join(os.getcwd(), "GestionClientes.py")
            os.system('{} {}'.format('python', cmd))
        else:
            cmd = os.path.join(os.getcwd(), "GestionProductos.py")
            os.system('{} {}'.format('python', cmd))




if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()
