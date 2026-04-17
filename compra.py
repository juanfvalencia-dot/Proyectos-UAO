class compra:
    def __init__(self, numero, cliente, sala, pelicula, horario, asiento, precio):
        self.__numero = numero
        self.__cliente = cliente
        self.__sala = sala
        self.__pelicula = pelicula
        self.__horario = horario
        self.__asiento = asiento
        self.__precio = precio

    def get_numero(self):
        return self.__numero
    
    def get_cliente(self):
        return self.__cliente
    
    def get_sala(self):
        return self.__sala
    
    def get_pelicula(self):
        return self.__pelicula
    
    def get_horario(self):
        return self.__horario
    
    def get_asiento(self):
        return self.__asiento
    
    def get_precio(self):
        return self.__precio
