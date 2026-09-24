import flet as ft


# ============================================================
# SEMANA 5: CLASE PRODUCTO Y COLECCIONES
# ============================================================

class Producto:
    """Representa un producto de la tienda de abastos."""

    def __init__(self, id_producto: int, nombre: str, precio: float, stock: int):
        self.__id_producto = id_producto
        self.__nombre = nombre.strip()
        self.__precio = precio
        self.__stock = stock

    @property
    def id_producto(self):
        return self.__id_producto

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    @property
    def stock(self):
        return self.__stock

    def actualizar_datos(self, nombre: str, precio: float, stock: int):
        self.__nombre = nombre.strip()
        self.__precio = precio
        self.__stock = stock


class Catalogo:
    """Administra productos usando list, dict y set."""

    def __init__(self):
        self.productos = []             # list: conserva y recorre productos
        self.productos_por_id = {}      # dict: relaciona ID con objeto Producto
        self.ids_registrados = set()    # set: evita IDs duplicados

    def agregar(self, producto: Producto):
        if producto.id_producto in self.ids_registrados:
            raise ValueError("Ya existe un producto con ese ID.")
        if any(p.nombre.casefold() == producto.nombre.casefold()
               for p in self.productos):
            raise ValueError("Ya existe un producto con ese nombre.")

        self.productos.append(producto)
        self.productos_por_id[producto.id_producto] = producto
        self.ids_registrados.add(producto.id_producto)

    def buscar(self, criterio: str):
        criterio = criterio.strip()
        if not criterio:
            return None

        # Primero intenta buscar por ID; si no es numérico, busca por nombre.
        if criterio.isdigit():
            return self.productos_por_id.get(int(criterio))

        criterio = criterio.casefold()
        for producto in self.productos:
            if criterio in producto.nombre.casefold():
                return producto
        return None

    def listar(self):
        return list(self.productos)

    def actualizar(self, id_producto: int, nombre: str, precio: float, stock: int):
        producto = self.productos_por_id.get(id_producto)
        if producto is None:
            raise ValueError("No se encontró un producto con ese ID.")

        nombre_normalizado = nombre.strip().casefold()
        for otro in self.productos:
            if otro.id_producto != id_producto and otro.nombre.casefold() == nombre_normalizado:
                raise ValueError("Otro producto ya utiliza ese nombre.")

        producto.actualizar_datos(nombre, precio, stock)

    def eliminar(self, id_producto: int):
        producto = self.productos_por_id.get(id_producto)
        if producto is None:
            raise ValueError("No se encontró un producto con ese ID.")

        self.productos.remove(producto)
        del self.productos_por_id[id_producto]
        self.ids_registrados.remove(id_producto)


# ============================================================
# SEMANA 6: INTERFAZ GRÁFICA FLET Y MANEJO DE EVENTOS
# ============================================================

