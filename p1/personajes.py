from utils import *


class Personaje:
    def __init__(self, equipo):
        self.nombre = ""
        self.vida_maxima = 99
        self.vida_actual = 0
        self.danyo = 0
        self.posicion = ""
        self.enfriamiento = 1
        self.enfriamiento_restante = 0
        self.equipo = equipo

    def mover(self):  # La acción Mover es igual para todos los personajes
        celda_valida = False
        while not celda_valida:
            # Pedimos al usuario que nos indique la celda
            celda = input('Indica la celda a la que mover al {} (Posición actual: {})\n'.format(self.nombre,
                                                                                                self.posicion))
            celda = celda.upper()
            # Comprobamos que tiene sentido en nuestro tablero
            celda_valida = validar_celda(celda, 'D', '4')
            if not celda_valida:
                print('Ups... valor de celda incorrecto. ')
            else:
                # Comprobamos que no hay allí otro personaje
                disponible = comprobar_celda_disponible(celda, self.equipo)
                if disponible:
                    # Comprobamos que es contigua a aquella en la que estábamos
                    es_contigua = validar_celda_contigua(celda, self.posicion)
                    if not es_contigua:
                        celda_valida = False
                        print('Ups... la celda {} no es contigua a la posicion actual {}'.format(celda,
                                                                                                 self.posicion))
                        continue
                    # Solo cambiamos la posición si se cumple todo
                    self.posicion = celda
                else:
                    celda_valida = False
                    print('Ups... la celda ya está ocupada!')
                    continue
        return None

    def habilidad(self):
        # Depende del tipo de personaje
        raise NotImplemented("habilidad() no implementada")

    def habilidad_disponible(self):
        # Devuelve True o False dependiendo de si la habilidad se puede usar este turno.
        return self.enfriamiento_restante == 0

    def desc_habilidad(self):
        # Depende del tipo de personaje
        raise NotImplemented("desc_habilidad() no implementada")


class Medico(Personaje):
    def __init__(self, equipo):
        super().__init__(equipo)
        self.nombre = "Medico"
        self.vida_maxima = 1
        self.vida_actual = 1
        self.danyo = 0

    def get_personajes_curables(self):
        # Devuelve un diccionario con los personajes del equipo curables
        personajes_curables = dict()
        contador_acciones = 1

        # Recorremos el equipo, y añadimos los personajes curables al diccionario. La clave es un número que se va
        # incrementando (pasado a string), y el valor, el personaje al que asignamos ese número
        for per in self.equipo:
            if per.vida_actual < per.vida_maxima:
                personajes_curables[str(contador_acciones)] = per
                contador_acciones += 1
        return personajes_curables

    def habilidad_disponible(self):
        # Aquí también consideramos el caso de que no haya personajes curables
        return self.enfriamiento_restante == 0 and len(self.get_personajes_curables()) > 0

    def habilidad(self):
        # Obtenemos un diccionario con los personajes curables
        personajes_curables = self.get_personajes_curables()

        # Le mostramos las posibilidades al usuario
        for num, per in personajes_curables.items():
            print("{}: {} [{}/{}]".format(num, per.nombre, per.vida_actual, per.vida_maxima))

        while True:
            # El usuario elige, y comprobamos que el número escogido es, efectivamente, una clave del diccionario
            personaje = input('Selecciona el personaje a curar: ')
            if personaje not in personajes_curables:
                print('ERROR: selección inválida. ')
                continue

            # Si lo es, curamos al personaje escogido (que está almacenado en el valor del diccionario)
            personajes_curables[personaje].vida_actual = personajes_curables[personaje].vida_maxima

            # Restauramos el enfriamiento de todos los personajes
            for per in self.equipo:
                per.enfriamiento_restante = 0

            # Pero ponemos a 1 el del médico que acabamos de usar
            self.enfriamiento_restante = self.enfriamiento
            return None  # Devolvemos el código de acción (en este caso, no afecta al oponente)

    def desc_habilidad(self):
        # Cadena que describe la habilidad
        return 'Curar a un compañero'


class Artillero(Personaje):
    def __init__(self, equipo):
        super().__init__(equipo)
        self.nombre = "Artillero"
        self.vida_maxima = 2
        self.vida_actual = 2
        self.danyo = 1

    def habilidad(self):
        while True:
            # Pide al usuario la esquina superior izquierda de la zona a disparar
            celda = input('Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2): ')
            celda = celda.upper()
            celda_valida = validar_celda(celda, 'D', '4')
            if not celda_valida:
                print('Ups... valor de celda incorrecto. ')
                continue

            # Restaura el enfriamiento del equipo
            for per in self.equipo:
                per.enfriamiento_restante = 0

            # Ajusta el enfriamiento para la habilidad que acabamos de usar
            self.enfriamiento_restante = self.enfriamiento

            # Genera el código alfanumérico
            return 'A' + celda

    def desc_habilidad(self):
        # Cadena que describe la habilidad
        return 'Disparar en área (2x2). Daño 1.'


class Francotirador(Personaje):
    def __init__(self, equipo):
        super().__init__(equipo)
        self.nombre = "Francotirador"
        self.vida_maxima = 3
        self.vida_actual = 3
        self.danyo = 3

    def habilidad(self):
        while True:
            # Pide al usuario la celda a disparar
            celda = input('Indica las coordenadas de la celda a la que disparar: ')
            celda = celda.upper()
            celda_valida = validar_celda(celda, 'D', '4')
            if not celda_valida:
                print('Ups... valor de celda incorrecto. ')
                continue

            # Restaura el enfriamiento del equipo
            for per in self.equipo:
                per.enfriamiento_restante = 0

            # Ajusta el enfriamiento para la habilidad que acabamos de usar
            self.enfriamiento_restante = self.enfriamiento

            # Genera el código alfanumérico
            return 'F' + celda

    def desc_habilidad(self):
        # Cadena que describe la habilidad
        return 'Disparar a una celda. Daño 3.'


class Inteligencia(Personaje):
    def __init__(self, equipo):
        super().__init__(equipo)
        self.nombre = "Inteligencia"
        self.vida_maxima = 2
        self.vida_actual = 2
        self.danyo = 0

    def habilidad(self):
        while True:
            # Pide al usuario la esquina superior izquierda de la zona a visualizar
            celda = input('Indica las coordenadas de la esquina superior izquierda de la zona de observación (área 2x2): ')
            celda = celda.upper()
            celda_valida = validar_celda(celda, 'D', '4')
            if not celda_valida:
                print('Ups... valor de celda incorrecto. ')
                continue

            # Restaura el enfriamiento del equipo
            for per in self.equipo:
                per.enfriamiento_restante = 0

            # Ajusta el enfriamiento para la habilidad que acabamos de usar
            self.enfriamiento_restante = self.enfriamiento

            # Genera el código alfanumérico
            return 'I' + celda

    def desc_habilidad(self):
        # Cadena que describe la habilidad
        return 'Revelar a los enemigos en un área 2x2.'
