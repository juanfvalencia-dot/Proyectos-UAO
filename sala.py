from asientovip import asientovip
from asientomedium import asientomedium
from asientobasic import asientobasic


class sala:
    def __init__(self, nombre, filas, columnas, pelicula, horarios):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.pelicula = pelicula
        self.horarios = horarios
        self.asientos = []
        self.posiciones = {}
        self.crear_asientos()

    def crear_asientos(self):
        self.asientos = []
        self.posiciones = {}
        
        f = self.filas
        c = self.columnas

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        i = 0
        while i < f:
            fila = []
            j = 0
            while j < c:

                if i < f // 3:
                    a = asientovip(i, j)
                elif i < (2 * f) // 3:
                    a = asientomedium(i, j)
                else:
                    a = asientobasic(i, j)

                fila.append(a)

                codigo = letras[i] + str(j + 1)
                self.posiciones[codigo] = (i, j)

                j += 1

            self.asientos.append(fila)
            i += 1   
    
    def mostrar_salasimple(self):
        ancho = 60 

        print("\n")
        print(f"--- MAPA {self.nombre.upper()} ---".center(ancho))
        print("\n")

        for fila in self.asientos:
            linea = ""  

            for a in fila:
                linea += a.mostrar_simple()

            print(linea.center(ancho))  

        print("\n")
        print("Pantalla".center(ancho))

    def mostrar_sala(self):
        ancho = 60

        print("\n")
        print(f"Sala: {self.nombre} | Película: {self.pelicula}".center(ancho))
        print("\n")

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        f = self.filas

        i = 0
        for fila in self.asientos:

            #PASILLO ENTRE TIPOS 
            if i == f // 3 or i == (2 * f) // 3:
                print(" " * 5 + "═" * (ancho - 10))  # línea elegante

            linea = letras[i] + " "

            j = 0
            for a in fila:
                codigo = letras[i] + str(j + 1)
                linea += a.mostrar_detallado(codigo)

                #PASILLOS LATERALES
                if j == 0 or j == self.columnas - 2:
                    linea += " | "
                else:
                    linea += " "

                j += 1

            print(linea.center(ancho))
            i += 1

        print("\n")
        print("Pantalla".center(ancho))
        print("\n")
        print("V=VIP | M=MEDIUM | B=BASIC | X=OCUPADO".center(ancho))
        print("\n")
                
    def calcular_precio(self, a):
        return a.precio()

    def vender_asiento(self, fila, columna):
        a = self.asientos[fila][columna]

        a.ocupar()
        return True

    def vender_por_codigo(self, codigo):
        codigo = codigo.upper()

        if codigo not in self.posiciones:
            return None

        fila, col = self.posiciones[codigo]
        a = self.asientos[fila][col]

        if a.get_ocupado():
            return None

        precio = self.calcular_precio(a)
        a.ocupar()
        return precio

    def ocupacion(self):
        ocupados = 0
        total = self.filas * self.columnas

        for fila in self.asientos:
            for a in fila:
                if a.ocupado:
                    ocupados += 1

        return ocupados, total
    
    def liberar_asiento(self, codigo):
        if codigo in self.posiciones:
            i, j = self.posiciones[codigo]
            self.asientos[i][j].desocupar()

    def esta_llena(self):
        for fila in self.asientos:
            for a in fila:
                if not a.get_ocupado():
                    return False
        return True