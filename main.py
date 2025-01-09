import time
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def agregar_producto(engine):
    while True:
            # Solicita el nombre del producto
            nuevo_producto = input('¿Qué artículo desea añadir al inventario? ').strip().capitalize()
            if not nuevo_producto:      # Si no introdujo nuevo producto, se lo vuelve a pedir
                print("El nombre del producto no puede estar vacío.")
                continue
            
            # Verifica si el producto ya existe en la base de datos
            query_verificacion = text("""
                SELECT COUNT(*) FROM emprendimiento_prueba WHERE Nombre_Producto = :nombre
            """)
            with engine.begin() as conn:
                resultado = conn.execute(query_verificacion, {'nombre': nuevo_producto}).scalar()
            
            if resultado > 0:  # Si el producto ya existe, se lo vuelve a pedir
                print(f"El producto '{nuevo_producto}' ya existe en el inventario. Intente con otro producto.")
                continue
            
            # Solicita la descripción del producto
            descripcion_nuevo_producto = input('Introduzca una breve descripción del artículo: \n')
            if not descripcion_nuevo_producto:
                descripcion_nuevo_producto = None
            
            # Solicita la cantidad del producto
            try:
                cantidad_nuevo_producto = int(input('¿Cuántos artículos añade del nuevo producto? '))
                if cantidad_nuevo_producto <= 0:    # Evalúa que no se introduzca número negativo
                    print("La cantidad debe ser un número positivo.")
                    continue
            except ValueError:
                print('Ingrese un número válido para la cantidad.')
                continue
            
            # Solicita el precio del producto
            try:
                precio_nuevo_producto = float(input('Ingrese el precio del nuevo producto.\nSi es un número decimal, utilice punto (.) como separador: $'))
                if precio_nuevo_producto <= 0:  # Evalúa que no se introduzca un precio negativo
                    print("El precio debe ser un número positivo.")
                    continue
            except ValueError:
                print('Ingrese un número válido para el precio.')
                continue
            
            # Solicita la categoría del producto
            categoria_nuevo_producto = input('Ingrese la categoría del nuevo producto: ').capitalize()
            if not categoria_nuevo_producto:
                print("La categoría no puede estar vacía.")
                continue
            
            break
        
    # Se añade el nuevo producto al inventario
    query = text("""
        INSERT INTO emprendimiento_prueba(Nombre_Producto, Descripcion, Cantidad_Stock, Precio_Producto, Categoria)
        VALUES(:nombre, :descripcion, :cantidad, :precio, :categoria)
    """)
    
    with engine.begin() as conn:  # begin() es parahacer commit automáticamente
        conn.execute(query, {
            'nombre': nuevo_producto,
            'descripcion': descripcion_nuevo_producto,
            'cantidad': cantidad_nuevo_producto,
            'precio': precio_nuevo_producto,
            'categoria': categoria_nuevo_producto
        })
        
        print(f'Producto [{nuevo_producto}] agregado correctamente.')
        
    return engine


def mostrar_productos(engine):
    query = text("""SELECT * FROM emprendimiento_prueba""")
    
    with engine.begin() as conn:
        productos = conn.execute(query)
        
        print("\nInventario actual:")
        
        for producto in productos:
            print(f"\n  ID: {producto[0]}")
            print(f"  Nombre: {producto[1]}")
            print(f"  Descripción: {producto[2]}")
            print(f"  Cantidad: {producto[3]}")
            print(f"  Precio: ${producto[4]:.2f}")
            print(f"  Categoría: {producto[5]}")


def pedir_codigo_producto(accion):  # Se añade ésta función para mejorar la legibilidad y modularidad
    while True:
        try:
            codigo_producto = int(input(f'Introduzca el código del producto a {accion}: '))
            return codigo_producto
        except ValueError:
            print('Ingrese un número válido para la búsqueda.\n')



def buscar_producto(engine):
    producto_id = pedir_codigo_producto(accion='ver')
    
    query = text("SELECT * FROM emprendimiento_prueba WHERE Producto_ID = :id")
    
    with engine.begin() as conn:
        resultado = conn.execute(query, {'id': producto_id}).fetchone() # fetchone() devuelve una sola fila
    
    if not resultado:
        print('El producto no se encuentra en el inventario.')
        return
    
    print("\nDetalles del producto:")
    print(f"  ID: {resultado[0]}")
    print(f"  Nombre: {resultado[1]}")
    print(f"  Descripción: {resultado[2]}")
    print(f"  Cantidad: {resultado[3]}")
    print(f"  Precio: ${resultado[4]:.2f}")
    print(f"  Categoría: {resultado[5]}")
    
    return resultado