def main(page: ft.Page):
    page.title = "Catálogo de productos - Tienda de Abastos"
    page.window_width = 1050
    page.window_height = 760
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    catalogo = Catalogo()
    producto_seleccionado = {"id": None}

    campo_id = ft.TextField(label="ID del producto", width=220,
                            keyboard_type=ft.KeyboardType.NUMBER)
    campo_nombre = ft.TextField(label="Nombre del producto", width=300)
    campo_precio = ft.TextField(label="Precio ($)", width=180,
                                keyboard_type=ft.KeyboardType.NUMBER)
    campo_stock = ft.TextField(label="Stock", width=180,
                               keyboard_type=ft.KeyboardType.NUMBER)
    campo_busqueda = ft.TextField(label="Buscar por ID o nombre", expand=True)

    mensaje = ft.Text()
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio ($)")),
            ft.DataColumn(ft.Text("Stock")),
        ],
        rows=[],
        column_spacing=35,
    )

    def mostrar_mensaje(texto, error=False):
        mensaje.value = texto
        mensaje.color = ft.Colors.RED if error else ft.Colors.GREEN
        page.update()

    def leer_campos():
        id_texto = (campo_id.value or "").strip()
        nombre = (campo_nombre.value or "").strip()
        precio_texto = (campo_precio.value or "").strip().replace(",", ".")
        stock_texto = (campo_stock.value or "").strip()

        if not id_texto or not nombre or not precio_texto or not stock_texto:
            raise ValueError("Completa todos los campos.")

        try:
            id_producto = int(id_texto)
            precio = float(precio_texto)
            stock = int(stock_texto)
        except ValueError:
            raise ValueError("ID y stock deben ser enteros; el precio debe ser numérico.")

        if id_producto <= 0:
            raise ValueError("El ID debe ser un número entero mayor que cero.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        return id_producto, nombre, precio, stock

    def refrescar_tabla(lista=None):
        productos = catalogo.listar() if lista is None else lista
        tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(p.id_producto))),
                    ft.DataCell(ft.Text(p.nombre)),
                    ft.DataCell(ft.Text(f"{p.precio:.2f}")),
                    ft.DataCell(ft.Text(str(p.stock))),
                ],
                on_select_change=lambda e, pid=p.id_producto: seleccionar_producto(pid),
            )
            for p in productos
        ]
        page.update()

    def limpiar_campos(e=None):
        campo_id.value = ""
        campo_nombre.value = ""
        campo_precio.value = ""
        campo_stock.value = ""
        producto_seleccionado["id"] = None
        mostrar_mensaje("Campos limpiados.")

    def seleccionar_producto(id_producto):
        producto = catalogo.productos_por_id.get(id_producto)
        if producto:
            campo_id.value = str(producto.id_producto)
            campo_nombre.value = producto.nombre
            campo_precio.value = str(producto.precio)
            campo_stock.value = str(producto.stock)
            producto_seleccionado["id"] = producto.id_producto
            mostrar_mensaje(f"Producto {producto.nombre} seleccionado. Puedes actualizarlo o eliminarlo.")

    def agregar_producto(e):
        try:
            id_producto, nombre, precio, stock = leer_campos()
            catalogo.agregar(Producto(id_producto, nombre, precio, stock))
            refrescar_tabla()
            limpiar_campos()
            mostrar_mensaje("Producto agregado correctamente.")
        except ValueError as error:
            mostrar_mensaje(str(error), True)

    def buscar_producto(e):
        criterio = (campo_busqueda.value or "").strip()
        if not criterio:
            refrescar_tabla()
            mostrar_mensaje("Escribe un ID o nombre para buscar.", True)
            return
        producto = catalogo.buscar(criterio)
        if producto:
            refrescar_tabla([producto])
            seleccionar_producto(producto.id_producto)
            mostrar_mensaje("Producto encontrado.")
        else:
            refrescar_tabla([])
            mostrar_mensaje("No se encontró ningún producto.", True)

    def listar_productos(e):
        campo_busqueda.value = ""
        refrescar_tabla()
        mostrar_mensaje(f"Se muestran {len(catalogo.productos)} producto(s).")

    def actualizar_producto(e):
        try:
            id_producto, nombre, precio, stock = leer_campos()
            catalogo.actualizar(id_producto, nombre, precio, stock)
            refrescar_tabla()
            mostrar_mensaje("Producto actualizado correctamente.")
        except ValueError as error:
            mostrar_mensaje(str(error), True)

    def eliminar_producto(e):
        try:
            id_texto = (campo_id.value or "").strip()
            if not id_texto:
                raise ValueError("Ingresa el ID del producto que deseas eliminar.")
            id_producto = int(id_texto)
            catalogo.eliminar(id_producto)
            refrescar_tabla()
            limpiar_campos()
            mostrar_mensaje("Producto eliminado correctamente.")
        except ValueError as error:
            mostrar_mensaje(str(error), True)

    encabezado = ft.Text(
        "CATÁLOGO DE PRODUCTOS\nTienda de Abastos",
        size=26,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    formulario = ft.Column(
        controls=[
            ft.Text("Datos del producto", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([campo_id, campo_nombre], wrap=True),
            ft.Row([campo_precio, campo_stock], wrap=True),
            ft.Row(
                [
                    ft.FilledButton("Agregar", icon=ft.Icons.ADD, on_click=agregar_producto),
                    ft.FilledButton("Actualizar", icon=ft.Icons.EDIT, on_click=actualizar_producto),
                    ft.FilledButton("Eliminar", icon=ft.Icons.DELETE, on_click=eliminar_producto),
                    ft.OutlinedButton("Limpiar", icon=ft.Icons.CLEAR, on_click=limpiar_campos),
                ],
                wrap=True,
            ),
        ],
        spacing=12,
    )

    busqueda = ft.Row(
    controls=[
        ft.Container(
            content=campo_busqueda,
            width=450,
        ),
        ft.FilledButton(
            "Buscar",
            icon=ft.Icons.SEARCH,
            on_click=buscar_producto,
        ),
        ft.OutlinedButton(
            "Listar todos",
            icon=ft.Icons.LIST,
            on_click=listar_productos,
        ),
    ],
    alignment=ft.MainAxisAlignment.START,
    vertical_alignment=ft.CrossAxisAlignment.CENTER,
    wrap=True,
)

    page.add(
        ft.Column(
            controls=[
                encabezado,
                ft.Divider(),
                formulario,
                ft.Divider(),
                ft.Text("Consulta de productos", size=18, weight=ft.FontWeight.BOLD),
                busqueda,
                mensaje,
                ft.Row([tabla], scroll=ft.ScrollMode.AUTO),
                ft.Text(
                    "Consejo: selecciona una fila de la tabla para cargar sus datos en el formulario.",
                    size=12,
                    italic=True,
                ),
            ],
            spacing=15,
        )
    )
    refrescar_tabla()


if __name__ == "__main__":
    ft.run(main)
