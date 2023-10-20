from utils import limpiar_terminal, casillas_2x2

tablero = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4']

class Jugador:
    def __init__(self) -> None:
        self.oponente = Jugador
        self.equipo = list()
        self.informe = str

    def turno(self):
        oponentes = []
        for oponente in self.oponente.equipo:
            oponentes.append(oponente.id)
        if 'Artillero' not in oponentes and 'Francotirador' not in oponentes:
            return True
        else:
            return False

    def eliminar_personajes_muertos(self):
        for personaje in self.equipo:
            if personaje.vida_actual == 0:
                self.equipo[self.equipo.index(personaje)] = 0
        self.equipo = [x for x in self.equipo if x!= 0]


    def realizar_accion(self) -> str:

        opciones_personajes = []
        opciones_validas = []

        print('-- SITUACION DEL EQUIPO --\n')

        self.resetear_enfriamiento()

        for personaje in self.equipo:

            if personaje.enfriamiento_restante != 0:
                print(f'El {personaje.id} se encuentra en [{personaje.posicion}] con [Vida: {personaje.vida_actual}/{personaje.vida_maxima}] [Habilidad no disponible]')
            else:
                print(f'El {personaje.id} se encuentra en [{personaje.posicion}] con [Vida: {personaje.vida_actual}/{personaje.vida_maxima}]')


        print('')

        print('-- Selecciona una acción --\n')



        i = 0
        for personaje in self.equipo:

            if personaje.id == 'Medico':
                if personaje.enfriamiento_restante == 0:
                    print(f'{i}: Mover ({personaje.id})')
                    print(f'{i + 1}: Curar a un personaje ({personaje.id})')
                    opciones_personajes.append({i : [personaje.id, 'm']})
                    opciones_personajes.append({i + 1: [personaje.id, 'h']})
                    opciones_validas.append(str(i))
                    opciones_validas.append(str(i + 1))
                    i += 2
                else:
                    print(f'{i}: Mover ({personaje.id})')
                    opciones_personajes.append({i : [personaje.id, 'm']})
                    opciones_validas.append(str(i))
                    i += 1

            if personaje.id == 'Inteligencia':
                if personaje.enfriamiento_restante == 0:
                    print(f'{i}: Mover ({personaje.id})')
                    print(f'{i + 1}: Explorar un área 2x2 ({personaje.id})')
                    opciones_personajes.append({i : [personaje.id, 'm']})
                    opciones_personajes.append({i + 1: [personaje.id, 'h']})
                    opciones_validas.append(str(i))
                    opciones_validas.append(str(i + 1))
                    i += 2
                else:
                    print(f'{i}: Mover ({personaje.id})')
                    opciones_personajes.append({i : [personaje.id, 'm']})
                    opciones_validas.append(str(i))
                    i += 1

            if personaje.id == 'Artillero':
                if personaje.enfriamiento_restante == 0:
                    print(f'{i}: Mover ({personaje.id})')
                    print(f'{i + 1}: Atacar en un area 2x2 ({personaje.id})')
                    opciones_personajes.append({i: [personaje.id, 'm']})
                    opciones_personajes.append({i + 1: [personaje.id, 'h']})
                    opciones_validas.append(str(i))
                    opciones_validas.append(str(i + 1))
                    i += 2
                else:
                    print(f'{i}: Mover ({personaje.id})')
                    opciones_personajes.append({i : [personaje.id, 'm']})
                    opciones_validas.append(str(i))
                    i += 1

            if personaje.id == 'Francotirador':
                if personaje.enfriamiento_restante == 0:
                    print(f'{i}: Mover ({personaje.id})')
                    print(f'{i + 1}: Disparar a una posición ({personaje.id})')
                    opciones_personajes.append({i: [personaje.id, 'm']})
                    opciones_personajes.append({i + 1: [personaje.id, 'h']})
                    opciones_validas.append(str(i))
                    opciones_validas.append(str(i + 1))
                    i += 2
                else:
                    print(f'{i}: Mover ({personaje.id})')
                    opciones_personajes.append({i : [personaje.id, 'm']})
                    opciones_validas.append(str(i))
                    i += 1

        print('')

        num_accion = (input('Selecciona la acción siguiente: '))

        while num_accion not in opciones_validas:
            num_accion = (input('Opcion no válida, introduzca de nuevo la acción: '))

        if num_accion in opciones_validas:
            num_accion = int(num_accion)
            for personaje in self.equipo:
                if personaje.id == opciones_personajes[num_accion][num_accion][0]:
                    if opciones_personajes[num_accion][num_accion][1] == 'm':
                        res = personaje.mover()

                        self.control_de_enfriamiento()
                        return res
                    else:
                        res = personaje.habilidad(self.oponente)

                        self.control_de_enfriamiento()
                        return res

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
            while pos in pos_init or pos not in tablero:
                pos = input(f'La casilla no es valida, escoja otra posicion para el {personaje.id}: ')

            pos_init.append(pos)
            personaje.posicion = pos
    def recibir_accion(self, STR: str):

        self.informe = '-- INFORME DEL TURNO DEL ENEMIGO -- \n'
        self.informe += ''


        if STR == 'move':
            self.informe += 'No se ha registrado actividad enemiga \n'

        STR = list(STR)

        if STR[0] == 'I':
            casillas_afectadas = casillas_2x2(STR)

            for personaje in self.equipo:
                if personaje.posicion in casillas_afectadas:
                    self.informe += f'El enemigo ha avistado a {personaje.id}\n'

        if STR[0] == 'A':
            casillas_afectadas = casillas_2x2(STR)

            for personaje in self.equipo:
                if personaje.posicion in casillas_afectadas:
                    self.informe += f'El enemigo ha dañado a {personaje.id}, [{personaje.vida_actual}/{personaje.vida_maxima}]\n'

        if STR[0] == 'F':
            casilla_puntero = STR[1:]
            casilla = str(casilla_puntero[0]+casilla_puntero[1])

            for personaje in self.equipo:
                if personaje.posicion == casilla:
                    self.informe += f'El enemigo ha abatido a {personaje.id}, [{personaje.vida_actual}/{personaje.vida_maxima}]\n'
    def resetear_enfriamiento(self):
        for personaje in self.equipo:
            if personaje.count == 2:
                personaje.enfriamiento_restante = 0
                personaje.count = 0

    def control_de_enfriamiento(self):
        for personaje in self.equipo:
            if personaje.enfriamiento_restante == 1:
                personaje.count += 1

