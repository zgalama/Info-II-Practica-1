class Jugador:
    def __init__(self, nom) -> None:
        self.nombre = nom
        self.oponente = Jugador
        self.equipo = list()
        self.informe = str
    def anadir_oponente(self, opo):
        self.oponente = opo
    def anadir_personanjes(self, lista_de_personajes: list):
        for personaje in lista_de_personajes:
            self.equipo.append(personaje)

class Personaje:
    def __init__(self) -> None:
        self.vida_maxima = int
        self.vida_actual = int
        self.danyo = int
        self.posicion = str
        self.enfriamiento_restante = int
        self.equipo = list()
    def mover(self, pos: str):
        self.posicion = pos

class Medico(Personaje):
    def __init__(self) -> None:
        super().__init__()
    def habilidad(self, objetivo: Personaje):
        objetivo.vida_actual = objetivo.vida_maxima

class Inteligencia(Personaje):
    def __init__(self) -> None:
        super().__init__()

    def habilidad(self, posicion : str):
        letras_casillas = ('a', 'b', 'c', 'd')
        numeros_casillas = ('1', '2', '3', '4')

        casillas_exploradas = [posicion]

        for letra in letras_casillas:
            if letra == posicion[0]:
                for numero in numeros_casillas:
                    if numero == posicion[1]:
                        idx_letra = letras_casillas.index(letra)
                        idx_numero = numeros_casillas.index(numero)
                        try:
                            cas2 = letras_casillas[idx_letra + 1] + numero
                            cas3 = letra + numeros_casillas[idx_numero + 1]
                            cas4 = letras_casillas[idx_letra + 1] + numeros_casillas[idx_numero + 1]
                            casillas_exploradas.extend([cas2, cas3, cas4])
                            return casillas_exploradas #-- Lista con las casillas a explorar, return de control. Modificar para interactuar.
                        except:
                            error = print('La ubicacion seleccionada no es valida para un area 2x2')
                            return error








