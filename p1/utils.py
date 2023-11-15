# Limpia la terminal para empezar el turno del otro jugador
def limpiar_terminal():
    print(chr(27) + "[2J")


# Valida que la celda escogida no se salga del tablero
# En este caso, max_col y max_row podrían no haberse incluido como parámetros porque el tablero es siempre igual.
def validar_celda(celda, max_col, max_row):
    if len(celda) != 2:
        return False
    if celda[0] < 'A' or celda[0] > max_col:
        return False

    if celda[1] < '1' or celda[1] > max_row:
        return False
    return True

# Compruba que no hay otro personaje en la celda escogida
def comprobar_celda_disponible(celda, equipo):
    for p in equipo:
        if p.posicion == celda:
            return False
    return True

# Valida que la celda1 y la celda2 son contiguas (un personaje podría moverse de una a otra)
def validar_celda_contigua(celda1, celda2):
    if ord(celda1[0]) - 1 == ord(celda2[0]) or ord(celda1[0]) + 1 == ord(celda2[0]):  # La letra es contigua
        return ord(celda1[1]) == ord(celda2[1])  # El numero es igual

    if ord(celda1[1]) - 1 == ord(celda2[1]) or ord(celda1[1]) + 1 == ord(celda2[1]):  # El numero es contiguo
        return ord(celda1[0]) == ord(celda2[0])  # La letra es igual

    return False
