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

#definicao de motores e sensores

motor_esquerdo = Motor(Port.B)
motor_direito = Motor(Port.D)
garra = Motor(Port.C)
cacamba = Motor(Port.A)
sld = ColorSensor(Port.S1)
sle = ColorSensor(Port.S2)
ultra = UltrasonicSensor(Port.S3)
slf = ColorSensor(Port.S4)

#definicao de variaveis e calculo de base (medidas do robô para mover ambos motores simultaneamente)

erro = 0 
i = 0
d = 0
pid = 0
ultimoerro = 0
kp = 6
ki = 0.01
kd = 1.8
base = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 95, axle_track = 127)
fp = 300
rgbd = list
rgbe = list
os.system('setfont Lat15-TerminusBold14')

#arquivos de calibragem, medias e etc

manipulacao = open("branco.txt", "r")

manipulacaodenovo = float(manipulacao.readline())

arq = open("calibragem.txt", "r")
importrgb = open("verde.txt", "r")

valoresverde = importrgb.readline()
rgb_list = valoresverde[1:-1].split(", ")

#int = transformar em numero inteiro

vermelho_e = int(rgb_list[0])
verde_e = int(rgb_list[1])
azul_e = int(rgb_list[2])

vermelho_d = int(rgb_list[3])
verde_d = int(rgb_list[4])
azul_d = int(rgb_list[5])

importrgbcinza = open("resgate.txt", "r")

valorescinza = importrgbcinza.readline()
rgb_listcinza = valorescinza[1:-1].split(", ")

vermelho_ec = int(rgb_listcinza[0])
verde_ec = int(rgb_listcinza[1])
azul_ec = int(rgb_listcinza[2])

vermelho_dc = int(rgb_listcinza[3])
verde_dc = int(rgb_listcinza[4])
azul_dc = int(rgb_listcinza[5])

importbrancosala3 = open("brancosala3.txt", "r")

valoresbrancosala3 = importbrancosala3.readline()

rgb_media_listbrancosala3 = valoresbrancosala3.split(", ")

mediacinzaesquerda = (int(rgb_listcinza[0]) + int(rgb_listcinza[1]) + int(rgb_listcinza[2]))/3

mediacinzadireita = (int(rgb_listcinza[3]) + int(rgb_listcinza[4]) + int(rgb_listcinza[5]))/3

#transformar string (linha) em float (flutuante)

mdcbd =(mediacinzadireita + float(rgb_media_listbrancosala3[0]))/2

mdcbe = (mediacinzaesquerda + float(rgb_media_listbrancosala3[1]))/2

importvermelhosala3 = open("vermelhosala3.txt", "r")

valoresvermelhosala3 = importvermelhosala3.readline()

rgb_listvermelhosala3 = valoresvermelhosala3[1:-1].split(", ")

vermelho_ve = float(rgb_listvermelhosala3[0])
verde_ve = float(rgb_listvermelhosala3[1])
azul_ve = float(rgb_listvermelhosala3[2])

importverdesala3 = open("verdesala3.txt", "r")

valoresverdesala3 = importverdesala3.readline()

rgb_listverdesala3 = valoresverdesala3[1:-1].split(", ") 

vermelho_vd = float(rgb_listverdesala3[0])
verde_vd = float(rgb_listverdesala3[1])
azul_vd = float(rgb_listverdesala3[2])

#se o sensor de cor da frente identificar um valor rgb = 0 ele substitui o valor por 1.5 para não executar 
#uma divisão por 0 

if vermelho_vd == 0: 
    vermelho_vd = 1.5

if azul_vd == 0:
    azul_vd = 1.5

rzslfverdevv = verde_vd / vermelho_vd
rzslfverdeva = verde_vd / azul_vd 

#rz = razao, slf = sensor, red = vermelho, vv = vermelho e verde, va = vermelho e azul 

if verde_ve == 0:
    verde_ve = 1.5

if azul_ve == 0:
    azul_ve = 1.5

#razoes para verde, vermelho e margem de erro

rzslfredvv = vermelho_ve / verde_ve #3,54
rzslfredva = vermelho_ve / azul_ve #39?

