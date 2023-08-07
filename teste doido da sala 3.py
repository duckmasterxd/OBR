#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math
import time
import os 
ev3 = EV3Brick()

motor_esquerdo = Motor(Port.B)
motor_direito = Motor(Port.C)
sld = ColorSensor(Port.S4)
sle = ColorSensor(Port.S1)
ultrafrente = UltrasonicSensor(Port.S3)
ultra = UltrasonicSensor(Port.S2)
erro = 0 
i = 0
d = 0
pid = 0
ultimoerro = 0
kp = 4
ki = 0.01
kd = 1
base = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 95, axle_track = 127)
fp = 270
rgbd = list
rgbe = list
os.system('setfont Lat15-TerminusBold14')

# Função para fazer o hub mudar a cor do LED
def mudar_cor_led(cor):
    ev3.light.on(cor)

arq = open("calibragem.txt", "r")
importrgb = open("verde.txt", "r")

valores = importrgb.readline()
rgb_list = valores[1:-1].split(", ")

vermelho_e = int(rgb_list[0])
verde_e = int(rgb_list[1])
azul_e = int(rgb_list[2])

vermelho_d = int(rgb_list[3])
verde_d = int(rgb_list[4])
azul_d = int(rgb_list[5])

razaorge = verde_e / vermelho_e #4,2
razaobge = verde_e / azul_e #1,35

razaorgd = verde_d / vermelho_d #3,3
razaobgd = verde_d / azul_d #1,32

razaorge = razaorge - 0.7
razaobge = razaobge - 0.5

razaorgd = razaorgd - 0.7
razaobgd = razaobgd - 0.5

print('verde_e', verde_e)
print('verde_d', verde_d)
print('vermelho_e', vermelho_e)
print('vermelho_d', vermelho_d)
print('azul_e', azul_e)
print('azul_d', azul_d)

print('RGE', razaorge)
print('RGD', razaorgd)
print('BGE', razaobge)
print('BGD', razaobgd)


def Calculopid():
    global erro
    global d
    global i 
    global ultimoerro 
    global fp
    rgbd = sld.rgb() 
    rgbe = sle.rgb()
    md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)
    me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)
    erro = 0 - (md - me) #se o valor for positivo o sensor direito está vendo branco, ent precisa virar pra esquerda, e vice versa 
    i = i + erro
    d = erro - ultimoerro
    pid = (((erro * kp) + (i * ki)) + (d * kd))
    base.drive(fp, pid)
    
    #curva de 90
    if (erro <= -85): #curva para a esquerda
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
        base.straight(150)
        base.drive(0, -200) 
        while (md >= 75):
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            rgbd = sld.rgb()
        base.straight(-100)
        base.drive(0, 200)
        rgbd = sld.rgb() 
        rgbe = sle.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        erro = 0 - (md - me)
        while (math.fabs(erro) >= 15):
            rgbd = sld.rgb() 
            rgbe = sle.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            erro = 0 - (md - me)
    elif (erro >= 85): #curva pra direita
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
        base.straight(150)
        base.drive(0, 200) 
        while (me >= 75):
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            rgbe = sle.rgb()
        base.straight(-100)
        base.drive(0, -200) 
        rgbd = sld.rgb() 
        rgbe = sle.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        erro = 0 - (md - me)
        while (math.fabs(erro) >= 15):
            rgbd = sld.rgb() 
            rgbe = sle.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            erro = 0 - (md - me)

def Obstaculo():
    if ultrafrente.distance() < 50:
        base.straight(-200)
        base.turn(290)
        base.straight(350)
        wait(500)
        base.turn(-290)
        wait(250)
        base.straight(880)
        wait(500)
        base.turn(-290)
        wait(250)
        base.straight(300)
        wait(500)
        base.turn(290)
        wait(250)
        base.straight(-40)
        base.straight(20)

