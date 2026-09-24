# Semana-5-y-6
Colecciones, Genéricos, Interfaz Gráfica y Manejo de Eventos
# Catálogo de productos - Tienda de Abastos

Proyecto de Python que integra los contenidos de las semanas 5 y 6: colecciones, operaciones CRUD, interfaz gráfica y manejo de eventos.

## Funcionalidades

- Agregar, buscar, listar, actualizar y eliminar productos.
- Evitar IDs y nombres duplicados.
- Validar ID, nombre, precio y stock.
- Seleccionar una fila de la tabla para cargar los datos en el formulario.
- Mostrar mensajes de confirmación y error.

## Colecciones utilizadas

- `list`: conserva los productos y permite recorrerlos.
- `dict`: relaciona el ID con el objeto `Producto` para realizar búsquedas.
- `set`: mantiene los IDs registrados y permite detectar duplicados.

## Requisitos

- Python 3.10 o superior.
- Flet.

## Instalación y ejecución

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python -m pip install -r requirements.txt
python main.py
```

También puedes ejecutar la aplicación con el comando de Flet:

```bash
flet run main.py
```

## Uso

1. Completa ID, nombre, precio y stock.
2. Pulsa **Agregar** para registrar el producto.
3. Escribe un ID o parte del nombre en el campo de búsqueda y pulsa **Buscar**.
4. Pulsa **Listar todos** para volver a mostrar el catálogo completo.
5. Para actualizar, carga el producto mediante la búsqueda o selecciónalo en la tabla, modifica sus datos y pulsa **Actualizar**.
6. Para eliminar, carga el producto y pulsa **Eliminar**.

## Nota

Los productos se almacenan en memoria mientras la aplicación está abierta. Al cerrar la aplicación, los datos se reinician. El enunciado no exige persistencia en archivos o base de datos.
