class Jugador:
    def __init__(self, nom) -> None:
        self.nombre = nom
        self.oponente = Jugador
        self.equipo = list()
        self.informe = str
    def realizar_accion(self) -> str:
        pass

    def crear_equipo(self):
        M = Medico()
        I = Inteligencia()
        A = Artillero()
        F = Francotirador()
        self.equipo.extend([M,I,A,F])
        M.equipo.extend([I,A,F])
        I.equipo.extend([M,A,F])
        A.equipo.extend([M,I,F])
        F.equipo.extend([M,I,A])
    def posicionar_equipo(self):

        pos_init = []
        valid_pos = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4']

        for personaje in self.equipo:
            pos = input(f'Escriba la posicion inicial de {personaje.id}: ')
            while pos in pos_init or pos not in valid_pos:
                pos = input(f'La casilla no es valida, escoja otra posicion para el {personaje.id}: ')

            pos_init.append(pos)
            personaje.posicion = pos
    def recibir_accion(self, s : str):
        pass

class Personaje:
    def __init__(self) -> None:
        self.vida_maxima = int
        self.vida_actual = int
        self.danyo = int
        self.posicion = str
        self.enfriamiento_restante = int
        self.equipo = list()

    def mover(self):

        tablero = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4']
        pos_ocupadas = []
        pos_actual = self.posicion

        for personaje in self.equipo:
            pos_ocupadas.append(personaje.posicion)
        pos_ocupadas.append(pos_actual)

        while True:
            pos_nueva = input(f'Escribe a la casilla a la que quieres mover {self.id}: ')
            list_pos = list(pos_actual)
            list_npos = list(pos_nueva)

            diff_letter = abs(ord(list_pos[0]) - ord(list_npos[0]))
            diff_number = abs(int(list_pos[1]) - int(list_npos[1]))

            if ((diff_letter == 1 and diff_number == 0) or \
                (diff_letter == 0 and diff_number == 1) or \
                (diff_letter == 1 and diff_number == 1)) and \
                    (pos_nueva not in pos_ocupadas) and (pos_nueva in tablero):
                self.posicion = pos_nueva
                print(f'{self.id} se ha movido a {self.posicion}')
                break
            else:
                print(f'La casilla no es válida')


class Medico(Personaje):
    def __init__(self) -> None:
        super().__init__()
        self.id = 'Medico'
        self.vida_maxima = 1
        self.vida_actual = 1

    def habilidad(self, objetivo: Personaje):
        objetivo.vida_actual = objetivo.vida_maxima
        print('Se ha curado al completo a {}, su salud ahora es {}\n'.format(objetivo.id, objetivo.vida_actual))

class Inteligencia(Personaje):
    def __init__(self) -> None:
        super().__init__()
        self.id = 'Inteligencia'
        self.vida_maxima = 2
        self.vida_actual = 2

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
        self.vida_maxima = 3
        self.vida_actual = 3

    def habilidad(self, posicion : str, opo : Jugador):
        equipo_enemigo = opo.equipo
        for enemigo in equipo_enemigo:
            if enemigo.posicion == posicion:
                enemigo.vida_actual = 0

class Artillero(Personaje):
    def __init__(self):
        super().__init__()
        self.id = 'Artillero'
        self.vida_maxima = 2
        self.vida_actual = 2

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
















