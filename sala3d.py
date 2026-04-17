from sala import sala

class sala3d(sala):
    def __init__(self, nombre, filas, columnas, pelicula, horarios):
        super().__init__(nombre, filas, columnas, pelicula, horarios)
        self.__tipo = "3d"
        self.__recarga = 10000
        self.__gafas = 3500

    def get_recarga(self):
        return self.__recarga
    
    def get_gafas(self):
        return self.__gafas
    
    def get_tipo(self):
        return self.__tipo.upper()


    def calcular_precio(self, a):
        base = super().calcular_precio(a)
        cal = base + self.__recarga

        # VIP no paga gafas
        if a.tipo() != "V":
            cal += self.__gafas

        return cal
