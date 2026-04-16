from sala2d import sala2d
from sala3d import sala3d
from compra import compra
from admin import admin
from usuario import usuario
from asiento import asiento


import random
import time
import os
import pickle
import unicodedata

def limpiarrapido():
    os.system("cls" if os.name == "nt" else "clear")

def limpiar():
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")

def limpiarlento():
    time.sleep(8)
    os.system("cls" if os.name == "nt" else "clear")

def cartelera(salas):
    ancho = 60
    print("\n")
    print("--- CARTELERA ---".center(ancho))
    print("\n")

    funciones = []

    for s in salas:
        if not s.esta_llena():  
            funciones.append((s.horarios, s))

    #ordena correctamente (formato 24h)
    funciones.sort()

    id_funcion = 101
    mapa = {}

    for f in funciones:
        hora = f[0]
        s = f[1]

        print(f"ID: {id_funcion} | {s.pelicula} | Hora: {s.horarios} | Sala: {s.get_tipo()}".center(ancho))

        mapa[id_funcion] = s
        id_funcion += 1

    return mapa

def carteleraconcompra(sala, compra, usulista):
    usu = usulista
    salas_lista = sala
    compras = compra

    cartelera(salas_lista)
    print("\n")
    opc = input("Desea comprar(Comprar) o volver al menu(Volver): ")
    opc = opc.replace(" ", "")
    opc = unicodedata.normalize('NFD', opc)
    opc = ''.join(c for c in opc if unicodedata.category(c) != 'Mn')
    if opc.lower() == "comprar":
        limpiarrapido()
        titulo()
        entradas(salas_lista, compras, usu)
    else:
        return

def seleccionar_funcion(mapa):
    while True:
        try:
            op = input("\nID de función para ver mapa ( O digite 'Volver'): ")
            op = op.replace(" ", "")
            op = unicodedata.normalize('NFD', op)
            op = ''.join(c for c in op if unicodedata.category(c) != 'Mn')
            
            if op.lower() == "volver":
                return None
            
            op = int(op)

            if op not in mapa:
                print("\nID inválido")
                continue  

            return mapa[op]

        except:
            print("\nError, ingrese una opción válida")


#CARGAR DATOS 
def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo) and os.path.getsize(nombre_archivo) > 0:
        try:
            with open(nombre_archivo, "rb") as archivo:
                datos = pickle.load(archivo)
                print("Datos cargados correctamente")
                return datos
        except Exception as e:
            print("Error al cargar:", e)
            return {
                "compras": [],
                "usuarios": []
            }
    else:
        print("Archivo no encontrado, iniciando datos vacíos")
        return {
            "compras": [],
            "usuarios": []
        }


#GUARDAR DATOS 
def guardar_datos(nombre_archivo, datos):
    try:
        carpeta = os.path.dirname(nombre_archivo)

        #Crea la carpeta si la carpeta no existe
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print("Carpeta creada:", carpeta)

        with open(nombre_archivo, "wb") as archivo:
            pickle.dump(datos, archivo)

        print("Datos guardados correctamente")

    except Exception as e:
        print("Error al guardar:", e)

def mostrar_factura(compra, sala, cliente_obj=None):
    ancho = 60
    print("\n")
    print(("="*40).center(ancho))
    print("FACTURA GRAN CINEMA".center(ancho))
    print(("="*40).center(ancho))

    print(f"Factura #: {compra.get_numero()}".center(ancho))
    print(f"Cliente: {compra.get_cliente()}".center(ancho))

    #NIVEL DE USUARIO (SOLO SI ES OBJETO)
    if cliente_obj and not isinstance(cliente_obj, str):
        print(f"Nivel: {cliente_obj.nivel()}".center(ancho))

    print(f"Película: {compra.get_pelicula()}".center(ancho))
    print(f"Sala: {compra.get_sala()}".center(ancho))
    print(f"Hora: {compra.get_horario()}".center(ancho))
    print(f"Asiento: {compra.get_asiento()}".center(ancho))

    print(("-"*40).center(ancho))

    #obtener asiento real
    fila, col = sala.posiciones[compra.get_asiento()]
    a = sala.asientos[fila][col]

    if sala.get_tipo() == "2d" and a.tipo() == "V":
        print("Beneficio VIP: Servicio de comida incluida".center(ancho))

    base = a.precio()
    total = base

    print(f"Precio asiento: ${int(base)}".center(ancho))

    #SOLO si es 3D
    if sala.get_tipo() == "3d":
        recarga = sala.get_recarga()
        gafas = sala.get_gafas()

        print(f"Recargo 3D: ${recarga}".center(ancho))
        total += recarga

        #VIP NO paga gafas
        if a.tipo() == "V":
            print("gafas 3D: $0 (incluidas en VIP)".center(ancho))
        else:
            print(f"gafas 3D: ${gafas}".center(ancho))
            total += gafas

    print(("-"*40).center(ancho))
    print(f"TOTAL: ${int(total)}".center(ancho))
    print(("="*40).center(ancho))