def Verde():
    rgbd = sld.rgb()
    rgbe = sle.rgb()

    if ((((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) or ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1])) and (rgbe[1] >= 30 or rgbd[1] >= 30)):
        base.stop()
        wait(1000)
        print("comeco")
        base.straight(-35)
        if ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]) and (rgbd[1] >= 30):
            base.stop()
            wait(500)
            print("to verificando")
            rgbe = sle.rgb()
            if ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) and (rgbe[1] >= 30):
                base.stop()
                wait(1000)
                print("sla")
                base.straight(375)
                base.drive(0, -200)
                wait(300)
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
                while (me >= 75):
                    wait(500)
                    rgbe = sle.rgb()
                    me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
            else:
                print("estou ali")
                rgbd = sld.rgb() 
                rgbe = sle.rgb()
                md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)
                me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)
                base.straight(75)
                base.stop()
                wait(1000)
                if (md <= 75):
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                    base.straight(175)
                    base.drive(0, 200) 
                    while (me >= 75):
                        wait(50)
                        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                        rgbe = sle.rgb() 
                    base.straight(-100) 
                else:
                    print("é falso direito")
        elif ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) and (rgbe[1] >= 30):
            print("achei verde esquerdo")
            base.stop()
            wait(1000)
            base.straight(-35)
            wait(100)
            base.drive(0, 100)
            wait(800)
            rgbd = sld.rgb()
            if (((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]) and (rgbd[1] >= 30)):
                print("epa duplo verde esquerdo")
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
                base.straight(100)
                base.drive(0, -200)
                while (me >= 75):
                    wait(50)
                    rgbe = sle.rgb()
                    me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            else:  
                rgbe = sle.rgb()
                me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)
                if (me <= 75):
                    print("estou aqui")
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                    base.straight(300)
                    base.drive(0, -200)
                    wait(1000) 
                    while (md >= 75):
                        wait(50)
                        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                        rgbd = sld.rgb()
                    base.straight(-100)
                else:
                    print("é falso esquerdo")

'''rgbe = sle.rgb()
rbgd = sld.rgb()

print('Sensor Esquerdo:')
print('Vermelho:', rgbe[0])
print('Verde:', rgbe[1])
print('Azul:', rgbe[2])
print('-----------------------')
print('Sensor Direito:')
print('VermelhoD:', rgbd[0])
print('VerdeD:', rgbd[1])
print('AzulD:', rgbd[2])
print('-----------------------')'''


correntee = motor_esquerdo.current()
corrented = motor_direito.current()
limite_corrente = 1000

tempo_inicial = time.time()
tempo_limite = tempo_inicial + #tal segundos, aqui a gente define o tempo

