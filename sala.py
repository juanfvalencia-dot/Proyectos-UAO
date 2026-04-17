from asientovip import asientovip
from asientomedium import asientomedium
from asientobasic import asientobasic


class sala:
    def __init__(self, nombre, filas, columnas, pelicula, horarios):
        self.__nombre = nombre
        self.__filas = filas
        self.__columnas = columnas
        self.__pelicula = pelicula
        self.__horarios = horarios
        self.__asientos = []
        self.__posiciones = {}

    def get_nombre(self):
        return self.__nombre
    
    def get_filas(self):
        return self.__filas

    def get_columnas(self):
        return self.__columnas

    def get_pelicula(self):
        return self.__pelicula

    def get_horarios(self):
        return self.__horarios

    def get_asientos(self):
        return self.__asientos

    def get_posiciones(self):
        return self.__posiciones

    def calcular_precio(self, a):
        return a.precio()

    def vender_asiento(self, fila, columna):
        a = self.__asientos[fila][columna]

        a.ocupar()
        return True

    def vender_por_codigo(self, codigo):
        codigo = codigo.upper()

        if codigo not in self.__posiciones:
            return None

        fila, col = self.__posiciones[codigo]
        a = self.__asientos[fila][col]

        if a.get_ocupado():
            return None

        precio = self.calcular_precio(a)
        a.ocupar()
        return precio

    def ocupacion(self):
        ocupados = 0
        total = self.__filas * self.__columnas

        for fila in self.__asientos:
            for a in fila:
                if a.ocupado:
                    ocupados += 1

        return ocupados, total
    
    def liberar_asiento(self, codigo):
        if codigo in self.__posiciones:
            i, j = self.__posiciones[codigo]
            self.__asientos[i][j].desocupar()

    def esta_llena(self):
        for fila in self.__asientos:
            for a in fila:
                if not a.get_ocupado():
                    return False
        return True