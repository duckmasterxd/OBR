#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, LogicMailbox, NumericMailbox, TextMailbox
import math
import time
ev3 = EV3Brick()

# definindo sensores e motores
with open("verde.txt", "r+") as calibragem:
    calibragem.read()
with open("branco.txt", "r+") as calibragem:
    manipulas = calibragem.read()

global sala3
global PIDRGB 
PIDRGB = True 
sala3 = 0
ultrafrente = 0
ultralado = 0
tempoinicial = time.time()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
sld = ColorSensor(Port.S4)
sle = ColorSensor(Port.S1)
gyro = GyroSensor(Port.S2)
slf = ColorSensor(Port.S3)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 65, axle_track = 105)
server = BluetoothMailboxServer()
tbox = TextMailbox('piton', server)
nbox = NumericMailbox('piton', server)
print("Esperando conectar...")
server.wait_for_connection(1)
print("Conectado.")
cronometro = 0
# programa principal

class RunOnce(object):
    def __init__(self, func):
        self.func = func
        self.ran = False

    def __call__(self):
        if not self.ran:
            self.func()
            self.ran = True

def transformarlistaemstring(lista1):
    #print(lista1)
    for i in range(0, len(lista1)):
        if lista1[i] == "(" or lista1[i] == "," or lista1[i] == ")":
            lista1[i] = " "
    lista2 = []
    for i in range(0, len(lista1)):
        if lista1[i] != " " and lista1[i + 1] != " ":
            lista2.append(lista1[i] + lista1[i + 1])
        elif lista1[i - 1] == " " and lista1[i + 1] == " ":
            lista2.append(lista1[i])
    lista2.pop(3)
    #print(lista2)

def TransformarRGBemListas():
    lista1 = []
    lista2 = []
    calibragem = open("verde.txt", "r")
    calibrs = calibragem.read()

    for i in range(0, len(calibrs)):
        lista1.append(calibrs[i])
    
    #transformarlistaemstring(lista1)
    for i in range(0, len(lista1)):
        if lista1[i] == "(" or lista1[i] == "," or lista1[i] == ")":
            lista1[i] = " "
    lista2 = []
    for i in range(0, len(lista1)):
        if lista1[i] != " " and lista1[i + 1] != " ":
            lista2.append(lista1[i] + lista1[i + 1])
        elif lista1[i - 1] == " " and lista1[i + 1] == " ":
            lista2.append(lista1[i])
    
    #print(lista2)
    
    listacalibragem = lista2
    for i in range(0, 6):
        listacalibragem[i] = int(listacalibragem[i])
    global R
    global G
    global B
    R = listacalibragem[0]
    G = listacalibragem[1]
    B = listacalibragem[2]
    RD = listacalibragem[3]
    GD = listacalibragem[4]
    BD = listacalibragem[5]
    global razaoRG
    global razaoBG
    razaoRG = G / R
    razaoBG = G / B
    razaoRGD = (GD / RD) 
    razaoBGD = (GD / BD) 
    razaoRG = min(razaoRG, razaoRGD) - 0.5
    razaoBG = min(razaoBG, razaoBGD) - 0.5
    print(razaoRG, razaoBG)
    print(razaoRGD, razaoBGD)
    
def Calibragem():
    if calibrarverde == 1:
        salvarverdeE = sle.rgb()
        salvarverdeD = sld.rgb()
        calibragem = open("verde.txt", "w")
        calibragem.write("{} {}".format(salvarverdeE, salvarverdeD))

def Inicializar():
    tbox.wait()
    TransformarRGBemListas()
    tempoinicial = time.time()
    while tbox.read() != "Inicie":
        robot.stop()

i = 0
d = 0
erro = 0
ue = 0
fe = 0
fd = 0
fp = 100
kp = 5
ki = 0.00001
kd = 2

def PIDRGB():
    calibrarverde = 0
    sldRGB = sld.rgb()
    sleRGB = sle.rgb()
    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
    global erro
    erro = (0 - ((mediargbd + float(manipulas)) - mediargbe))
    global d
    global ue
    d = erro - ue
    global i
    i = i + erro
    soma = (((erro * kp) + (i * ki)) + (d * kd))
    ue = erro
    global fp
    robot.drive(-fp, -soma)

def DuploVerde():
    sleRGB = sle.rgb()
    sldRGB = sld.rgb()
    #if ((sleRGB[0] * 4) < sleRGB[1] and (sleRGB[2] * 1.2) < sleRGB[1]) and ((sldRGB[0] * 4) < sldRGB[1] and (sldRGB[2] * 1.2) < sldRGB[1]) and sldRGB[1] < 30 and sleRGB[1] < 30: #Duplo Verde
    robot.drive(-80, 0)
    wait(1000)
    robot.turn(585)
    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
    while mediargbd > 20:
        mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
        robot.drive(0, 80)
    robot.turn(60)
    #robot.drive(80, 0)
    #wait(500)
    diferenca = 0

