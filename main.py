from clases import (Jugador, Personaje, Medico, Inteligencia, Francotirador)

#--- PRUEBAS ---#

j1 = Jugador('Rosa')
j2 = Jugador('Felix')

j1.oponente = j2
j2.oponente = j1

exp1 = Inteligencia()
exp2 = Inteligencia()
med1 = Medico()
med2 = Medico()
frn1 = Francotirador()

exp1.posicion = 'c3'
exp2.posicion = 'a1'
frn1.posicion = 'd3'
med1.posicion = 'd1'
med2.posicion = 'b4'
exp2.vida_actual = 3
exp2.vida_maxima = 3

j1.equipo.append(exp1)
j1.equipo.append(med1)
j1.equipo.append(frn1)
j2.equipo.append(exp2)
j2.equipo.append(med2)

exp1.habilidad('d3', j2)
exp2.habilidad('c2', j1)
frn1.habilidad('b4',j2)

print(med2.vida_actual)