class Personaje:
    def __init__(self) -> None:
        self.vida_maxima = int
        self.vida_actual = int
        self.posicion = str
        self.enfriamiento_restante = 0
        self.count = 0
        self.equipo = list()
        self.jugador = Jugador

    def mover(self):

        pos_ocupadas = []
        pos_actual = self.posicion

        for personaje in self.equipo:
            pos_ocupadas.append(personaje.posicion)
        pos_ocupadas.append(pos_actual)

        while True:

            pos_nueva = input(f'Escribe a la casilla a la que quieres mover {self.id}: ')
            while pos_nueva == '':
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
                return 'move'
            else:
                print(f'La casilla no es válida')

class Medico(Personaje):
    def __init__(self) -> None:
        super().__init__()
        self.id = 'Medico'
        self.vida_maxima = 1
        self.vida_actual = 1

    def habilidad(self, opo : Jugador):
        opciones_validas = ['M','I','A','F']
        objetivos_a_curar = []
        for objetivo in self.jugador.equipo:
            if objetivo.vida_actual != objetivo.vida_maxima:
                objetivos_a_curar.append(objetivo.id[0])
                print(f'{objetivo.id[0]}: Curar al {objetivo.id}')
        if not objetivos_a_curar:
            print('No hay objetivos a los que curar, perdiste el turno')
            return 'move'

        objetivo = input('A quien quieres curar: ')

        while objetivo not in objetivos_a_curar:
            objetivo = input('Selecciona una opción válida: ')

        for personaje in self.jugador.equipo:
            if objetivo == personaje.id[0]:
                personaje.vida_actual = personaje.vida_maxima
                print('Se ha curado al completo a {}, su salud ahora es {}/{}\n'.format(personaje.id, personaje.vida_actual, personaje.vida_maxima))
                self.enfriamiento_restante += 1
                return 'move'

class Inteligencia(Personaje):
    def __init__(self) -> None:
        super().__init__()
        self.id = 'Inteligencia'
        self.vida_maxima = 2
        self.vida_actual = 2

    def habilidad(self, opo : Jugador) -> str:
        letras_casillas = ('a', 'b', 'c', 'd')
        numeros_casillas = ('1', '2', '3', '4')

        posicion = input('Selecciona la casilla superior derecha del area 2x2 a explorar: ')
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

        self.enfriamiento_restante += 1

        return f'I{posicion[0]}{posicion[1]}'

class Francotirador(Personaje):
    def __init__(self):
        super().__init__()
        self.id = 'Francotirador'
        self.vida_maxima = 3
        self.vida_actual = 3

    def habilidad(self, opo : Jugador):

        posicion = input('Introduzca la casilla a la que disparar: ')
        diana =[]

        while posicion not in tablero:
            posicion = input('Esa casilla no existe, introduzca una casilla válida: ')
        equipo_enemigo = opo.equipo
        for enemigo in equipo_enemigo:
            if enemigo.posicion == posicion:
                enemigo.vida_actual = 0
                diana.append(enemigo)
                print(f'{enemigo.id} ha caído!')
                self.enfriamiento_restante += 1
                return f'{self.id[0]}{posicion}'
        if not diana:
            print(f'No se ha matado a ningún enemigo en {posicion}')
            self.enfriamiento_restante += 1
            return 'move'

class Artillero(Personaje):
    def __init__(self):
        super().__init__()
        self.id = 'Artillero'
        self.vida_maxima = 2
        self.vida_actual = 2

    def habilidad(self, opo : Jugador):
        letras_casillas = ('a', 'b', 'c', 'd')
        numeros_casillas = ('1', '2', '3', '4')

        posicion = input('Selecciona la casilla superior izquierda del area 2x2 que quieres atacar: ')
        posiciones_validas = ['a1','a2','a3','b1','b2','b3','c1', 'c2', 'c3']

        while posicion not in posiciones_validas:
            posicion = input('Selecciona una casilla valida que abarque un area 2x2:  ')

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
            self.enfriamiento_restante += 1
            return 'move'

        self.enfriamiento_restante += 1
        return f'A{posicion[0]}{posicion[1]}'

#-- PRUEBAS


