def salas(lista):
    print("\nSalas:\n")
    i = 0
    for s in lista:
        print(f"{i+1}. {s.nombre} ({s.get_tipo}) - {s.pelicula}")
        i += 1

def obtener_cliente(lista_usuarios):
    nombre = input("Usuario (o digite volver): ")

    #limpiar texto
    nombre = nombre.replace(" ", "")
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')

    if nombre.lower() == "volver":
        return None

    #BUSCAR USUARIO EXISTENTE
    for u in lista_usuarios:
        if u.get_nombre().lower() == nombre.lower():
            print("Usuario encontrado")
            return u

    #NO EXISTE
    print("Usuario no encontrado")

    while True:
        try:
            op = input("¿Desea crearlo? (si/no) o seguir como invitado (invitado): ").lower()
            op = op.replace(" ", "")
            op = unicodedata.normalize('NFD', op)
            op = ''.join(c for c in op if unicodedata.category(c) != 'Mn')
            break
        except:
            print("Error, ingrese una opción válida")
            continue

    #CREAR USUARIO
    if op.lower() == "si":
        cedula = input("Cédula: ")
        telefono = input("Teléfono: ")
        puntos = 0 

        nuevo = usuario(nombre, cedula, telefono, puntos)

        lista_usuarios.append(nuevo)

        print("Usuario creado")
        return nuevo
    elif op.lower() == "invitado":
        print("Entrando como invitado")
        return nombre  
    elif op.lower() == "no":
        print("Operación cancelada")
        time.sleep(1)
        return None
        


def entradas(salas, compras, usu_lista):
    lista_usuarios = usu_lista

    mapa = cartelera(salas)

    sala = seleccionar_funcion(mapa)
    if sala is None:
        return
    horario = sala.horarios

    limpiarrapido()
    titulo()

    if sala is None:
        return

    sala.mostrar_sala()
    while True:
        try:  
            codigo = input("Asiento (ej: A3, o digite 'Volver'): ")
            codigo = codigo.replace(" ", "")
            codigo = unicodedata.normalize('NFD', codigo)
            codigo = ''.join(c for c in codigo if unicodedata.category(c) != 'Mn')
            
            codigo = codigo.upper()
            if codigo.lower() == "volver":
                return
            
            if codigo not in sala.posiciones:
                print("Asiento no existe")
                continue
    
            resultado = sala.vender_por_codigo(codigo)

            if resultado is None:
                print("Asiento ocupado")
                continue
            break
        except:
            print("Error, ingrese asiento valido")
            pass

    precio = resultado

    cliente = obtener_cliente(lista_usuarios)

    if cliente is None:
        sala.liberar_asiento(codigo)  
        return
    
    numero = random.randint(1000, 9999)

    existe = True

    while existe:
        numero = random.randint(1000, 9999)
        existe = False
        for c in compras:
            if c.get_numero() == numero:
                existe = True

    cli = cliente

    if isinstance(cliente, str):
        cliente = cliente
    else:
        cliente = cliente.get_nombre()

    c = compra(numero, cliente, sala.nombre, sala.pelicula, horario, codigo.upper(), precio)
    compras.append(c)

    limpiarrapido()
    titulo()
    mostrar_factura(c, sala, cli)

    if isinstance (cliente, usuario):
        if sala.get_tipo == "2D":
            c.fidelidad(sala.get_tipo())
        elif sala.get_tipo == "3D":
            c.fidelidad(sala.get_tipo())

    while True:
        try:
            print("\n")
            opc = input("Ingrese (si) para seguir explorando: ")
            opc = opc.replace(" ", "")
            opc = unicodedata.normalize('NFD', opc)
            opc = ''.join(c for c in opc if unicodedata.category(c) != 'Mn')
            
            if opc.lower() == "si":
                break
        except:
            pass

