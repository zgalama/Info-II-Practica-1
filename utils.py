
def limpiar_terminal():
    print(chr(27) + "[2J")

def eliminar_personajes_muertos(equipo : list):
    for personaje in equipo:
        if personaje.vida_actual == 0:
            equipo.remove(personaje)

def casillas_2x2(STR):
    STR = list(STR)
    casilla_puntero = STR[1:]
    casillas_afectadas = [casilla_puntero]
    ascii_letra = ord(casilla_puntero[0])
    num = int(casilla_puntero[1])

    c2 = str(ascii_letra + 1) + str(num)
    c3 = str(ascii_letra) + str(num + 1)
    c4 = str(ascii_letra + 1) + str(num + 1)

    casillas_afectadas.append(c2)
    casillas_afectadas.append(c3)
    casillas_afectadas.append(c4)

    return casillas_afectadas