from clases import (Jugador, Personaje, Medico, Inteligencia)

#--- PRUEBAS ---#

j1 = Jugador('Rosa')
j2 = Jugador('Felix')

j1.oponente = j2
j2.oponente = j1

exp1 = Inteligencia()
exp2 = Inteligencia()
med1 = Medico()
med2 = Medico()

exp1.posicion = 'c3'
exp2.posicion = 'a1'
med1.posicion = 'd1'
med2.posicion = 'b4'
exp2.vida_actual = 1
exp2.vida_maxima = 3

j1.equipo.append(exp1)
j1.equipo.append(med1)
j2.equipo.append(exp2)
j2.equipo.append(med2)

exp1.habilidad('b3', j2)
exp2.habilidad('c2', j1)


