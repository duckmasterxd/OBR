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
garra = Motor(Port.D)
porta_cacamba = Motor(Port.A)
sld = ColorSensor(Port.S3)
sle = ColorSensor(Port.S4)
ultra = UltrasonicSensor(Port.S1)
slf = ColorSensor(Port.S2)
erro = 0 
i = 0
d = 0
pid = 0
ultimoerro = 0
kp = 4
ki = 0.01
kd = 1.8
base = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 95, axle_track = 127)
fp = 270
rgbd = list
rgbe = list
os.system('setfont Lat15-TerminusBold14')

manipulacao = open("branco.txt", "r")

manipulacaodenovo = float(manipulacao.readline())

arq = open("calibragem.txt", "r")
importrgb = open("verde.txt", "r")

valoresverde = importrgb.readline()
rgb_list = valoresverde[1:-1].split(", ")

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

mdcbd =(mediacinzadireita + float(rgb_media_listbrancosala3[0]))/2

mdcbe = (mediacinzaesquerda + float(rgb_media_listbrancosala3[1]))/2

importvermelhosala3 = open("vermelhosala3.txt", "r")

valoresvermelhosala3 = importvermelhosala3.readline()

rgb_listvermelhosala3 = valoresvermelhosala3

vermelho_ve = int(rgb_listvermelhosala3[0])
verde_ve = int(rgb_listvermelhosala3[1])
azul_ve = int(rgb_listvermelhosala3[2])

importverdesala3 = open("verdesala3.txt", "r")

valoresverdesala3 = importverdesala3.readline()

rgb_listverdesala3 = valoresverdesala3 

vermelho_vd = int(rgb_listverdesala3[0])
verde_vd = int(rgb_listverdesala3[1])
azul_vd = int(rgb_listverdesala3[2])

razaoslfverdevv = verde_vd / vermelho_vd
razaoslfverdeva = verde_vd / azul_vd 

razaoslfvermelhovv = vermelho_ve / verde_ve 
razaoslfvermelhova = vermelho_ve / azul_ve

razaoave1 = azul_ec / vermelho_ec #1,6 
razaoave2 = azul_ec / verde_ec #1,16

razaoavd1 = azul_dc / vermelho_dc 
razaoavd2 = azul_dc / verde_dc

razaorge = verde_e / vermelho_e #4,2
razaobge = verde_e / azul_e #1,35

razaorgd = verde_d / vermelho_d #3,3
razaobgd = verde_d / azul_d #1,32

razaorge = razaorge - 0.7
razaobge = razaobge - 0.5

razaorgd = razaorgd - 0.7
razaobgd = razaobgd - 0.5

def DescerGarra(): 
    garra.run_target(500, -130)

def SubirGarra(): 
    garra.run_target(500, 130)

def MediaDireita():
    rgbd = sld.rgb()
    md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)

def MediaEsquerda():
    rgbe = sle.rgb()
    me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)

def Mediadosdois():
    rgbd = sld.rgb()
    md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)
    rgbe = sle.rgb()
    me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)

def Calculopid():
    global erro
    global d
    global i 
    global ultimoerro 
    global fp
    Mediadosdois()
    erro = 0 - ((md + manipulacaodenovo) - me)  #se o valor for positivo o sensor direito está vendo branco, ent precisa virar pra esquerda, e vice versa 
    i = i + erro
    d = erro - ultimoerro
    pid = (((erro * kp) + (i * ki)) + (d * kd))
    base.drive(fp, pid)
    
    #curva de 90
    if (erro <= -85):  #curva para a esquerda
        MediaDireita()
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, -200) 
        while (md >= 75):
            MediaDireita()
        base.straight(-50)
        MediaEsquerda()
        if (me <= 70):
            base.straight(50)
        base.drive(0, 200)
        Mediadosdois()
        erro = 0 - (md - me)
        while (math.fabs(erro) >= 15):
            Mediadosdois()
            erro = 0 - (md - me)
    elif (erro >= 85):  #curva pra direita
        MediaEsquerda()
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, 200) 
        while (me >= 75):
            MediaEsquerda()
        base.straight(-50)
        MediaDireita()
        if (md <= 70):
            base.straight(50)
        base.drive(0, -200) 
        Mediadosdois()
        erro = 0 - (md - me)
        while (math.fabs(erro) >= 15):
            Mediadosdois()
            erro = 0 - (md - me)