def Verde():
    acheiverde = False
    sleRGB = sle.rgb()
    sldRGB = sld.rgb()
    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
    if mediargbe < 32 or mediargbd < 32:
        if (sleRGB[1] < 30 and (sleRGB[0] * razaoRG) < sleRGB[1] and (sleRGB[2] * razaoBG) < sleRGB[1]) or (sldRGB[1] < 30 and (sldRGB[0] * razaoRG) < sldRGB[1] and (sldRGB[2] * razaoBG) < sldRGB[1]):
            acheiverde = True
            wait(50)
            robot.stop()
            wait(50)
            print(razaoRG, razaoBG)
            if (sldRGB[1] < 30 and (sldRGB[0] * razaoRG) < sldRGB[1] and (sldRGB[2] * razaoBG) < sldRGB[1]):
                print("Achei o direito")
                print("Média do esquerdo: {}, Média do direito: {}".format(mediargbe, mediargbd))
                print("RGB do esquerdo: {}, RGB do direito: {}".format(sleRGB, sldRGB))
                robot.drive(0, 100)
                wait(100)
                sleRGB = sle.rgb()
                sldRGB = sld.rgb()
                mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                print("Achei o direito")
                print("Média do esquerdo: {}, Média do direito: {}".format(mediargbe, mediargbd))
                print("RGB do esquerdo: {}, RGB do direito: {}".format(sleRGB, sldRGB))
                if sleRGB[1] < 30 and ((sleRGB[0] * razaoRG) < sleRGB[1] and (sleRGB[2] * razaoBG) < sleRGB[1]):
                    print("Achei duplo verde no direito")
                    DuploVerde()
                else:
                    print("Não achei duplo verde. Média do Esquerdo: ", mediargbe)
                    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                    robot.straight(-125)
                    robot.drive(0, -200)
                    wait(250)
                    sleRGB = sle.rgb()
                    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                    while mediargbe > 20:
                        sleRGB = sle.rgb()
                        mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                        #print("Tentando achar linha", mediargbe, sle.rgb())
            elif (sleRGB[1] < 30 and (sleRGB[0] * razaoRG) < sleRGB[1] and (sleRGB[2] * razaoBG) < sleRGB[1]):
                print("Achei o esquerdo")
                print("Média do esquerdo: {}, Média do direito: {}".format(mediargbe, mediargbd))
                print("RGB do esquerdo: {}, RGB do direito: {}".format(sleRGB, sldRGB))
                robot.drive(0, 100)
                wait(100)
                robot.stop()
                sleRGB = sle.rgb()
                sldRGB = sld.rgb()
                mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                print("Achei o esquerdo")
                print("Média do esquerdo: {}, Média do direito: {}".format(mediargbe, mediargbd))
                print("RGB do esquerdo: {}, RGB do direito: {}".format(sleRGB, sldRGB))
                if sldRGB[1] < 30 and ((sldRGB[0] * razaoRG) < sldRGB[1] and (sldRGB[2] * razaoBG) < sldRGB[1]):
                    print("Achei duplo verde no esquerdo")
                    DuploVerde()
                else:
                    print("Não achei duplo verde. Média do Direito: ", mediargbd)
                    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                    robot.straight(-125)
                    robot.turn(-290)
                    wait(250)
                    #robot.drive(0, 100)
                    #wait(250)
                    sldRGB = sld.rgb()
                    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                    while mediargbd > 20:
                        sldRGB = sld.rgb()
                        mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                        #print("Tentando achar linha", mediargbd, sld.rgb())
    return acheiverde

def Obstaculo():
    if slf.reflection() > 5:
        print("Achei obs")
        robot.straight(200)
        robot.turn(-290)
        sleRGB = sle.rgb()
        mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
        #mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
        if mediargbe > 30: #Caso ele desvie o obstáculo pelo lado esquerdo, este sensor deverá ser o esquerdo, caso contrário, será o direito.
            #robot.drive(-80, 300)
            robot.straight(-350)
            wait(500)
            robot.turn(290)
            wait(250)
            robot.straight(-865)
            wait(500)
            robot.turn(290)
            wait(250)
            robot.straight(-220)
            wait(500)
            robot.turn(-290)
            wait(250)
            sleRGB = sle.rgb()
            mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
            print("Tentando achar linha (obstaculo)", mediargbe, sleRGB)
            #robot.drive(0, 180)
            #wait(500) 
        robot.straight(-40)
        #sldRGB = sld.rgb()
        #mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
       #if mediargbd > 30: #Mesma coisa acima, só que o inverso.
            #sldRGB = sld.rgb()
            #mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
            #robot.drive(0, -200)
            #wait(500)
        robot.straight(20)
    
