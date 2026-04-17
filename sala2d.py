from sala import sala

class sala2d(sala):
    def __init__(self, nombre, filas, columnas, pelicula, horarios):
        super().__init__(nombre, filas, columnas, pelicula, horarios)
        self.__tipo = "2d"
        self.__recarga = 0

    def get_recarga(self):
        return self.__recarga
    
    def get_tipo(self):
        return self.__tipo.upper()
    
    def calcular_precio(self, a):
        cal = super().calcular_precio(a) + self.__recarga

        if a.tipo() != "V":
            cal += 1000
        return cal
    