razaoave1 = azul_ec / vermelho_ec #1,6 
razaoave2 = azul_ec / verde_ec #1,16

razaoavd1 = azul_dc / vermelho_dc 
razaoavd2 = azul_dc / verde_dc

razaorge = verde_e / vermelho_e #4,2
razaobge = verde_e / azul_e #1,35

razaorgd = verde_d / vermelho_d #3,3
razaobgd = verde_d / azul_d #1,32

razaorge = razaorge - 1.4
razaobge = razaobge - 1

razaorgd = razaorgd - 1.4
razaobgd = razaobgd - 1

def DescerGarra(): 
    garra.run(-180)
    wait(1200)
    garra.stop()
    wait(500)
    garra.hold()

def SubirGarra(): 
    garra.run(180)
    wait(600)
    garra.stop()
    wait(800)
    garra.run(185)
    wait(600)
    garra.hold()

#definicoes de timer 
#timer pega a data desde a epoque e subtrai do novo valor de timer para ver quanto tempo se passou desde a epoque
ultimoresettimer = time.time()
timerdasala3 = time.time()

def Calculopid():
    global erro
    global d
    global i 
    global ultimoerro 
    global fp
    global ki 
    global kp 
    rgbd = sld.rgb() 
    rgbe = sle.rgb()
    md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)
    me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)
    erro = 0 - ((md + manipulacaodenovo) - me)  #se o valor for positivo o sensor direito está vendo branco, ent precisa virar pra esquerda, e vice versa 
    i = i + erro
    d = erro - ultimoerro
    pid = (((erro * kp) + (i * ki)) + (d * kd))
    base.drive(fp, pid)
    
    #curva de 90
    if (erro <= -40) and not(((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1])):  #curva para a esquerda
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, -200) 
        while (md >= 25):
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            rgbd = sld.rgb()
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        if (me <= 30):
            base.straight(50)
        base.drive(0, 200)
        rgbd = sld.rgb() 
        rgbe = sle.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        erro = 0 - (md - me)
        while (math.fabs(erro) >= 15): #math.fabs é o módulo do erro, módulo é a distância de um número até zero
            rgbd = sld.rgb() 
            rgbe = sle.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            erro = 0 - (md - me)
    elif (erro >= 40) and not(((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1])):  #curva pra direita
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, 200) 
        while (me >= 25):
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            rgbe = sle.rgb()
        base.straight(-50)
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        if (md <= 30):
            base.straight(50)
        base.drive(0, -200) 
        rgbd = sld.rgb() 
        rgbe = sle.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        erro = 0 - (md - me)
        while (math.fabs(erro) >= 15): #math.fabs é o módulo do erro, módulo é a distância de um número até zero 
            rgbd = sld.rgb() 
            rgbe = sle.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            erro = 0 - (md - me)

def Obstaculo(): 
    global ultimoresettimer
    if ultra.distance() < 70:
        ultimoresettimer = time.time()
        base.straight(-200)
        base.turn(290)
        base.straight(600)
        wait(500)
        base.turn(-290)
        wait(250)
        base.straight(1200)
        wait(500)
        base.drive(0, -200)
        wait(1500)
        rgbd = sld.rgb() 
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        base.drive(200, 0) #andar até encontrar linha
        while (md >= 25):
            rgbd = sld.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        wait(500)
        base.straight(100)
        rgbe = sle.rgb() 
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        base.drive(0, 100)
        while (me >= 45):
            rgbe = sle.rgb()
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        wait(1000)
        ultimoresettimer = time.time()
    
