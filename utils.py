
def limpiar_terminal():
    print(chr(27) + "[2J")

def eliminar_personajes_muertos(equipo : list):
    for personaje in equipo:
        if personaje.vida_actual == 0:
            equipo.remove(personaje)