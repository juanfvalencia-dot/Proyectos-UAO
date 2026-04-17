from sala2d import sala2d
from sala3d import sala3d
from compra import compra
from admin import admin
from usuario import usuario
from asiento import asiento
from funcion import funcion


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

def cartelera(funciones):
    ancho = 60
    print("\n")
    print("--- CARTELERA ---".center(ancho))
    print("\n")

    # PEDIR DÍA
    dia_busqueda = input("Ingrese el día (ej: Lunes) o 'Volver': ")
    print("\n")

    # NORMALIZAR TEXTO
    dia_busqueda = dia_busqueda.replace(" ", "")
    dia_busqueda = unicodedata.normalize('NFD', dia_busqueda)
    dia_busqueda = ''.join(c for c in dia_busqueda if unicodedata.category(c) != 'Mn')

    if dia_busqueda.lower() == "volver":
        return {}

    funciones_dia = []

    # FILTRAR Y PREPARAR ORDEN
    for f in funciones:
        if f.get_dia().lower() == dia_busqueda.lower():
            hora = int(f.get_horario().replace(":", ""))

            # 🔥 AJUSTE PARA MADRUGADA
            if hora < 600:
                hora += 2400

            funciones_dia.append((hora, f))

    # ORDENAR POR HORA
    funciones_dia.sort(key=lambda x: x[0])

    id_funcion = 101
    mapa = {}
    encontrado = False

    # IMPRIMIR
    for _, f in funciones_dia:
        s = f.get_sala()

        print(f"ID: {id_funcion} | {f.get_pelicula()} | Hora: {f.get_horario()} | Sala: {s.get_tipo()}".center(ancho))

        mapa[id_funcion] = f
        id_funcion += 1
        encontrado = True

    if not encontrado:
        print("\nNo hay funciones para ese día\n")

    return mapa

def carteleraconcompra(funciones, compras, usulista):
    usu = usulista

    cartelera(funciones)
    print("\n")
    opc = input("Desea comprar(Comprar) o volver al menu(Volver): ")

    opc = opc.replace(" ", "")
    opc = unicodedata.normalize('NFD', opc)
    opc = ''.join(c for c in opc if unicodedata.category(c) != 'Mn')

    if opc.lower() == "comprar":
        limpiarrapido()
        titulo()
        entradas(funciones, compras, usu)
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

def mostrar_factura(compra, funcion, cliente_obj=None):
    ancho = 60
    print("\n")
    print(("="*40).center(ancho))
    print("FACTURA GRAN CINEMA".center(ancho))
    print(("="*40).center(ancho))

    print(f"Factura #: {compra.get_numero()}".center(ancho))
    print(f"Cliente: {compra.get_cliente()}".center(ancho))

    # NIVEL DE USUARIO
    if cliente_obj and not isinstance(cliente_obj, str):
        print(f"Nivel: {cliente_obj.nivel()}".center(ancho))

    print(f"Película: {compra.get_pelicula()}".center(ancho))
    print(f"Sala: {funcion.get_sala().get_nombre()}".center(ancho))
    print(f"Hora: {compra.get_horario()}".center(ancho))
    
    # 🔥 NUEVO (DÍA)
    print(f"Día: {funcion.get_dia()}".center(ancho))

    print(f"Asiento: {compra.get_asiento()}".center(ancho))

    print(("-"*40).center(ancho))

    # USAR FUNCION (NO SALA)
    fila, col = funcion.get_posiciones()[compra.get_asiento()]
    a = funcion.get_asientos()[fila][col]

    sala = funcion.get_sala()

    if sala.get_tipo() == "2d" and a.tipo() == "V":
        print("Beneficio VIP: Servicio de comida incluida".center(ancho))

    base = a.precio()
    total = base

    print(f"Precio asiento: ${int(base)}".center(ancho))

    if sala.get_tipo() == "3d":
        recarga = sala.get_recarga()
        gafas = sala.get_gafas()

        print(f"Recargo 3D: ${recarga}".center(ancho))
        total += recarga

        if a.tipo() == "V":
            print("gafas 3D: $0 (incluidas en VIP)".center(ancho))
        else:
            print(f"gafas 3D: ${gafas}".center(ancho))
            total += gafas

    print(("-"*40).center(ancho))
    print(f"TOTAL: ${int(total)}".center(ancho))
    print(("="*40).center(ancho))

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

def mostrar_sala_funcion(f):
    ancho = 60
    print("\n")
    print(f"{f.get_pelicula()} | {f.get_dia()} | {f.get_horario()}".center(ancho))
    print("\n")

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    asientos = f.get_asientos()

    for i, fila in enumerate(asientos):
        linea = letras[i] + " "
        for j, a in enumerate(fila):
            codigo = letras[i] + str(j + 1)
            linea += a.mostrar_detallado(codigo) + " "
        print(linea.center(ancho))

    print("\n")
    print("Pantalla".center(ancho))

