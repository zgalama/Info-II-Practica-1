from clases import (Jugador, Personaje, Medico, Inteligencia, Francotirador, Artillero)

#--- PRUEBAS ---#

j1 = Jugador('Rosa')
j2 = Jugador('Felix')

j1.oponente = j2
j2.oponente = j1

j1.crear_equipo()
j2.crear_equipo()

j1.posicionar_equipo()

print(j1.equipo[1].posicion)

print(j1.equipo[1].equipo)
j1.equipo[2].mover()