def Curva_de_90():
    global tempoinicial
    global tempofinal
    giro90 = gyro.angle()
    tempofinal = time.time()
    sleRGB = sle.rgb()
    sldRGB = sld.rgb()
    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
    mediargbe90 = ((sleRGB[0] + sleRGB[1] + sleRGB[2])/3) * 5
    mediargbd90 = ((sldRGB[0] + sldRGB[1] + sldRGB[2])/3) * 5
    if diferenca > 1.25:
        if mediargbd > mediargbe90:
            print("aacheio 90")
           #robot.drive(0, -200)
            #wait(200)
            robot.stop()
            wait(500)
            if Verde() == False:
                robot.turn(-70)
                robot.straight(-100)
                while mediargbd > 30:
                    sleRGB = sle.rgb()
                    sldRGB = sld.rgb()
                    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                    robot.drive(0, 200)
                    wait(500)
                robot.turn(-60)
                #robot.straight(30)
                tempoinicial = time.time()
        elif mediargbe > mediargbd90:
            print("Achei 90")
            robot.drive(0, 200)
            wait(200)
            if Verde() == False:
                robot.turn(70)
                robot.straight(-100)
                while mediargbe > 30:
                    sleRGB = sle.rgb()
                    sldRGB = sld.rgb()
                    mediargbe = (sleRGB[0] + sleRGB[1] + sleRGB[2])/3
                    mediargbd = (sldRGB[0] + sldRGB[1] + sldRGB[2])/3
                    robot.drive(0, -200)
                robot.turn(60)
                #robot.straight(30)
                tempoinicial = time.time()
    if (gyro.angle() - giro90) > 60:
        robot.straight(30)

def ConversaEntreEV3s():
    nbox.wait()
    chave = nbox.read()
    print(chave)
    if chave == 1:
        robot.stop()

def Teste_Sala3():
    while slf.reflection() <= 1:
        robot.drive(-80, 0)
    tbox.send("Fechar garra")
    if slf.reflection() > 5:
        chave = 5
        print("travei o motor")
        nbox.send(chave)

def Rampa():
    if tbox.read() == "Achei rampa":
        global sala3
        sala3 = 1
        global angulorampa
        angulorampa = gyro.angle()
    elif tbox.read() == "Entrei na sala 3":
        sala3 = 2

def AbaixarGarraHost():
    tbox.send("Abaixa ae")
    wait(100)
    while tbox.read() != "Terminei":
        robot.stop()
        wait(100)
def LevantarGarraHost():
    tbox.send("Levanta ae")
    wait(100)
    while tbox.read() != "Terminei":
        robot.stop()
        wait(100)
def AbrirGarraHost():
    tbox.send("Abre ae")
    wait(100)
    while tbox.read() != "Terminei":
        robot.stop()
        wait(100)
def FecharGarraHost():
    tbox.send("Fecha ae")
    wait(100)
    while tbox.read() != "Terminei":
        robot.stop()
        wait(100)

def PIDGyro(distancia):
    gyro.reset_angle(0)
    p = 0.5
    fp = 80
    while robot.distance() >= distancia:
        #print(robot.distance())
        correcao = 0 - (gyro.angle() * p)
        #print(correcao)
        robot.drive(-fp, correcao)
    robot.stop()
    left_motor.brake()
    right_motor.brake()

def GirarGraus(graus):
    angulosdesejados = gyro.angle() + graus
    if angulodesejados < 0:
        while gyro.angle() < angulosdesejados:
            robot.drive(0, 300)
    elif angulodesejados > 0:
        while gyro.angle() < angulosdesejados:
            robot.drive(0, -300)
    robot.stop()
     

def Sala3():
    robot.straight(-90)
    AbaixarGarraHost()
    AbrirGarraHost()
    robot.drive(-200, 0)
    while nbox.read() != 1:
        pass
    robot.stop()
    gyro.reset_angle(0)
    while gyro.angle() > -45:
        robot.drive(0, -200)
    tbox.send("Indo pro meio da sala 3")
    while ultrafrente != 1:
        ultrafrente = nbox.read()
        robot.drive(-80, 0)
    FecharGarraHost()
    LevantarGarraHost()
    while gyro.angle() < -1:
        robot.drive(0, 200)
    tbox.send("Comecei a checagem no lado esquerdo")
    while ultrafrente != 2:
        ultrafrente = nbox.read()
        robot.drive(-80, 0)
    tbox.send("Dando ré")
    while ultrafrente != 3:
        ultrafrente = nbox.read()
        robot.drive(80, 0)
    while gyro.angle() < 180:
        robot.drive(0, 200)
    tbox.send("Voltando pro meio")


    
    


    

Inicializar()
TransformarRGBemListas()
#gyro.reset_angle(0)
tempoinicial = time.time()
while sala3 != 2:
    if sala3 == 0:
        tempofinal = time.time()
        global diferenca
        diferenca = tempofinal - tempoinicial
        #Teste_Sala3()
        PIDRGB()
        Verde()
        Curva_de_90()
        Obstaculo()
        Rampa()
        print(tbox.read())
    if sala3 == 1:
        PIDRGB()
        Rampa()
        ki = 0
        kd = 0
        fp = 200
        print(sala3)

Sala3()