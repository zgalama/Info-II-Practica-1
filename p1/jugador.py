from utils import validar_celda, comprobar_celda_disponible
from personajes import *


class Jugador:
    def __init__(self):
        self.oponente = None
        self.equipo = []
        self.informe = None

        # crear_equipo y posicionar_equipo se llaman en el constructor: se hacen cada vez que se instancia la clase
        self.crear_equipo()
        self.posicionar_equipo()

    def set_oponente(self, jugador):
        # Comprobamos que el oponente es un objeto de la clase Jugador y lo guardamos en el atributo "oponente"
        assert issubclass(type(jugador),
                          Jugador), "Error asignando oponente. Tiene que ser de tipo Jugador y es " + str(type(jugador))
        self.oponente = jugador

    def turno(self):
        # Muestra el resultado del turno del oponente
        if self.informe is not None:
            print('\n---- INFORME ---- ')  # \n: Salto de línea (por estética)
            print(self.informe)

        # Muestra el estado del equipo
        print('\n---- SITUACION DEL EQUIPO ---- ')
        for per in self.equipo:
            print('{} está en {} [Vida {}/{}]'.format(per.nombre, per.posicion, per.vida_actual, per.vida_maxima))
        print('')  # Espacio

        # Muestra las posibles acciones a realizar y las ejecuta
        # Devuelve un código alfanumérico (AB2, FD1, ...) cuando afecta al enemigo, o None, cuando no
        accion = self.realizar_accion()

        # Le pide al oponente cómo le afecta su acción
        # Va fuera del if siguiente para que oponente pueda actualizar su informe
        resultado = self.oponente.recibir_accion(accion)

        if resultado is not None:
            # Muestra el efecto de la acción en el oponente
            print('\n---- RESULTADO DE LA ACCIÓN ----')
            print(resultado['respuesta'])
            # Victoria pasa a valer True si se ha acabado la partida (gana el atacante)
            victoria = resultado['victoria']
        else:
            self.informe = 'Nada que reportar'
            victoria = False  # No se puede ganar sin agredir al contrario

        return victoria

    def realizar_accion(self):
        # Obtenemos un diccionario con las acciones disponibles (ver get_acciones)
        acciones_disponibles = self.get_acciones()

        # Las mostramos al usuario
        print('\n---- ACCIONES DISPONIBLES ---- ')
        for num, accion in acciones_disponibles.items():
            print('{}: {}'.format(num, accion[0]))

        # El usuario escoge, y se ejecuta la acción
        while True:
            # Elegir accion
            accion = input('Seleccion la acción de este turno: ')
            if accion not in acciones_disponibles:
                print('ERROR: acción inválida')
                continue

            # Se llama a la función asociada con la acción escogida (elemento 1 de la tupla, ver get_acciones)
            codigo = acciones_disponibles[accion][1]()
            return codigo  # Devolvemos el código de acción

    def recibir_accion(self, codigo):
        # Cuando la acción del contrario no afecta a nuestro tablero, actualizar informe y devolver None
        # Es el caso de las acciones del médico y los movimientos
        if codigo is None:
            self.informe = 'Nada que reportar'
            return None

        # Interpretamos el código
        personaje = codigo[0]
        coordenadas = codigo[1:]

        resultado = {'respuesta': None, 'victoria': False}  # Plantilla para rellenar

        if personaje == 'A':
            # El artillero enemigo afecta a un área de 2 x 2 en nuestro tablero: la calculamos
            celdas_afectadas = []
            max_col = ord(coordenadas[0]) + 1 if coordenadas[0] < 'D' else ord(coordenadas[0])
            max_row = ord(coordenadas[1]) + 1 if coordenadas[1] < '4' else ord(coordenadas[1])

            for col in range(ord(coordenadas[0]), max_col+1):
                for row in range(ord(coordenadas[1]), max_row + 1):
                    celdas_afectadas.append(chr(col)+chr(row))

            # La respuesta empieza vacía y se va llenando
            respuesta = ''
            bajas = []

            # Comprobamos en cada celda afectada si hay algún personaje nuestro; si lo hay, le bajamos la vida y,
            # si no le queda más vida, lo eliminamos, informando en ambos casos al contrario
            for c in celdas_afectadas:
                for idx, per in enumerate(self.equipo):
                    if per.posicion == c:
                        per.vida_actual -= 1  # herir
                        if per.vida_actual == 0:
                            respuesta += '{} ha sido eliminado\n'.format(per.nombre)
                            # Los personajes que se quedan sin vida se guardan en bajas
                            bajas.append(idx)
                        else:
                            respuesta += '{} ha sido herido en {} [Vida restante: {}]\n'.format(per.nombre,
                                                                                                per.posicion,
                                                                                                per.vida_actual)

            # Elmininamos del equipo los personajes sin vida
            for idx in bajas:
                del self.equipo[idx]

            # Para ver si nos quedan personajes militares (Artillero o Francotirador), sumamos el daño que pueden
            # hacer los personajes que quedan en el equipo; si sale 0, solo quedan Médico y/o Inteligencia.
            danyo_restante = 0
            for per in self.equipo:
                danyo_restante += per.danyo

            # Si ya no quedan personajes o el daño que pueden hacer los que quedan es 0, acabamos la partida
            if len(self.equipo) == 0 or danyo_restante == 0:
                resultado['victoria'] = True

            # Para no devolver una respuesta vacía
            if respuesta == '':
                respuesta = 'Ningún personaje ha sido herido\n'
            resultado['respuesta'] = respuesta

        elif personaje == 'F':
            idx = 0
            respuesta = ''

            # El francotirador solo afecta a una casilla. Vamos a esa casilla, y si tenemos un personaje, lo eliminamos
            # (el daño del francotirador es la vida máxima de un personaje; cuando son alcanzados, siempre mueren)
            for idx, per in enumerate(self.equipo):
                if per.posicion == coordenadas:
                    per.vida_actual = 0
                    respuesta = '{} ha sido eliminado\n'.format(per.nombre)
                    break

            del self.equipo[idx]  # Borrar del equipo

            # Misma lógica que en caso anterior
            danyo_restante = 0
            for per in self.equipo:
                danyo_restante += per.danyo
            if len(self.equipo) == 0 or danyo_restante == 0:
                resultado['victoria'] = True

            if respuesta == '':
                respuesta = 'Ningún personaje ha sido herido\n'
            resultado['respuesta'] = respuesta

        elif personaje == 'I':
            # La inteligencia afecta a un área de 2 x 2 en nuestro tablero; la calculamos
            celdas_afectadas = []
            max_col = ord(coordenadas[0]) + 1 if coordenadas[0] < 'D' else ord(coordenadas[0])
            max_row = ord(coordenadas[1]) + 1 if coordenadas[1] < '4' else ord(coordenadas[1])

            for col in range(ord(coordenadas[0]), max_col+1):
                for row in range(ord(coordenadas[1]), max_row + 1):
                    celdas_afectadas.append(chr(col)+chr(row))

            # Comprobamos las casillas afectadas y mostramos un mensaje por cada personaje avistado
            respuesta = ''
            for c in celdas_afectadas:
                for per in self.equipo:
                    if per.posicion == c:
                        respuesta += '{} ha sido avistado en {}\n'.format(per.nombre, per.posicion)

            if respuesta == '':
                respuesta = 'Ningún personaje ha sido revelado\n'
            resultado['respuesta'] = respuesta

        self.informe = resultado['respuesta']
        return resultado

    def posicionar_equipo(self):
        # Asumimos que el equipo ya está creado
        assert len(self.equipo) > 0, 'Error: no hay equipo que posicionar!'

        # Por cada personaje, pedimos al usuario dónde colocarlo
        print('Vamos a posicionar a nuestros personajes en el tablero!')
        for personaje in self.equipo:
            celda_valida = False
            while not celda_valida:
                celda = input('Indica la celda (A-D, 1-4. p.ej: B2) en la que posicionar al {}: '.format(personaje.nombre))
                celda = celda.upper()
                celda_valida = validar_celda(celda, 'D', '4')
                if not celda_valida:
                    # No es una celda válida y volvemos al input
                    print('Ups... valor de celda incorrecto. ')
                else:
                    # Hay que comprobar si ya había otro personaje
                    disponible = comprobar_celda_disponible(celda, self.equipo)
                    if disponible:
                        # Si no lo había, asignamos la posición
                        personaje.posicion = celda
                    else:
                        # Si lo había, volvemos al input
                        celda_valida = False
                        print('Ups... la celda ya está ocupada!')
                        continue

        print('Posicionamiento terminado\n')

    def crear_equipo(self):
        # Instanciamos objetos de cada tipo de personaje.
        # Siempre hay un objeto de cada tipo.
        medico = Medico(self.equipo)
        artillero = Artillero(self.equipo)
        francotirador = Francotirador(self.equipo)
        intel = Inteligencia(self.equipo)
        self.equipo.extend([medico, artillero, francotirador, intel])

    def get_acciones(self):
        # Creamos el diccionario con las acciones disponibles
        acciones_disponibles = dict()
        contador_acciones = 1
        for per in self.equipo:
            # La clave del diccionario es contador_acciones (1, 2, 3... en orden) pasado a string, y el valor,
            # una tupla con el string que se muestra al usuario (elemento 1) y la función correspondiente a esa acción
            # (elemento 2 de la tupla).
            acciones_disponibles[str(contador_acciones)] = ('Mover ({})'.format(per.nombre), per.mover)
            contador_acciones += 1

            # Mover siempre está disponible, pero las habilidades especiales tienen enfriamiento y podrían no estar
            # disponibles (y no se añaden al diccionario)
            if per.habilidad_disponible():
                acciones_disponibles[str(contador_acciones)] = ('{} ({})'.format(per.desc_habilidad(), per.nombre),
                                                                per.habilidad)
                contador_acciones += 1

        return acciones_disponibles
