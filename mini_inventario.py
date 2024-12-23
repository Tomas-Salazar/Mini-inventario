import time


def agregar_producto(inventario):
    while True:
            nuevo_producto = input('¿Qué artículo desea añadir al inventario? ').strip().capitalize()
            if not nuevo_producto:      # Si no introdujo nuevo producto, se lo vuelve a pedir
                print("El nombre del producto no puede estar vacío.")
                continue
            elif not inventario:    # Si inventario está vacío, no me interesa el siguiente condicional
                pass
            
            for producto in inventario.values():
                if producto["nombre"].lower() == nuevo_producto.lower():    # Revisa en el inventario que no exista ya el producto
                    print('El producto ya existe en el inventario.')
                    
            descripcion_nuevo_producto = input('Introduzca una breve descripción del artículo: \n')
            if not descripcion_nuevo_producto:
                descripcion_nuevo_producto = ''
            
            try:
                cantidad_nuevo_producto = int(input('¿Cuántos artículos añade del nuevo producto? '))
                if cantidad_nuevo_producto <= 0:    # Evalúa que no se introduzca número negativo
                    print("La cantidad debe ser un número positivo.")
                    continue
            except ValueError:
                print('Ingrese un número válido para la cantidad.')
                continue
            
            try:
                precio_nuevo_producto = float(input('Ingrese el precio del nuevo producto: '))
                if precio_nuevo_producto <= 0:  # Evalúa que no se introduzca un precio negativo
                    print("El precio debe ser un número positivo.")
                    continue
            except ValueError:
                print('Ingrese un número válido para el precio.')
                continue
            
            categoria_nuevo_producto = input('Ingrese la categoría del nuevo producto: ').strip().capitalize()
            if not categoria_nuevo_producto:
                print("La categoría no puede estar vacía.")
                continue
            
            break
        
    if nuevo_producto:  # Verifico que no esté vacío
        nuevo_id = max(inventario.keys(), default=0) + 1    # Ésto lo realizo debido a que no fue implementado SQL.
        inventario[nuevo_id] = {    # Agrega el nuevo producto al inventario
            "nombre": nuevo_producto,
            "descripcion": descripcion_nuevo_producto,
            "cantidad": cantidad_nuevo_producto,
            "precio": precio_nuevo_producto,
            "categoria": categoria_nuevo_producto
        }
    
    return inventario


def mostrar_productos(inventario):
    if not inventario:
        print('No hay ningún producto registrado.')
    else:
        for id_producto, datos in inventario.items():
            print(f'\nID: {id_producto}\nNombre: {datos["nombre"]}\nDescripción: {datos["descripcion"]}\n'
                f'Cantidad: {datos["cantidad"]}\nPrecio: ${datos["precio"]:.2f}\nCategoría: {datos["categoria"]}')


def pedir_codigo_producto(accion):  # Se añade ésta función para mejorar la legibilidad y modularidad
    while True:
        try:
            codigo_producto = int(input(f'Introduzca el código del producto a {accion}: '))
            return codigo_producto
        except ValueError:
            print('Ingrese un número válido para la búsqueda.\n')


def verificar_codigo_producto(codigo, inventario):  # Se añade ésta función para mejorar la legibilidad y modularidad
    if codigo:
        lista_codigos_inventario = list(inventario.keys())
        if codigo not in lista_codigos_inventario:
            print('El código introducido no se encuentra en el inventario')
            return False
        return True


def menu_actualizar():  # Se añade ésta función para mejorar la legibilidad y modularidad
    menu = """
¿Qué quiere modificar del producto?
Nombre
Descripción
Cantidad
Precio
Categoría
"""
    print(menu)