def Verde():
    global ultimoresettimer
    rgbd = sld.rgb()
    rgbe = sle.rgb()

    if (((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) or ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1])): 
        base.stop()
        wait(1000)
        ultimoresettimer = time.time()
        print("Comeco do verde")
        if ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]):
            base.stop()
            wait(500)
            print("Estou verificando")
            rgbe = sle.rgb()
            if ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]):
                base.stop()
                wait(1000)
                print("Duplo verde direito")
                base.drive(0, -200)
                wait(2000)
                base.drive(0, -200)
                rgbd = sld.rgb()
                md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                while (md >= 25):
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                if (me <= 30):
                    base.straight(50)
                base.drive(0, 200)
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                ultimoresettimer = time.time()
            else:
                print("Estou no direito")
                wait(500)                
                rgbd = sld.rgb() 
                md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)
                base.straight(80)
                if (md <= 50):
                    print("Curva verde direito")
                    rgbe = sle.rgb()
                    me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
                    base.straight(70)
                    base.drive(0, 200)
                    wait(1500) 
                    while (me >= 25):
                        rgbe = sle.rgb()
                        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                    base.straight(50) 
                    ultimoresettimer = time.time() 
                else:
                    print("É falso direito")
                    Calculopid()
                    ultimoresettimer = time.time()
        elif ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]):
            print("Achei verde esquerdo")
            base.stop()
            wait(1000)
            rgbd = sld.rgb()
            if ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]):
                print("Epa duplo verde esquerdo")
                rgbd = sld.rgb()
                md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                base.drive(0, -200)
                wait(2000)
                base.drive(0, -200)
                while (md >= 25):
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                if (me <= 30):
                    base.straight(50)
                base.drive(0, 200)
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                ultimoresettimer = time.time()
            else:
                print("Estou no esquerdo")
                wait(500) 
                rgbe = sle.rgb()
                me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)
                base.straight(80)
                if (me <= 50):
                    print("Curva verde esquerdo") 
                    base.straight(70)
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                    base.drive(0, -200)
                    wait(1500)
                    while (md >= 25):
                        rgbd = sld.rgb()
                        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                    base.straight(50)
                    ultimoresettimer = time.time()
                else:
                    print("É falso esquerdo")
                    Calculopid()
                    ultimoresettimer = time.time()

#termo que funciona como especie de booleano para a programacao ir para o looping principal
alinhei = 0 

#alinhar consiste em o robô alinhar-se perpendicularmente à fita prateada que dá inicio a sala3
#usando a media dos sensores esquerdo e direito, do branco e da fita prateada, garantindo precisão 