def obtener_usuario_por_nombre(nombre, lista_usuarios):
    for u in lista_usuarios:
        if u.get_nombre().lower() == nombre.lower():
            return u
    return None

def buscar_factura(compras, salas):
    print("\n")
    while True:
        try:
            num = input("Número de factura ( O digite 'Volver'): ")
            num = num.replace(" ", "")
            num = unicodedata.normalize('NFD', num)
            num = ''.join(c for c in num if unicodedata.category(c) != 'Mn')

            if num.lower() == "volver":
                return

            break
        except:
            print("Inválido")
            continue
    
    num = int(num)
    
    limpiarrapido()
    titulo()

    for c in compras:
        if c.get_numero() == num:

            # encontrar sala
            for s in salas:
                if s.nombre == c.get_sala():
                    mostrar_factura(c, s)
                    continuar()
                    return

    print("Factura no encontrada")


def cancelar(compras, salas):
    cancelado = True

    while cancelado:
        try:
            num = input("\nNúmero de factura a cancelar (O digite 'Volver'): ")
            num = num.replace(" ", "")
            num = unicodedata.normalize('NFD', num)
            num = ''.join(c for c in num if unicodedata.category(c) != 'Mn')
    
            if num.lower() == "volver":
                return
            num = int(num)
        except:
            print("Entrada inválida")
            continue

        encontrada = False

        limpiarrapido()
        titulo()

        for i in range(len(compras)):
            c = compras[i]

            if c.get_numero() == num:
                encontrada = True

                # encontrar sala
                sala_encontrada = None
                for s in salas:
                    if s.nombre == c.get_sala():
                        sala_encontrada = s
                        break

                #mostrar factura
                mostrar_factura(c, sala_encontrada)

                #confirmación
                opcion = input("\n¿Esta es la factura correcta? (si/no/volver): ").lower()
                opcion = opcion.replace(" ", "")
                opcion = unicodedata.normalize('NFD', opcion)
                opcion = ''.join(c for c in opcion if unicodedata.category(c) != 'Mn')
            

                if opcion == "si":
                    sala_encontrada.liberar_asiento(c.get_asiento())
                    compras.pop(i) 
                    print("Compra cancelada")
                    time.sleep(3)
                    cancelado = False
                    return

                elif opcion == "no":
                    print("Intenta con otro número")
                    time.sleep(1)
                    break

                elif opcion == "volver":
                    print("Saliendo...")
                    time.sleep(3)
                    return

                else:
                    print("Respuesta inválida")
                    time.sleep(1)
                    break

        if not encontrada:
            print("Factura no encontrada")
            time.sleep(1)

def crear_usuario(lista):
    listau = lista
    ancho = 60
    print("\n")
    print("--- REGISTRO DE AFILIACIÓN ---".center(ancho))
    while True:
            nombre = input("Usuario: ")
            nombre = nombre.replace(" ", "")
            nombre = unicodedata.normalize('NFD', nombre)
            nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')

            existe = False

            for u in listau:
                if u.get_nombre() == nombre:
                    print("Usuario ya registrado")
                    existe = True

            if not existe:
                break

    cedula = input("Cédula: ")
    telefono = input("Teléfono: ")
    puntos = 0
    c = usuario(nombre, cedula, telefono, puntos)
    listau.append(c)


    print("\n¡Registro exitoso! Ahora eres parte de Gran Cinema.")
    time.sleep(2)