def actualizar_producto(inventario):
    codigo = pedir_codigo_producto(accion='actualizar')
    
    verificacion_codigo = verificar_codigo_producto(codigo, inventario)
    if not verificacion_codigo:
        return inventario
        
    while True:
        menu_actualizar()
        opcion = input('Elija una opción: ').strip().lower()
        
        # Menú de opciones
        if opcion == 'nombre':  
            nuevo_nombre = input('Escriba el nuevo nombre del producto: ').capitalize()
            if nuevo_nombre:    # No se utiliza método get() ya que ya nos aseguramos que existan
                inventario[codigo]['nombre'] = nuevo_nombre    # Sobreescribe por el nuevo nombre.
                break
            else:
                print('El nombre no puede estar vacío.')
            
        elif opcion in ['descripción', 'descripcion']:
            nueva_descripcion = input('Escriba la nueva descripción del producto: ')
            if nueva_descripcion:
                inventario[codigo]['descripcion'] = nueva_descripcion    # Sobreescribe por la nueva cantidad
                break
            
        elif opcion == 'cantidad':
            try:
                nueva_cantidad = int(input('Escriba la nueva cantidad del producto: '))
                if nueva_cantidad >= 0:
                    inventario[codigo]['cantidad'] = nueva_cantidad    # Sobreescribe por la nueva cantidad
                    break
                else:
                    print('La cantidad no puede ser negativa.')
            except ValueError:
                print('Ingrese un número válido.')
            
        elif opcion == 'precio':
            try:
                nuevo_precio = round(float(input('Escriba el nuevo precio del producto: ')), 2)
                if nuevo_precio > 0:
                    inventario[codigo]['precio'] = nuevo_precio    # Sobreescribe por el nuevo precio
                    break
                else:
                    print('El precio debe ser mayor a 0.')
            except ValueError:
                print('Ingrese un número válido.')
                
        elif opcion in ['categoría', 'categoria']:
            nueva_categoria = input('Escriba la nueva categoría del producto: ').capitalize()
            if nueva_categoria:
                inventario[codigo]['categoria'] = nueva_categoria    # Sobreescribe por la nueva categoria
                break
            else:
                print('La categoría no puede estar vacía.')
                
        else:
            print('Elija una opción disponible.')       # Ataja cualquier otra respuesta que no esté dentro de las opciones
            
    return inventario


def eliminar_producto(inventario):
    codigo = pedir_codigo_producto(accion='eliminar')
    
    verificacion_codigo = verificar_codigo_producto(codigo, inventario)
    if not verificacion_codigo:
        return inventario
    
    inventario.pop(codigo)  # Ya fue chequeado previamente que la key exista
    
    return inventario


def buscar_producto(inventario):
    codigo = pedir_codigo_producto(accion='ver')
    
    verificacion_codigo = verificar_codigo_producto(codigo, inventario)
    if not verificacion_codigo:
        return inventario
    
    producto = inventario.get(codigo)
    
    print("\nDetalles del producto:")
    print(f"  ID: {codigo}")
    print(f"  Nombre: {producto['nombre']}")
    print(f"  Descripción: {producto['descripcion']}")
    print(f"  Cantidad: {producto['cantidad']}")
    print(f"  Precio: ${producto['precio']:.2f}")
    print(f"  Categoría: {producto['categoria']}")
    
    return producto


def reporte_bajo_stock(inventario):
    while True:
        try:
            cantidad_limite_bajo = int(input(f'Introduzca el limite de stock: '))
            if cantidad_limite_bajo <= 0:    # Evalúa que no se introduzca número negativo
                print("La cantidad debe ser un número positivo.")
                continue
            break
        except ValueError:
            print('Ingrese un número válido.')
            continue
    
    for id_producto, datos in inventario.items():
        if datos['cantidad'] <= cantidad_limite_bajo:
            nombre = datos['nombre']
            cantidad = datos['cantidad']
            print(f'\nEl producto {nombre}(ID: {id_producto}) se encuentra bajo de stock, con {cantidad} unidades.')


