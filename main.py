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
motor_direito = Motor(Port.D)
garra = Motor(Port.C)
porta_cacamba = Motor(Port.A)
sld = ColorSensor(Port.S1)
sle = ColorSensor(Port.S2)
ultra = UltrasonicSensor(Port.S3)
slf = ColorSensor(Port.S4)
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

if vermelho_vd == 0: 
    vermelho_vd = 1.5

if azul_vd == 0:
    azul_vd = 1.5

rzslfverdevv = verde_vd / vermelho_vd
rzslfverdeva = verde_vd / azul_vd 

#rz = razao, slf = sensor, red = vermelho, vv = vermelho e verde, va = vermelho e azul 
#rzslfredvv = vermelho_ve / verde_ve #3,54
#rzslfredva = vermelho_ve / azul_ve #39?

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
    garra.run(180)
    wait(600)
    garra.hold()

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
    if (erro <= -40):  #curva para a esquerda
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, -200) 
        while (md >= 25):
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            rgbd = sld.rgb()
        base.straight(-50)
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        if (me <= 20):
            base.straight(50)
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
    elif (erro >= 40):  #curva pra direita
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
        if (md <= 20):
            base.straight(50)
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

def Obstaculo(): #andar até encontrar linha
    if ultra.distance() < 70:
        base.straight(-200)
        base.turn(290)
        base.straight(600)
        wait(500)
        base.turn(-290)
        wait(250)
        ultimoresettimer = time.time()
        base.straight(1050)
        ultimoresettimer = time.time()
        wait(500)
        base.turn(-320)
        wait(250)
        rgbd = sld.rgb() 
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        base.drive(200, 0)
        while (md >= 25):
            rgbd = sld.rgb()
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        wait(500)
        base.straight(100)
        ultimoresettimer = time.time()
        rgbe = sle.rgb() 
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        base.drive(0, 100)
        while (me >= 25):
            rgbe = sle.rgb()
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        wait(250)
        base.straight(-50)
        wait(1000)
        ultimoresettimer = time.time()
    
def Verde():
    rgbd = sld.rgb()
    rgbe = sle.rgb()

    if (((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]) or ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1])): 
        base.stop()
        wait(1000)
        ultimoresettimer = time.time()
        print("comeco")
        if ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]):
            base.stop()
            wait(500)
            print("to verificando")
            rgbe = sle.rgb()
            if ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]):
                base.stop()
                wait(1000)
                print("duplo verde direito")
                base.drive(0, -200)
                wait(2000)
                base.drive(0, -200)
                rgbd = sld.rgb()
                md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                while (md >= 25):
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                ultimoresettimer = time.time()
            else:
                print("estou ali")
                wait(500)                
                rgbd = sld.rgb() 
                md = ((rgbd[0] + rgbd[1] + rgbd[2])/3)
                base.straight(80)
                if (md <= 50):
                    print("curva verde direito")
                    rgbe = sle.rgb()
                    me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
                    base.straight(70)
                    base.drive(0, 200) 
                    wait(1500)
                    while (me >= 25):
                        rgbe = sle.rgb()
                        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                    base.straight(50)
                    base.drive(0, -50) 
                    ultimoresettimer = time.time() 
                else:
                    print("é falso direito")
                    Calculopid()
                    ultimoresettimer = time.time()
        elif ((rgbe[0] * razaorge) <= rgbe[1] and (rgbe[2] * razaobge) <= rgbe[1]):
            print("achei verde esquerdo")
            base.stop()
            wait(1000)
            rgbd = sld.rgb()
            if ((rgbd[0] * razaorgd) <= rgbd[1] and (rgbd[2] * razaobgd) <= rgbd[1]):
                print("epa duplo verde esquerdo")
                rgbd = sld.rgb()
                md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                base.drive(0, -200)
                wait(2000)
                base.drive(0, -200)
                while (md >= 25):
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                ultimoresettimer = time.time()
            else:
                print("estou aqui")
                wait(500) 
                rgbe = sle.rgb()
                me = ((rgbe[0] + rgbe[1] + rgbe[2])/3)
                base.straight(80)
                if (me <= 50):
                    print("curva verde esquerdo")
                    rgbd = sld.rgb()
                    md = (rgbd[0] + rgbd[1] + rgbd[2])/3 
                    base.straight(70)
                    base.drive(0, -200)
                    wait(1500)
                    while (md >= 25):
                        rgbd = sld.rgb()
                        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                    base.straight(50)
                    ultimoresettimer = time.time()
                else:
                    print("é falso esquerdo")
                    Calculopid()
                    ultimoresettimer = time.time()

chavedefenda = 0 