def Sala3():
    rgbd = sld.rgb
    rgbe = sle.rgb
	
    razaoave1 = azul_e / vermelho_e #1,6
    razaoave2 = azul_e / verde_e#1,16

    razaoavd1 = azul_d / vermelho_d
    razaoavd2 = azul_d / verde_d 

    repete = 0

    #ver cinza

    if (((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or ((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
        base.stop()
        base.straight(suficiente para o robô entrar na sala)
        base.drive(90 graus) #para ficar encostado na parede
        while (correntee < limite_corrente) and (corrented < limite_corrente): #se enquadrar na parede
            base.straight(-50)
        
        #ver a reta lateral superior direito
        base.drive(90 graus para a direita) 
		#abre garra
		base.straight(sla)
		#fecha garra
		base.straight(volta para a posição original antes de andar para frente)
		base.drive(90 graus esquerda)
		while (correntee < limite_corrente) and (corrented < limite_corrente): #precisao de volta
			base.straight(-50)
		
        #varredura quadrado central
        base.straight(suficiente para entrar no quadrado central)
		base.drive(0, 200) #se eu n me engano aqui é pra direita
		while (repete < 4):
			#abre garra 
			base.straight(quantia indefinida)
			#fecha garra 
			base.drive(0, -200) #se eu n me engano aqui é pra esquerda 
			repete = repete + 1
		
        base.drive(fica virado rente a borda superior esquerda)
		#abre garra
		tempo_inicial = time.time()
		tempo_limite = tempo_inicial + #tal segundos, aqui a gente define o tempo
		while (correntee < limite_corrente) and (corrented < limite_corrente) or time.time() < tempo_limite:
			base.straight(75)
        
        if tempo_limite > time.time() #Sala3.3
            base.stop()
            print('n achei nada 1') 
            base.drive(90 graus direita)
            while (correntee < limite_corrente) and (corrented < limite_corrente): #precisao de volta
			    base.straight(50)
            if ver valor mt baixo:
                base.straight(-50)
                #abre garra
                base.straight(75)
                #fecha garra              
            elif ver parede branca:
                base.straigth(pra trás)
                base.drive(fica rente ao lado superior direito porém mais puxado pra lateral da sala) #varredura da lateral superior
				tempo_inicial = time.time()
				tempo_limite = tempo_inicial + #tal segundos, aqui a gente define o tempo
				while (correntee < limite_corrente) and (corrented < limite_corrente):
					#abre garra
					base.straight(75)
					#fecha garra
				if ver valor mt baixo:
                    base.straight(-50)
                    #abre garra
                    base.straight(75)
                    #fecha garra
                elif ver vermelho ou vermelho:
                    base.straight(pra trás)
                    base.drive(180 graus)
                    #deixa vitimas
                    while (correntee < limite_corrente) and (corrented < limite_corrente):
                        base.straight(-50)
                    base.straight(pouco pra frente)
                    while (correntee < limite_corrente) and (corrented < limite_corrente):
							#abre garra
							base.straight(50)
							#fecha
                    if ver valor mt baixo:
                        base.straight(-50)
                        #abre garra
                        base.straight(75)
                        #fecha garra
                    elif ver vermelho ou verde: 
                        base.straight(pra trás)
                        base.drive(180 graus)
                        #deixa as vitimas
                    base.straight(-50)
                    base.drive(ficar rente ao lado superior esquerdo, mais puxado pra lateral)
                    while (correntee < limite_corrente) and (corrented < limite_corrente):
                        #abre garra
                        base.straight(50)
                        #fecha
                    if ver valor mt baixo:
                        base.straight(-50)
                        #abre garra
                        base.straight(75)
                        #fecha garra
                    else: 
                        base.drive(180 graus)
                        base.straight(pra frente)
                        #deixa as vítimas
                        print('fim 3')

        elif (correntee > limite_corrente) and (corrented > limite_corrente):
            if ver valor mt baixo:
						base.straight(-50)
						#abre garra
						base.straight(75)
						#fecha garra 
			base.stop()
			#fecha garra
			
            elif ver verde ou vermelho:
				print('achei 1') 
				base.straight(quantia indefinida para trás)
				base.drive(180 graus)
				#deixa vítimas

				base.drive(fica rente ao lado superior direito porém mais puxado pra lateral da sala) #varredura da lateral superior
				tempo_inicial = time.time()
				tempo_limite = tempo_inicial + #tal segundos, aqui a gente define o tempo
				while (correntee < limite_corrente) and (corrented < limite_corrente) or time.time() < tempo_limite:
					#abre garra
					base.straight(75)
					#fecha garra
				
                if tempo_limite > time.time(): #Sala3.1
                    base.stop()
                    print('n achei nada 2')
                
                elif (correntee > limite_corrente) and (corrented > limite_corrente): #Sala3.2
					base.stop()
					if ver valor mt baixo:
						base.straight(-50)
						#abre garra
						base.straight(75)
						#fecha garra
					elif ver parede branca: #Sala3.1
						base.straight(-50)
						base.drive(ficar rente ao lado inferior esquerdo)
						while (correntee < limite_corrente) and (corrented < limite_corrente):
							#abre garra
							base.straight(50)
							#fecha
						base.stop()
						base.straight(pra trás um pouco)
						base.drive(180)
						#deixa vitimas
						base.drive(vira para ficar rente a primeira área)
						#abre garra 
						base.straight(frente)
						#fecha garra'	
						#deixa as vítimas na primeira área
						
                        base.drive(rente ao lado inferior esquerdo)

                        while (correntee < limite_corrente) and (corrented < limite_corrente):
                            #abre garra
							base.straight(50)
							#fecha

                        if ver valor mt baixo:
                            base.straight(-50)
                            #abre garra
                            base.straight(75)
                            #fecha garra
            
                        base.drive(vira para a área de resgate)
						#deixa as vitimas na segunda área
						print('fim 1')
					
					elif ver verde ou vermelho: #Sala3.2
						base.straight(-50)
                        base.drive(180 graus)
						#deixa vítimas
						base.drive(ficar rente ao lado inferior esquerdo)
                        tempo_inicial = time.time()
				        tempo_limite = tempo_inicial + #tal segundos, aqui a gente define o tempo
						
                        while tempo_limite > time.time(): #varredura linha de X 
							#abre garra
							base.straight(50)
							#fecha
						
                        while (correntee < limite_corrente) and (corrented < limite_corrente): #se enquadrando no meio da parede lateral do lado esquerdo
                        base.drive(equivalente pra ficar em posição de 90 graus virado para a direita)
                        base.straight(para trás)


                        base.stop()
                        base.drive(90 graus para direita)
						
                        while (correntee < limite_corrente) and (corrented < limite_corrente): #varredura da lateral esquerda inferior
                            #abre garra
                            base.straight(75)
                            #fecha garra
                        if ver valor mt baixo:
                            base.straight(-50)
                            #abre garra
                            base.straight(75)
                            #fecha garra
					    elif ver parede branca: #Sala3.1
                            base.straight(-50)
                            base.drive(ficar rente ao lado superior esquerdo)
                            while (correntee < limite_corrente) and (corrented < limite_corrente):
                                #abre garra
                                base.straight(50)
                                #fecha
                        base.drive(180)
                        #deixa as vítimas na primeira área
						print('fim 2')			

while cinzatrue != 1:
    Calculopid()
    Obstaculo()
    Verde()
Sala3()