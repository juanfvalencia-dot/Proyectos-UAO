class funcion:
    def __init__(self, sala, pelicula, horario, dia):
        self.__sala = sala
        self.__pelicula = pelicula
        self.__horario = horario
        self.__dia = dia
        self.__asientos = []
        self.__posiciones = {}
        self.crear_asientos()

    def crear_asientos(self):
        self.__asientos = []
        self.__posiciones = {}

        filas = self.__sala.get_filas()
        columnas = self.__sala.get_columnas()

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for i in range(filas):
            fila = []
            for j in range(columnas):

                # MISMA LÓGICA DE SALA
                if i < filas // 3:
                    from asientovip import asientovip
                    a = asientovip(i, j)
                elif i < (2 * filas) // 3:
                    from asientomedium import asientomedium
                    a = asientomedium(i, j)
                else:
                    from asientobasic import asientobasic
                    a = asientobasic(i, j)

                fila.append(a)

                codigo = letras[i] + str(j + 1)
                self.__posiciones[codigo] = (i, j)

            self.__asientos.append(fila)

    def get_sala(self):
        return self.__sala
    
    def get_pelicula(self):
        return self.__pelicula
    
    def get_horario(self):
        return self.__horario
    
    def get_dia(self):
        return self.__dia

    def get_asientos(self):
        return self.__asientos
    
    def get_posiciones(self):
        return self.__posiciones