def entradas(funciones, compras, usu_lista):
    lista_usuarios = usu_lista

    mapa = cartelera(funciones)
    if not mapa:
        return

    f = seleccionar_funcion(mapa)
    if f is None:
        return

    sala = f.get_sala()
    horario = f.get_horario()
    pelicula = f.get_pelicula()

    limpiarrapido()
    titulo()

    mostrar_sala_funcion(f)

    while True:
        try:
            print("\n")
            codigo = input("Asiento (ej: A3, o digite 'Volver'): ")

            codigo = codigo.replace(" ", "")
            codigo = unicodedata.normalize('NFD', codigo)
            codigo = ''.join(c for c in codigo if unicodedata.category(c) != 'Mn')
            codigo = codigo.upper()

            if codigo.lower() == "volver":
                return

            if codigo not in f.get_posiciones():
                print("Asiento no existe")
                continue

            fila, col = f.get_posiciones()[codigo]
            a = f.get_asientos()[fila][col]

            if a.get_ocupado():
                print("Asiento ocupado")
                continue

            precio = a.precio()
            a.ocupar()

            break

        except:
            print("Error, ingrese asiento valido")

    cliente = obtener_cliente(lista_usuarios)

    if cliente is None:
        a.desocupar()
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

    if not isinstance(cliente, str):
        cliente = cliente.get_nombre()

    c = compra(numero, cliente, sala.get_nombre(), pelicula, horario, codigo, precio)
    compras.append(c)

    limpiarrapido()
    titulo()
    mostrar_factura(c, f, cli)

    if isinstance(cli, usuario):
        cli.fidelidad(sala.get_tipo())

    while True:
        opc = input("\nIngrese (si) para seguir explorando: ")
        opc = opc.replace(" ", "")
        opc = unicodedata.normalize('NFD', opc)
        opc = ''.join(c for c in opc if unicodedata.category(c) != 'Mn')

        if opc.lower() == "si":
            break

def modificar_usuario(lista_usuarios):

    print("\n--- MODIFICAR USUARIO ---\n")

    nombre = input("Ingrese el nombre del usuario a modificar (o 'volver'): ")

    # normalizar
    nombre = nombre.replace(" ", "")
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')

    if nombre.lower() == "volver":
        return

    usuario_encontrado = None

    # buscar usuario
    for u in lista_usuarios:
        if u.get_nombre().lower() == nombre.lower():
            usuario_encontrado = u
            break

    if usuario_encontrado is None:
        print("\nUsuario no encontrado")
        time.sleep(2)
        return

    print("\nUsuario encontrado ✔\n")

    # NUEVOS DATOS
    nuevo_nombre = input("Nuevo nombre (enter para no cambiar): ")
    nueva_cedula = input("Nueva cédula (enter para no cambiar): ")
    nuevo_telefono = input("Nuevo teléfono (enter para no cambiar): ")

    # VALIDACIONES + CAMBIOS

    if nuevo_nombre != "":
        if len(nuevo_nombre.strip()) > 1:
            usuario_encontrado.set_nombre(nuevo_nombre)
        else:
            print("Nombre inválido (mínimo 2 caracteres)")

    if nueva_cedula != "":
        if len(nueva_cedula.strip()) > 1:
            usuario_encontrado.set_cedula(nueva_cedula)
        else:
            print("Cédula inválida")

    if nuevo_telefono != "":
        if len(nuevo_telefono.strip()) > 1:
            usuario_encontrado.set_telefono(nuevo_telefono)
        else:
            print("Teléfono inválido")

    print("\nUsuario actualizado correctamente")
    time.sleep(2)

def buscar_factura(compras, funciones):
    print("\n")
    while True:
        try:
            num = input("Número de factura ( O digite 'Volver'): ")
            num = num.replace(" ", "")
            num = unicodedata.normalize('NFD', num)
            num = ''.join(c for c in num if unicodedata.category(c) != 'Mn')

            if num.lower() == "volver":
                return
            
            num = int(num)
            break

        except:
            print("Inválido")
            continue
    
    limpiarrapido()
    titulo()

    for c in compras:
        if c.get_numero() == num:

            #buscar la función correcta
            for f in funciones:
                if (f.get_sala().get_nombre() == c.get_sala() and 
                    f.get_horario() == c.get_horario() and
                    f.get_pelicula() == c.get_pelicula()):

                    mostrar_factura(c, f)
                    continuar()
                    return

    print("Factura no encontrada")

def mostrar_sala_simple_funcion(f):
    ancho = 60
    print("\n")
    print(f"{f.get_pelicula()} | {f.get_dia()} | {f.get_horario()}".center(ancho))
    print("\n")

    asientos = f.get_asientos()

    for fila in asientos:
        linea = ""
        for a in fila:
            linea += a.mostrar_simple() 
        print(linea.center(ancho))

    print("\n")
    print("Pantalla".center(ancho))

