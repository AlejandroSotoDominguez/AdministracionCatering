Servicio de Catering
********************

Administración de la base de datos
==================================

Menús de gestión
++++++++++++++++
 * Gestión Clientes
 * Gestión Productos


Tablas de la base de datos:
===========================

Tabla Clientes
++++++++++++++

+------------+------------+------------+------------+------------+-----------------+
| CodCliente |   Nombre   | Apellidos  |  Teléfono  |  Dirección |      Email      |
+============+============+============+============+============+=================+
|     1      |   Daniel   |   Otero    |  666443322 |  García B. | daniel@gmail.com|
+------------+------------+------------+------------+------------+-----------------+
|     2      |   Pedro    |  Martínez  |  666557788 |  Travesía  | pedro@gmail.com |
+------------+------------+------------+------------+------------+-----------------+
|     3      |   Borja    |   Pérez    |  663445577 |   Urzaiz   | borja@gmail.com |
+------------+------------+------------+------------+------------+-----------------+

Tabla Productos
+++++++++++++++

+------------+------------+------------+------------+------------+
|CodProducto |   Nombre   |Descripción |   Precio   |  Cantidad  | 
+============+============+============+============+============+
|     1      |   Lubina   |  pescados  |    10,00   |     10     |
+------------+------------+------------+------------+------------+
|     2      |    Agua    |   bebidas  |    1,20    |     25     |
+------------+------------+------------+------------+------------+
|     3      |  Milanesa  |   carnes   |    12,00   |     12     |
+------------+------------+------------+------------+------------+


Tabla Pedidos
+++++++++++++

+------------+------------+------------+------------+------------+
| CodPedido  | CodCliente |CodProducto |   Precio   |  Cantidad  | 
+============+============+============+============+============+
|     1      |     1      |     1      |     20     |     10     |
+------------+------------+------------+------------+------------+
|     2      |     2      |     2      |     50     |     25     |
+------------+------------+------------+------------+------------+


Funcionamiento
++++++++++++++

La aplicación se inicia con un menú en el que elegiremos si queremos acceder a la administración de clientes o de productos.

En ambas secciones se cargaran las tablas de la base de datos permitiéndonos modificar registros, añadir nuevos y borrarlos.

Además desde el menú del cliente podremos generar un listado de clientes y una factura.









