Este programa permite gestionar el inventario de productos utilizando una base de datos MySQL.

Se va a desplegar un menú por consola el cual tiene diferentes opciones que se eligen.

Las funcionalidades que tiene son:
Agregar productos, modificar productos, eliminar productos, ver todos o uno de los productos,
hacer un reporte de los productos cuya cantidad es igual o inferior al número que el usuario quiera poner como límite,
función para vaciar todo el inventario(Tabla vacía),
y por último tiene la posibilidad de elegir salir del programa en todo momento.

Tiene como requisito:
- Python 3.8 o superior
- Base de datos MySQL en ejecución
- Archivo `.env` con las credenciales de acceso.

Y las siguientes dependencias
-Externas (aclaradas en requeriments.txt):
    cryptography
    PyMySQL
    python-dotenv
    SQLAlchemy
-Internas:
    time
    os