def Obstaculo(): #andar até encontrar linha
    if ultra.distance() < 70:
        base.straight(-200)
        base.turn(290)
        base.straight(500)
        wait(500)
        base.turn(-290)
        wait(250)
        base.straight(1200)
        wait(500)
        base.turn(-290)
        wait(250)
        base.straight(500)
        wait(500)
        base.turn(350)
        wait(250)
        base.straight(-100)
    
def Verde():
    rgbd = sld.rgb()
    rgbe = sle.rgb()

    if ((((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) or ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1])) and (rgbe[1] >= 30 or rgbd[1] >= 30)): 
        base.stop()
        wait(1000)
        print("comeco")
        if ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]) and (rgbd[1] >= 30):
            base.stop()
            wait(500)
            print("to verificando")
            rgbe = sle.rgb()
            if ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) and (rgbe[1] >= 30):
                base.stop()
                wait(1000)
                print("duplo verde direito")
                base.straight(375)
                base.drive(0, -200)
                wait(300)
                MediaEsquerda() 
                while (me >= 75):
                    wait(1500)
                    MediaEsquerda() 
            else:
                print("estou ali")
                wait(500)                
                MediaDireita()
                base.straight(80)
                if (md <= 50):
                    print("curva verde direito")
                    MediaEsquerda() 
                    base.straight(150)
                    base.drive(0, 200) 
                    wait(1500)
                    while (me >= 75):
                        MediaEsquerda()
                    base.straight(100) 
                else:
                    print("é falso direito")
                    Calculopid()
        elif ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) and (rgbe[1] >= 30):
            print("achei verde esquerdo")
            base.stop()
            wait(1000)
            rgbd = sld.rgb()
            if (((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]) and (rgbd[1] >= 30)):
                print("epa duplo verde esquerdo")
                MediaEsquerda() 
                base.straight(200)
                base.drive(0, -200)
                while (me >= 75):
                    wait(50)
                    MediaEsquerda()
            else:
                print("estou aqui")
                wait(500) 
                MediaEsquerda()
                base.straight(80)
                if (me <= 50):
                    print("curva verde esquerdo")
                    MediaDireita() 
                    base.straight(100)
                    base.drive(0, -200)
                    wait(1500)
                    while (md >= 75):
                        MediaDireita()
                    base.straight(50)
                else:
                    print("é falso esquerdo")
                    Calculopid()

chavedefenda = 0 

def Alinhar():
    rgbd = sld.rgb()
    rgbe = sle.rgb()
    if (((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or ((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
        print("baraba")
        base.stop()
        wait(1000)
        Mediadosdois()

        errocbd = (mdcbd - md)
        errocbe = (mdcbe - me)

        kpcb = 10

        margem = 5

        while ((me > mdcbe + margem) or (me < mdcbe - margem)) or ((md > mdcbd + margem) or (md < mdcbd - margem)):
            Mediadosdois()
            errocbd = (mdcbd - md)
            errocbe = (mdcbe - me)

            motor_esquerdo.run(kpcb*errocbe) 
            motor_direito.run(kpcb*errocbd)
        base.stop()
        chavedefenda = 1
        return chavedefenda

def Sala3():
    base.stop()
    wait(500)
    print("fencis trombe")
    base.straight(1000)
    wait(500)
    base.turn(-350)
    wait(1000)
    base.straight(-250)
    distancia = ultra.distance()
    while ultra.distance() > distancia:
        print("zyb")
        wait(500)
        distancia = ultra.distance()
        
    print("zeb")
    base.stop()

garra.hold()
while Alinhar() != 1:
    Calculopid()
    Obstaculo()
    Verde()
    #Alinhar()
Sala3()