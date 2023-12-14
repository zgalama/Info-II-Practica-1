class Nodo:
    def __init__(self, dato, next):
        self.dato = dato
        self.next = next

class Cola:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def vacia(self):
        return self.first is None and self.last is None

    def peek(self):
        if self.vacia():
            return None

        return self.first.dato

    def mostrar(self):
        actual = self.first
        while actual is not None:
            print(actual.dato, end= " - ")
            actual = actual.next
        print("")

    def buscar(self,dato):
        actual = self.first
        while actual is not None:
            if actual.dato == dato:
                return True
            actual = actual.next
        return False

    def encolar(self, dato):
        nodo = Nodo(dato, None)

        if self.vacia():
            self.first = nodo
            self.last = nodo
        else:
            self.last.next = nodo
            self.last = nodo

        self.size += 1

    def desencolar(self):
        sacar = self.first
        if self.vacia():
            return sacar
        elif self.size == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next

        self.size -= 1
        return sacar.dato