def Alinhar():
    rgbd = sld.rgb()
    rgbe = sle.rgb()
    if ((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or (((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
        base.straight(50)
        if ((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or (((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
            print("baraba")
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
            chavedefenda = 1
            return chavedefenda

def Sala3():
    base.stop()
    wait(500)
    print("fencis trombe")
    DescerGarra()
    wait(1000)
    base.straight(1000)
    wait(500)
    SubirGarra()
    wait(1000)
    base.turn(-350)
    wait(1000)
    base.straight(-300)
    distancia = ultra.distance()
    while ultra.distance() > distancia:
        print("zyb")
        wait(500)
        distancia = ultra.distance()
    print("zeb")
    base.stop()
    wait(500)
    DescerGarra()
    base.straight(900)
    wait(500)
    base.stop()
    SubirGarra()
    wait(1000)
    base.turn(200)
    timerdasala3 = time.time()
    base.drive(300, 0)
    while ((ultra.distance() > 70) and time.time() - timerdasala3 < 13):
        pass
    rgbslf = slf.rgb()
    if (rgbslf[1] < rgbslf[0] and rgbslf[2] < rgbslf[0]) or ((rgbslf[0] * rzslfverdevv) <= rgbslf[1] and (rgbslf[2] * rzslfverdeva) <= rgbslf[1]): 
        print("achei a area de resgate ocasião1")
        base.stop()
        wait(1000)
        base.straight(-25)
        base.turn(800)
        base.straight(-100)
        base.stop()
        wait(500)
        porta_cacamba.run(-300)
        wait(1000)
        porta_cacamba.hold()
        base.stop()
        wait(1000)
        base.straight(100)
        base.straight(-200)
        base.straight(80)
        base.turn(-350)
        DescerGarra()
        timerdasala3 = time.time()
        base.drive(300, 0)
        while ((ultra.distance() > 150) and time.time() - timerdasala3 < 2):
            pass
        SubirGarra()
        rgbslf = slf.rgb()
        if (rgbslf[1] < rgbslf[0] and rgbslf[2] < rgbslf[0]) or ((rgbslf[0] * rzslfverdevv) <= rgbslf[1] and (rgbslf[2] * rzslfverdeva) <= rgbslf[1]): 
            print("achei a area de resgate ocasião1.1")
            base.stop()
            wait(1000)
            base.straight(-25)
            base.turn(800)
            base.straight(-100)
            base.stop()
            wait(2000)
            porta_cacamba.run(-300)
            wait(1000)
            porta_cacamba.hold()
            base.stop()
            wait(2000)
            base.straight(100)
            base.straight(-200)
            base.straight(80)
            base.turn(-350)
            DescerGarra()
            timerdasala3 = time.time()
            """while time.time() - timerdasala3 < 13:
                pass
            SubirGarra()
            base.turn(suficiente para ficar de frente para alguma area de resgate)
            DescerGarra()
            timerdasala3 = time.time()
            base.drive(300, 0)
            while ((ultra.distance() > 70) and time.time() - timerdasala3 < 13):
                pass
            SubirGarra()
            base.turn(ficar de costas para a area)
            base.straight(para trás)
            porta_cacamba.run(100)
            wait(500)
            base.straight(100)
            base.straight(-200)
            base.stop()
            print("acabou 1") 
        else: 
            faz a outra lá 

    else: 
        base.turn(350)
        distancia = ultra.distance()
        base.straight(-250)
        while ultra.distance() > distancia:
            print("alguma coisa q ewu n boterib antes")
            wait(500)
            distancia = ultra.distance()
            DescerGarra()
            timerdasala3 = time.time()
            base.drive(300, 0)
            while ((ultra.distance() > 70) and time.time() - timerdasala3 < 13):
                pass
            SubirGarra()
            rgbslf = slf.rgb()
            if (rgbslf[1] < rgbslf[0] and rgbslf[2] < rgbslf[0]) or ((rgbslf[0] * rzslfverdevv) <= rgbslf[1] and (rgbslf[2] * rzslfverdeva) <= rgbslf[1]): 
                print("achei a area de resgate ocasião1.3")
                base.turn(para ficar de costas para a area)
                base.straight(para trás)
                porta_cacamba.run(100)
                wait(500)
                base.straight(100)
                base.straight(-200)
                DescerGarra()
                timerdasala3 = time.time()
                base.drive(300, 0)
                while ((ultra.distance() > 70) and time.time() - timerdasala3 < 13):
                    pass
                SubirGarra()
                rgbslf = slf.rgb()
                if (rgbslf[1] < rgbslf[0] and rgbslf[2] < rgbslf[0]) or ((rgbslf[0] * rzslfverdevv) <= rgbslf[1] and (rgbslf[2] * rzslfverdeva) <= rgbslf[1]): 
                    base.turn(para ficar de costas para a area)
                    base.straight(para trás)
                    porta_cacamba.run(100)
                    wait(500)
                    base.straight(100)
                    base.straight(-200)
                    print("acabou 3")"""

estounarampa = False 

def VerificarRampa():
    global ultimoresettimer
    if time.time() - ultimoresettimer > 50:
        base.turn(335) #90 graus é a intenção
        wait(1000)
        if ultra.distance() < 70:
            estounarampa = True 
            fp = 500
            kp = 8
        else: 
            estounarampa = False
            print("greg")
            ultimoresettimer = time.time()
        base.turn(-335)

'''while True:
    rgbe = sle.rgb()
    print(rgbe)
    wait(1000)'''


garra.hold()
porta_cacamba.hold()
while Alinhar() != 1:
    pass
Sala3()
       
"""garra.hold()
ultimoresettimer = time.time()
base.straight(200)
wait(1000)
if ((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or (((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
    print("deu erro na sala3 e vou fazer de novo")
    while Alinhar != 1: 
        pass
Sala3()
else: 
    estounarampa = False
    base.straight(-200)
while estounarampa == False:
    Calculopid()
    Obstaculo()
    Verde()
    VerificarRampa()
while chavedefenda != 1:
    Alinhar()
    Calculopid()
Sala3()
"""