def cancelar(compras, funciones):
    cancelado = True

    while cancelado:
        try:
            limpiarrapido()
            titulo()
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

                #buscar la función correcta
                funcion_encontrada = None
                for f in funciones:
                    if (f.get_sala().get_nombre() == c.get_sala() and 
                        f.get_horario() == c.get_horario() and
                        f.get_pelicula() == c.get_pelicula()):

                        funcion_encontrada = f
                        break

                # mostrar factura
                mostrar_factura(c, funcion_encontrada)

                while True:
                    opcion = input("\n¿Esta es la factura correcta? (si/no/volver): ").lower()

                    opcion = opcion.replace(" ", "")
                    opcion = unicodedata.normalize('NFD', opcion)
                    opcion = ''.join(c for c in opcion if unicodedata.category(c) != 'Mn')

                    if opcion == "si":
                        #liberar asiento en FUNCION (no sala)
                        fila, col = funcion_encontrada.get_posiciones()[c.get_asiento()]
                        funcion_encontrada.get_asientos()[fila][col].desocupar()

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

        if not encontrada:
            print("Factura no encontrada")
            time.sleep(1)

def crear_usuario(lista):
    listau = lista
    while True:
            while True:
                try:
                    limpiarrapido()
                    titulo()
                    ancho = 60
                    print("\n")
                    print("--- REGISTRO DE AFILIACIÓN ---".center(ancho))
                    nombre = input("Usuario: ")
                    if len(nombre) > 0:
                        break
                    print("Ingrese un nombre de usuario valido")
                    time.sleep(3)
                except:
                    continue

            nombre = nombre.replace(" ", "")
            nombre = unicodedata.normalize('NFD', nombre)
            nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')

            existe = False

            for u in listau:
                if u.get_nombre() == nombre:
                    print("Usuario ya registrado")
                    time.sleep(3)
                    existe = True

            if not existe:
                break
    while True:
        cedula = input("Cédula: ")
        if len(cedula) > 0:
            break

        print("Ingrese un numero de cedula valido") 

        continue

    while True:
        telefono = input("Teléfono: ")
        if len(telefono) > 0:
            break

        print("Ingrese un numero de telfono valido") 

        continue

    puntos = 0
    c = usuario(nombre, cedula, telefono, puntos)
    listau.append(c)


    print("\n¡Registro exitoso! Ahora eres parte de Gran Cinema.")
    time.sleep(2)

def disponibilidadsala(funciones):

    mapa = cartelera(funciones)

    if not mapa:
        return

    while True:
        try:
            f = seleccionar_funcion(mapa)  

            if f:
                limpiarrapido()
                titulo()

                mostrar_sala_simple_funcion(f)  

                continuar()
                break
            else:
                break
        except:
            pass

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

    peliculas = [
            "Avengers",
            "Batman",
            "Spiderman",
            "Interstellar",
            "Joker",
            "Titanic",
            "Inception",
            "Fast & Furious"
        ]
    
    salas_lista = [
            sala2d("Sala 1", 5, 5, "", ""),
            sala2d("Sala 2", 5, 5, "", ""),
            sala3d("Sala 3", 5, 5, "", ""),
            sala3d("Sala 4", 5, 5, "", "")
        ]
    
    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
    horas = ["12:00","15:00","18:00","21:00","23:00","09:00"]

    funciones = []

    listausuarios = [
                usuario("Samuel2x", "1109190", "32123221", 220000),
                usuario("LauraIn","1029322","305313420", 120000),
                usuario("BreynerPRO","11112","31734322", 5000)
        ]
    
    datos = cargar_datos(ruta)

    compras = datos.get("compras", [])
    lista_usuarios = datos.get("usuarios", [])
    funciones = datos.get("funciones", [])

    if len(funciones) == 0:
        for dia in dias:
            for s in salas_lista:
                for hora in horas:
                    pelicula_random = random.choice(peliculas)
                    funciones.append(funcion(s, pelicula_random, hora, dia))


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
        print("8. Modificar usuario afiliado".center(ancho))
        print("9. Guardar y salir".center(ancho))

        op = input("\nDigite la opcion elegida: ")
        op = op.replace(" ", "")

        if op == "1":
            limpiar()
            titulo()
            carteleraconcompra(funciones, compras, listausuarios)
            limpiarrapido()
        elif op == "2":
            limpiar()
            titulo()
            disponibilidadsala(funciones)
            limpiarrapido()
        elif op == "3":
            limpiar()
            titulo()
            entradas(funciones, compras, listausuarios)
            limpiarrapido()
        elif op == "4":
            limpiar()
            titulo()
            buscar_factura(compras, funciones)
            limpiarrapido()
        elif op == "5":
            limpiar()
            titulo()
            cancelar(compras, funciones)
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
            modificar_usuario(listausuarios)
            limpiarrapido()
        elif op == "9":
            limpiar()
            titulo()
            print("Guardando y cerrando...")
            datos = {
                "compras": compras,
                "usuarios": lista_usuarios,
                "funciones": funciones
            }
            guardar_datos(ruta, datos)
            break
        else:
            print("Inválido")
            limpiar()

if __name__ == "__main__":
    main()