def disponibilidadsala(salaentrada):

    salas_lista = salaentrada

    mapa = cartelera(salas_lista)

    while True:
        try:
            sala = seleccionar_funcion(mapa)
            if sala:
                limpiarrapido()
                titulo()
                sala.mostrar_salasimple()
                continuar()
                break
            else:
                break
        except:
            pass

    limpiarrapido()

def continuar():
    while True:
        try:
            print("\n")
            opc = input("Ingrese (Si) para seguir explorando: ")
            opc = opc.replace(" ", "")
            opc = unicodedata.normalize('NFD', opc)
            opc = ''.join(c for c in opc if unicodedata.category(c) != 'Mn')

            if opc.lower() == "si":
                break
            else:
                continue
        except:
            print("Error, ingrese una opción válida")
    
def reconstruir_salas(compras, salas):
    for c in compras:
        for s in salas:
            if s.nombre == c.get_sala():
                if c.get_asiento() in s.posiciones:
                    fila, col = s.posiciones[c.get_asiento()]
                    s.asientos[fila][col].ocupar()

def titulo():
    ancho = 60
    print("═" * ancho)
    print("Gran Cinema".center(ancho))
    print("═" * ancho)

def ver_facturas(compras):

    intento = input("Contraseña: ")
    intento = intento.replace(" ","")

    a = admin()
    
    if not a.get_contraseña() == intento:
        print("Acceso denegado")
        time.sleep(2)
        return

    print("\n--- FACTURAS REGISTRADAS ---\n")

    if len(compras) == 0:
        print("No hay facturas")
        return

    for c in compras:
        print(f"Factura #: {c.get_numero()}")
    
    continuar()


def main():
    ruta = "datos/datos.pkl"

    limpiar()

    salas_lista = [
            sala2d("Sala 1", 5, 5, "Avengers", "15:00"),
            sala2d("Sala 2", 5, 5, "Avengers", "19:00"),
            sala3d("Sala 3", 5, 5, "Batman", "16:00"),
            sala3d("Sala 4", 5, 5, "Batman", "20:00")
        ]
    
    listausuarios = [
                usuario("Samuel2x", "1109190", "32123221", 220000),
                usuario("LauraIn","1029322","305313420", 120000),
                usuario("BreynerPRO","11112","31734322", 5000)
        ]
    
    datos = cargar_datos(ruta)

    compras = datos.get("compras", [])
    lista_usuarios = datos.get("usuarios", [])

    reconstruir_salas(compras, salas_lista)

    limpiar()

    
    titulo()

    limpiar()
    
    while True:
        
        titulo()
        ancho = 60

        print("\nOpciones:")
        print("1. Cartelera".center(ancho))
        print("2. Disponibilidad".center(ancho))
        print("3. Comprar".center(ancho))
        print("4. Historial".center(ancho))
        print("5. Cancelar".center(ancho))
        print("6. Visualizar como Administrador".center(ancho))
        print("7. Afiliarse a Gran Cinema".center(ancho))
        print("8. Guardar y salir".center(ancho))

        op = input("\nDigite la opcion elegida: ")
        op = op.replace(" ", "")

        if op == "1":
            limpiar()
            titulo()
            carteleraconcompra(salas_lista, compras, listausuarios)
            limpiarrapido()
        elif op == "2":
            limpiar()
            titulo()
            disponibilidadsala(salas_lista)
        elif op == "3":
            limpiar()
            titulo()
            entradas(salas_lista, compras, listausuarios)
            limpiarrapido()
        elif op == "4":
            limpiar()
            titulo()
            buscar_factura(compras, salas_lista)
            limpiarrapido()
        elif op == "5":
            limpiar()
            titulo()
            cancelar(compras, salas_lista)
            limpiarrapido()
        elif op=="6":
            limpiar()
            titulo()
            ver_facturas(compras)
            limpiarrapido()
        elif op == "7":
            limpiar()
            titulo()
            crear_usuario(listausuarios)
            limpiarrapido()
        elif op == "8":
            limpiar()
            titulo()
            print("Guardando y cerrando...")
            datos = {
                    "compras": compras,
                    "usuarios": lista_usuarios
                }
            guardar_datos(ruta, datos)
            break
        else:
            print("Inválido")
            limpiar()

if __name__ == "__main__":
    main()