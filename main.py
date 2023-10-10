from clases import (Jugador, Personaje, Medico, Inteligencia, Francotirador, Artillero)

#--- PRUEBAS ---#

j1 = Jugador('Rosa')
j2 = Jugador('Felix')

j1.oponente = j2
j2.oponente = j1

med1 = Medico()
art1 = Artillero()
frc1 = Francotirador()
int1 = Inteligencia()
equipo1 = [med1,int1,art1,frc1]
j1.anadir_personanjes(equipo1)

med2 = Medico()
art2 = Artillero()
frc2 = Francotirador()
int2 = Inteligencia()
equipo2 = [med2,int2,art2,frc2]
j2.anadir_personanjes(equipo2)

print(j1.equipo[0].vida_actual)