def menu_actualizar():  # Se añade ésta función para mejorar la legibilidad y modularidad
    menu = """
¿Qué quiere modificar del producto?
1. Nombre
2. Descripción
3. Cantidad
4. Precio
5. Categoría
6. Salir
"""
    print(menu)


def actualizar_producto(engine):
    # Pido el ID del producto a modificar
    codigo = pedir_codigo_producto(accion='actualizar')
    
    # Verifica si el producto existe
    query_verificacion = text("SELECT * FROM emprendimiento_prueba WHERE Producto_ID = :codigo")
    
    with engine.begin() as conn:
        producto = conn.execute(query_verificacion, {'codigo': codigo}).fetchone()
    
    if not producto:
        print("El producto no se encuentra en el inventario.")
        return
        
    # Hago el bucle para que el usuario pueda elegir qué modificar
    while True:
        menu_actualizar()
        opcion = input('Elija una opción: ').strip()
        
        # Menú de opciones
        if opcion == '1':
            nuevo_nombre = input("Escriba el nuevo nombre del producto: ").strip().capitalize()
            if nuevo_nombre:
                query_actualizar = text("UPDATE emprendimiento_prueba SET Nombre_Producto = :nuevo_nombre WHERE Producto_ID = :codigo")
                with engine.begin() as conn:
                    conn.execute(query_actualizar, {'nuevo_nombre': nuevo_nombre, 'codigo': codigo})
                print("Nombre actualizado correctamente.")
                break
            else:
                print("El nombre no puede estar vacío.")
        
        elif opcion == '2':
            nueva_descripcion = input("Escriba la nueva descripción del producto: ").strip()
            if nueva_descripcion:
                query_actualizar = text("UPDATE emprendimiento_prueba SET Descripcion = :nueva_descripcion WHERE Producto_ID = :codigo")
                with engine.begin() as conn:
                    conn.execute(query_actualizar, {'nueva_descripcion': nueva_descripcion, 'codigo': codigo})
                print("Descripción actualizada correctamente.")
                break
        
        elif opcion == '3':
            try:
                nueva_cantidad = int(input("Escriba la nueva cantidad del producto: "))
                if nueva_cantidad >= 0:
                    query_actualizar = text("UPDATE emprendimiento_prueba SET Cantidad_Stock = :nueva_cantidad WHERE Producto_ID = :codigo")
                    with engine.begin() as conn:
                        conn.execute(query_actualizar, {'nueva_cantidad': nueva_cantidad, 'codigo': codigo})
                    print("Cantidad actualizada correctamente.")
                    break
                else:
                    print("La cantidad no puede ser negativa.")
            except ValueError:
                print("Ingrese un número válido.")
        
        elif opcion == '4':
            try:
                nuevo_precio = float(input("Escriba el nuevo precio del producto: "))
                if nuevo_precio > 0:
                    query_actualizar = text("UPDATE emprendimiento_prueba SET Precio_Producto = :nuevo_precio WHERE Producto_ID = :codigo")
                    with engine.begin() as conn:
                        conn.execute(query_actualizar, {'nuevo_precio': nuevo_precio, 'codigo': codigo})
                    print("Precio actualizado correctamente.")
                    break
                else:
                    print("El precio debe ser mayor a 0.")
            except ValueError:
                print("Ingrese un número válido.")
        
        elif opcion == '5':
            nueva_categoria = input("Escriba la nueva categoría del producto: ").strip().capitalize()
            if nueva_categoria:
                query_actualizar = text("UPDATE emprendimiento_prueba SET Categoria = :nueva_categoria WHERE Producto_ID = :codigo")
                with engine.begin() as conn:
                    conn.execute(query_actualizar, {'nueva_categoria': nueva_categoria, 'codigo': codigo})
                print("Categoría actualizada correctamente.")
                break
            else:
                print("La categoría no puede estar vacía.")
        
        elif opcion == '6':
            print("Saliendo del menú de actualización.")
            break
    return


def eliminar_producto(engine):
    # Pido el ID del producto a modificar
    codigo = pedir_codigo_producto(accion='eliminar')
    
    # Verifica si el producto existe
    verificacion = text("SELECT * FROM emprendimiento_prueba WHERE Producto_ID = :codigo")
    
    with engine.begin() as conn:
        producto = conn.execute(verificacion, {'codigo': codigo}).fetchone()
    
    if not producto:
        print("El producto no se encuentra en el inventario.")
        return
    
    query_delete = text("DELETE FROM emprendimiento_prueba WHERE Producto_ID = :codigo")
    with engine.begin() as conn:
                    conn.execute(query_delete, {'codigo': codigo})
                    print("Producto eliminado correctamente.")
    return


