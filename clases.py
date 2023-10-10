class Jugador:
    def __init__(self, nom) -> None:
        self.nombre = nom
        self.oponente = Jugador
        self.equipo = list()
        self.informe = str
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
        self.id = 'Medico'

    def habilidad(self, objetivo: Personaje):
        objetivo.vida_actual = objetivo.vida_maxima
        print('Se ha curado al completo a {}, su salud ahora es {}\n'.format(objetivo.id, objetivo.vida_actual))

class Inteligencia(Personaje):
    def __init__(self) -> None:
        super().__init__()
        self.id = 'Inteligencia'

    def habilidad(self, posicion : str, opo : Jugador):
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
                            casillas_exploradas #-- Lista con las casillas a explorar
                        except:
                            error = print('La ubicacion seleccionada no es valida para un area 2x2\n')
                            return error

        equipo_enemigo = opo.equipo
        avistados = {}

        for (enemigo) in (equipo_enemigo):
            if enemigo.posicion in casillas_exploradas:
                avistados[enemigo.id] = enemigo.posicion

        if not avistados:
            print('No se ha avistado a ningún enemigo\n')
        else:
            print('Se han avistado enemigos: ')
            for ene, pos in avistados.items():
                print(ene, 'en', pos)
            print('\n')

class Francotirador(Personaje):
    def __init__(self):
        super().__init__()
        self.id = 'Francotirador'

    def habilidad(self, posicion : str, opo : Jugador):
        equipo_enemigo = opo.equipo
        for enemigo in equipo_enemigo:
            if enemigo.posicion == posicion:
                enemigo.vida_actual = 0

class Artillero(Personaje):
    def __init__(self):
        super().__init__()
        self.id = 'Artillero'

    def habilidad(self, posicion : str, opo : Jugador):
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
                            casillas_exploradas  # -- Lista con las casillas a explorar
                        except:
                            error = print('La ubicacion seleccionada no es valida para un area 2x2\n')
                            return error

        dañados = {}

        for enemigo in opo.equipo:
            if enemigo.posicion in casillas_exploradas:
                enemigo.vida_actual = enemigo.vida_actual - 1
                dañados[enemigo.id] = enemigo.vida_actual
                print(f'El {enemigo.id} ha sido dañado en {enemigo.posicion}. Vida restante [{enemigo.vida_actual}]')

        if not dañados:
            print('No se ha dañado a ningún enemigo\n')













