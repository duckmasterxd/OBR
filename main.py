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

mediacinzabrancodireito =(mediacinzadireita + float(rgb_media_listbrancosala3[0]))/2

mediacinzabrancoesquerdo = (mediacinzaesquerda + float(rgb_media_listbrancosala3[1]))/2

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
    erro = 0 - ((md + manipulacaodenovo) - me)  #se o valor for positivo o sensor direito está vendo branco, ent precisa virar pra esquerda, e vice versa 
    i = i + erro
    d = erro - ultimoerro
    pid = (((erro * kp) + (i * ki)) + (d * kd))
    base.drive(fp, pid)
    
    #curva de 90
    if (erro <= -85):  #curva para a esquerda
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, -200) 
        while (md >= 75):
            md = (rgbd[0] + rgbd[1] + rgbd[2])/3
            rgbd = sld.rgb()
        base.straight(-50)
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        if (me <= 70):
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
    elif (erro >= 85):  #curva pra direita
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        base.stop()
        wait(500) 
        base.straight(100)
        base.drive(0, 200) 
        while (me >= 75):
            me = (rgbe[0] + rgbe[1] + rgbe[2])/3
            rgbe = sle.rgb()
        base.straight(-50)
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        if (md <= 70):
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
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
                while (me >= 75):
                    wait(1500)
                    rgbe = sle.rgb()
                    me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
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
                    base.straight(150)
                    base.drive(0, 200) 
                    wait(1500)
                    while (me >= 75):
                        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
                        rgbe = sle.rgb() 
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
                rgbe = sle.rgb()
                me = (rgbe[0] + rgbe[1] + rgbe[2])/3 
                base.straight(200)
                base.drive(0, -200)
                while (me >= 75):
                    wait(50)
                    rgbe = sle.rgb()
                    me = (rgbe[0] + rgbe[1] + rgbe[2])/3
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
                    base.straight(100)
                    base.drive(0, -200)
                    wait(1500)
                    while (md >= 75):
                        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
                        rgbd = sld.rgb()
                    base.straight(50)
                else:
                    print("é falso esquerdo")
                    Calculopid()

def Alinhar():
    rgbd = sld.rgb()
    md = (rgbd[0] + rgbd[1] + rgbd[2])/3
    rgbe = sle.rgb()
    me = (rgbe[0] + rgbe[1] + rgbe[2])/3

    errocbd = (mediacinzabrancodireito - md)
    errocbe = (mediacinzabrancoesquerdo - me)

    kpcbd = 10

    kpcbe = 10

    margem = 5

    while ((me > mediacinzabrancoesquerdo + margem) or (me < mediacinzabrancoesquerdo - margem)) or ((md > mediacinzabrancodireito + margem) or (md < mediacinzabrancodireito - margem)):
        rgbd = sld.rgb()
        md = (rgbd[0] + rgbd[1] + rgbd[2])/3
        rgbe = sle.rgb()
        me = (rgbe[0] + rgbe[1] + rgbe[2])/3
        errocbd = (mediacinzabrancodireito - md)
        errocbe = (mediacinzabrancoesquerdo - me)

        motor_direito.run(kpcbd * errocbd)
        motor_esquerdo.run(kpcbe * errocbe) 
    base.stop()


def AcharSala3():
    rgbd = sld.rgb() 
    rgbe = sle.rgb()
    if (((rgbe[0] * razaoave1) <= rgbe[2] and (rgbe[1] * razaoave2) <= rgbe[2]) or ((rgbd[0] * razaoavd1) <= rgbd[2] and (rgbd[1] * razaoavd2) <= rgbd[2])):
        base.stop()
        wait(1000)
        base.straight(1000)
        wait(1000)
        '''base.drive(0, -100)
        wait(2000)
        distancia = ultra.distance()
        while ultra.distance() > distancia:
            base.straight(-100)
            distancia = ultra.distance()
            print('zab')
            wait(500)
        print('zub')
        wait(500)
        base.stop()'''

'''garra.hold()
while True:
    Calculopid()
    Obstaculo()
    Verde()
    AcharSala3()'''

#ande enquanto a distancia aumentar para saber se está prensando    
'''slf = ColorSensor(Port.S2)

while True:
    valor_reflexao = slf.reflection()
    
    print(valor_reflexao)
    wait(1000)'''

'''def Zub():
    print('zub')

garra.control.stall_tolerances(10, 300)
garra.run_until_stalled(-10, Zub(), 10)'''