def Alinhar():
    rgbd = sld.rgb()
    rgbe = sle.rgb()
    if ((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or (((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
        base.straight(50)
        if ((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or (((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
            print("Vou alinhar perpendicularmente à fita prateada da sala3")
            base.stop()
            wait(1000)
            rgbd = sld.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            rgbe = sle.rgb()
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3

            errocbd = (mdcbd - md)
            errocbe = (mdcbe - me)

            kpcb = 20

            margem = 3

            while ((me > mdcbe + margem) or (me < mdcbe - margem)) or ((md > mdcbd + margem) or (md < mdcbd - margem)):
                rgbd = sld.rgb()
                md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                errocbd = (mdcbd - md)
                errocbe = (mdcbe - me)

                motor_esquerdo.run(kpcb*errocbe) 
                motor_direito.run(kpcb*errocbd)
            base.stop()
            alinhei = 1
            return alinhei

#definicoes de booleano para as areas de resgate, assim o robô ao final de executar a varredura
#irá verificar o que é verdadeiro e o que é falso, assim o robô toma a "decisão" para qual area de resgate
#irá depositar as vitimas e kit de resgate

areasupd = False 
areainfe = False

def Sala3():
    global timerdasala3
    base.stop()
    wait(500)
    print("Estou na sala 3")
    DescerGarra()
    wait(2000)
    timerdasala3 = time.time()
    base.straight(1500)
    wait(1000)
    SubirGarra()
    wait(1000)
    base.drive(100, 0)
    timerdasala3 = time.time()
    while ultra.distance() > 200:
        pass
    base.stop()
    wait(1000)
    if time.time() - timerdasala3 > 5:
        print("Nao achei area supd")
        areasupd = False
        base.straight(-300)
        wait(1000)
    else: 
        print("Achei area supd")
        areasupd = True
        base.straight(-200)
        wait(1000)
    base.stop()
    wait(1000)
    base.drive(50, -200)
    wait(1500)
    distancia = ultra.distance()
    base.drive(-300, 0)
    wait(2000)
    while ultra.distance() > distancia:
        print("Estou me enquadrando na parede")
        distancia = ultra.distance()
    print("Enquadrei")
    base.stop()
    wait(1000)
    DescerGarra()
    base.straight(850)
    wait(1000)
    SubirGarra()
    wait(2000)
    DescerGarra()
    wait(2000)
    base.drive(0, -200)
    wait(1500)
    base.stop()
    wait(1000)
    base.drive(200, 0)
    wait(2000)
    while ultra.distance() > 130:
        pass
    base.stop() 
    SubirGarra()
    wait(2000)
    base.drive(0, 200)
    wait(3400)
    base.drive(-200, 0)
    wait(4000)
    base.straight(100)
    base.drive(0, -200)
    wait(2000)
    timerdasala3 = time.time()
    base.drive(50, 0)
    while ultra.distance() > 70:
        pass
    base.stop()
    wait(1000)
    if time.time() - timerdasala3 > 5:
        print("Nao achei area infe")
        areainfe = False
        wait(1000)
        base.straight(-300)
    else: 
        print("Achei area infe")
        areainfe = True
        wait(1000)
        base.straight(-100)
    base.drive(0, 200)
    wait(1500)
    base.straight(-400)
    DescerGarra()
    wait(1000)
    base.straight(850)
    SubirGarra()
    base.drive(0, -200)
    wait(1500)
    base.stop()
    DescerGarra()
    wait(2000)
    base.straight(500)
    base.stop()
    SubirGarra()
    wait(2000)
    DescerGarra()
    wait(2000)
    base.drive(0, 200)
    wait(2000)
    base.straight(-500)
    base.stop()
    SubirGarra()
    wait(2000)
    DescerGarra()
    wait(2000)
    base.straight(750)
    base.drive(0, -200)
    wait(1500)
    base.straight(750)
    SubirGarra()
    base.straight(-500)
    base.stop()
    wait(1000)
    if areasupd == True and areainfe == True:
        print("estou na sala3.1")
        base.drive(0, -200)
        wait(2000)
        base.drive(100, 0)
        while ultra.distance() > 70:
            pass
        base.drive(0, -200)
        wait(5000)
        base.straight(-300)
        cacamba.run(-300)
        wait(2000)
        cacamba.hold()
    if areasupd == True and areainfe == False:
        print("estou na sala3.2")
        base.drive(0, 200)
        wait(1800)
        base.drive(100, 0)
        while ultra.distance() > 70:
            pass
        base.drive(0, -200)
        wait(5000)
        base.straight(-300)
        cacamba.run(-300)
        wait(2000)
        cacamba.hold()
    if areasupd == False and areainfe == True:
        print("estou na sala3.3")
        base.drive(0, -200)
        wait(1800)
        base.drive(100, 0)
        while ultra.distance() > 70:
            pass
        base.drive(0, -200)
        wait(5000)
        base.straight(-300)
        cacamba.run(-300)
        wait(5000)
        cacamba.hold()
estounarampa = False 

#após uma quantia de tempo sem achar verde, obstaculo, e etc, o robô pensa que só está seguindo linha
#então provavelmente ele está na rampa, vira para verificar se o ultrassonico vê algo
#se ver algo, ele não executa o looping principal, ou seja, vai alinhar e fazer calculopid

def VerificarRampa():
    global ultimoresettimer
    if time.time() - ultimoresettimer > 50:
        base.turn(335) #90 graus é a intenção
        wait(1000)
        if ultra.distance() < 70:
            estounarampa = True
        else: 
            estounarampa = False
            print("Não estou na rampa")
            ultimoresettimer = time.time()
        base.turn(-335)

garra.hold()
cacamba.hold()
while Alinhar() != 1:
    pass
Sala3()

#segura a garra, enquanto ele não estiver na rampa, faz calculopid, obstaculo, verde e verificar rampa
#quando ele estiver na rampa ele irá alinhar e fazer calculopid, após alinhar ele irá fazer sala3
"""
garra.hold()
while estounarampa == False:
    Calculopid()
    Obstaculo()
    Verde()
    VerificarRampa()
while alinhei != 1:
    Alinhar()
    Calculopid()
Sala3()"""