def vaciar_inventario(inventario):
    while True:
        respuesta = input('Se está por eliminar completamente el inventario, ¿está de acuerdo?\n').strip().lower()
        if respuesta == 'no':
            print('No se ha eliminado nada.')
            return inventario
        elif respuesta == 'si':
            inventario.clear()
            return inventario
        else:
            'Escriba por si o por no.'


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
    inventario = {
    1: {"nombre": "Manzana", "descripcion": "Fruta fresca", "cantidad": 50, "precio": 0.5, "categoria": "Frutas"},
    2: {"nombre": "Pan", "descripcion": "Pan casero", "cantidad": 20, "precio": 1.0, "categoria": "Panadería"},
    3: {"nombre": "Leche", "descripcion": "Leche entera 1L", "cantidad": 30, "precio": 1.2, "categoria": "Lácteos"},
    4: {"nombre": "Yogur", "descripcion": "Yogur natural", "cantidad": 25, "precio": 0.8, "categoria": "Lácteos"},
    5: {"nombre": "Cereal", "descripcion": "Cereal integral 500g", "cantidad": 15, "precio": 2.5, "categoria": "Desayunos"},
    6: {"nombre": "Huevos", "descripcion": "Docena de huevos", "cantidad": 10, "precio": 1.5, "categoria": "Proteínas"},
    7: {"nombre": "Arroz", "descripcion": "Arroz blanco 1kg", "cantidad": 40, "precio": 1.0, "categoria": "Granos"},
    8: {"nombre": "Lentejas", "descripcion": "Lentejas secas 1kg", "cantidad": 35, "precio": 1.8, "categoria": "Granos"},
    9: {"nombre": "Zanahoria", "descripcion": "Zanahoria fresca", "cantidad": 60, "precio": 0.3, "categoria": "Verduras"},
    10: {"nombre": "Tomate", "descripcion": "Tomate maduro", "cantidad": 50, "precio": 0.4, "categoria": "Verduras"},
    11: {"nombre": "Pasta", "descripcion": "Spaghetti 500g", "cantidad": 20, "precio": 1.2, "categoria": "Pastas"},
    12: {"nombre": "Salsa de Tomate", "descripcion": "Salsa de tomate 500g", "cantidad": 25, "precio": 1.5, "categoria": "Salsas"},
    13: {"nombre": "Aceite de Oliva", "descripcion": "Aceite extra virgen 1L", "cantidad": 10, "precio": 5.0, "categoria": "Aceites"},
    14: {"nombre": "Azúcar", "descripcion": "Azúcar blanca 1kg", "cantidad": 30, "precio": 1.0, "categoria": "Dulces"},
    15: {"nombre": "Sal", "descripcion": "Sal refinada 1kg", "cantidad": 40, "precio": 0.5, "categoria": "Condimentos"},
    16: {"nombre": "Pimienta", "descripcion": "Pimienta negra 100g", "cantidad": 20, "precio": 1.2, "categoria": "Condimentos"},
    17: {"nombre": "Chocolate", "descripcion": "Barra de chocolate 100g", "cantidad": 30, "precio": 1.5, "categoria": "Dulces"},
    18: {"nombre": "Té", "descripcion": "Caja de té 20 sobres", "cantidad": 15, "precio": 2.0, "categoria": "Bebidas"},
    19: {"nombre": "Café", "descripcion": "Café molido 250g", "cantidad": 20, "precio": 3.0, "categoria": "Bebidas"},
    20: {"nombre": "Refresco", "descripcion": "Refresco 2L", "cantidad": 50, "precio": 1.8, "categoria": "Bebidas"}
    }
    
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
            inventario = agregar_producto(inventario)
            
        elif opcion == 2:
            # Mostrar los productos
            mostrar_productos(inventario)
            
        elif opcion == 3:
            # Ver un producto
            buscar_producto(inventario)
            
        elif opcion == 4:
            # Modificar un producto
            actualizar_producto(inventario)
            
        elif opcion == 5:
            # Eliminar un producto
            eliminar_producto(inventario)
            
        elif opcion == 6:
            # Reportar stock
            reporte_bajo_stock(inventario)
            
        elif opcion == 7:
            # Vaciar el inventario
            inventario = vaciar_inventario(inventario)
            
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

# Evita ejecución del script automática al importar el módulo
if __name__ == '__main__':
    main()