from clases import (Jugador, Personaje, Medico, Inteligencia, Francotirador, Artillero)
from utils import (limpiar_terminal, eliminar_personajes_muertos)

def main():

    print('Bienvenidos a Tactical Battle. A jugar!\n')

    input('Turno del Jugador 1. Pulsa intro para comenzar')
    j1 = Jugador()
    j1.crear_equipo()
    j1.posicionar_equipo()
    input('Jugador 1, pulsa intro para terminar tu turno')
    limpiar_terminal()

    input('Turno del Jugador 2. Pulsa intro para comenzar')
    j2 = Jugador()
    j2.crear_equipo()
    j2.posicionar_equipo()
    input('Jugador 2, pulsa intro para terminar tu turno')
    limpiar_terminal()

    j1.oponente = j2
    j2.oponente = j1

    final = False

    while not final:

        input('Turno del Jugador 1. Pulsa intro para comenzar')
        limpiar_terminal()

        eliminar_personajes_muertos(j1.equipo)
        final = j1.turno()
        if final:
            print("***** El jugador 1 ha ganado la partida! *****")
            return 0

        j1.realizar_accion()


        input('Jugador 1, pulsa intro para terminar tu turno')
        limpiar_terminal()

        input('Turno del Jugador 2. Pulsa intro para comenzar')
        limpiar_terminal()

        eliminar_personajes_muertos(j2.equipo)
        final = j2.turno()
        if final:
            print("***** El jugador 2 ha ganado la partida! *****")
            return 0

        j2.realizar_accion()


        input('Jugador 2, pulsa intro para terminar tu turno')

        limpiar_terminal()

if __name__ == '__main__':

    main()













