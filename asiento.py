class asiento:
    def __init__(self, fila, columna):
        self.__fila = fila
        self.__columna = columna
        self.__ocupado = False
        self.__precio_base = 10000

    def get_precio_base(self):
        return self.__precio_base
    
    def get_ocupado(self):
        return self.__ocupado
    
    def get_fila(self):
        return self.__fila
    
    def get_columna(self):
        return self.__columna
    
    def ocupar(self):
        self.__ocupado = True

    def multiplicador(self):
        k = 1
        return k

    def desocupar(self):   
        self.__ocupado = False

    def precio(self):
        r = self.__precio_base * self.multiplicador()
        return r

    def tipo(self):
        return " "

    def mostrar_simple(self):
        if self.__ocupado:
            m = "[X]"
            return m
        l = "[ ]"
        return l

    def mostrar_detallado(self, codigo):
        if self.__ocupado:
            x = "[X]"
            return x
        c = f"[{self.tipo()}-{codigo}]"
        return c