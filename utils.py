
def limpiar_terminal():
    print(chr(27) + "[2J")

def eliminar_personajes_muertos(equipo : list):
    for personaje in equipo:
        if personaje.vida_actual == 0:
            equipo.remove(personaje)

def casillas_2x2(STR):
    STR = list(STR)
    casilla_puntero = STR[1:]
    casilla = f'{casilla_puntero[0]}{casilla_puntero[1]}'
    casillas_afectadas = [casilla]
    ascii_letra = ord(casilla_puntero[0])
    num = int(casilla_puntero[1])

    c2 = chr(ascii_letra + 1) + str(num)
    c3 = chr(ascii_letra) + str(num + 1)
    c4 = chr(ascii_letra + 1) + str(num + 1)

    casillas_afectadas.append(c2)
    casillas_afectadas.append(c3)
    casillas_afectadas.append(c4)

    return casillas_afectadas