def reporte_bajo_stock(engine):
    while True:
        try:
            # Solicitar el límite de stock bajo
            cantidad_limite_bajo = int(input("Introduzca el límite de stock: "))
            if cantidad_limite_bajo <= 0:  # Asegurarse de que el número sea positivo
                print("La cantidad debe ser un número positivo.")
                continue
            break
        except ValueError:
            print("Ingrese un número válido.")
    
    # Consulta para obtener productos con stock bajo
    query_stock_bajo = text("""
        SELECT Producto_ID, Nombre_Producto, Cantidad_Stock
        FROM emprendimiento_prueba 
        WHERE Cantidad_Stock <= :cantidad_limite
    """)
    
    with engine.begin() as conn:
        productos_bajo_stock = conn.execute(query_stock_bajo, {'cantidad_limite': cantidad_limite_bajo}).fetchall()
    
    # Mostrar los productos con stock bajo
    if productos_bajo_stock:
        print("\nProductos con stock bajo:")
        for producto in productos_bajo_stock:
            producto_id, nombre, cantidad = producto
            print(f"- Producto {nombre} (ID: {producto_id}) tiene {cantidad} unidades.")
    else:
        print("\nNo hay productos con stock bajo para el límite especificado.")
    return


def vaciar_inventario(engine):
    while True:
        respuesta = input('Se está por eliminar completamente el inventario, ¿está de acuerdo? (si/no): ').strip().lower()
        if respuesta == 'no':
            print('No se ha eliminado nada.')
            return
        elif respuesta == 'si':
            # Confirmar eliminación completa del inventario
            query_delete_all = text("DELETE FROM emprendimiento_prueba")
            
            with engine.begin() as conn:
                conn.execute(query_delete_all)
                print('El inventario ha sido vaciado completamente.')
            return
        else:
            print('Por favor, escriba "si" o "no".')


def mostrar_menu():  # Se añade ésta función para mejorar la legibilidad y modularidad
    menu = """
Seleccione la opción que quiera realizar:
Opción 1: Agregar productos al inventario
Opción 2: Ver los productos del inventario
Opción 3: Ver un producto del inventario
Opción 4: Modificar algún producto del inventario
Opción 5: Elimina algún producto del inventario
Opción 6: Reportar stock bajo de unidades
Opción 7: Vaciar el inventario
Opción 8: Salir
"""
    print(menu)


def main():
    # Carga variables de entorno
    load_dotenv()
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    # Conexión a DB
    connection_string = f'mysql+pymysql://{username}:{password}@{server}/{database}'
    engine = create_engine(connection_string)
    
    # Inicio de programa
    opcion = None
    
    while not opcion:
        mostrar_menu()
        
        # Ingreso de opción por parte del usuario
        try:        # El try evalúa únicamente que el valor pueda convertirse a int, si es numérico pero no está en opciones, vuelve a pedir nueva opción
            opcion = int(input('Opción: '))
        except ValueError:
            print('Elija una opción disponible.') 
            opcion = None
            continue
        
        # Menú de opciones
        if opcion == 1:
            # Agregar producto
            agregar_producto(engine)
            
        elif opcion == 2:
            # Mostrar los productos
            mostrar_productos(engine)
            
        elif opcion == 3:
            # Ver un producto
            buscar_producto(engine)
            
        elif opcion == 4:
            # Modificar un producto
            actualizar_producto(engine)
            
        elif opcion == 5:
            # Eliminar un producto
            eliminar_producto(engine)
            
        elif opcion == 6:
            # Reportar stock
            reporte_bajo_stock(engine)
            
        elif opcion == 7:
            # Vaciar el inventario
            vaciar_inventario(engine)
            
        elif opcion == 8:
            # Salida del programa sin utilizar exit() (1)
            print('Usted ha finalizado la ejecución.\n¡Hasta pronto!\n')
            time.sleep(3)
            break
            
        else:
            print('Elija una opción disponible.')       # Ataja cualquier otra respuesta que no esté dentro de las opciones
            opcion = None
            continue
        
        # Consulta de confirmación de continuidad al usuario
        continuar = None
        while not continuar:
            continuar = input('\n¿Desea continuar? Responda si o no: ').lower().strip()
            if continuar == 'no':
                # Salida del programa sin utilizar exit() (2)
                print('Usted ha finalizado la ejecución.\n¡Hasta pronto!\n')
                time.sleep(3)
            elif continuar == 'si':
                opcion = None
            else:
                print('Intente escribir sólamente si o no.\n')      # Atrapa respuestas que no sean derivados de si o no
                continuar = None
    # Fin del programa

# Evita ejecución del script automática al importar el módulo
if __name__ == '__main__':
    main()