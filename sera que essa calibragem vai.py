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
import os
ev3 = EV3Brick()

#definindo sensores e motores

lista1 = []
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sld = ColorSensor(Port.S3)
sle = ColorSensor(Port.S4)
garra = Motor(Port.D)
cacamba = Motor(Port.A)
ultra = UltrasonicSensor(Port.S1)
slf = ColorSensor(Port.S2)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 65, axle_track = 105)
os.system('setfont Lat15-TerminusBold14')
c = 0

c = 0
calibesquerdo = sle.rgb()
calibdireito = sld.rgb()

calibbrancosala3direito = sld.rgb()
calibbrancosala3esquerdo = sle.rgb()

while ev3.buttons.pressed() != [Button.UP, Button.DOWN]:
    if ev3.buttons.pressed() == [Button.UP]:
        wait(500)
        c = c + 1
        ev3.screen.clear()
    elif ev3.buttons.pressed() == [Button.DOWN]:
        wait(500)
        c = c - 1
        ev3.screen.clear()
    elif ev3.buttons.pressed() == [Button.LEFT] and c == 0:
        calibesquerdo = sle.rgb()
    elif ev3.buttons.pressed() == [Button.RIGHT] and c == 0:
        calibdireito = sld.rgb()
    elif ev3.buttons.pressed() == [Button.LEFT] and c == 1:
        calibesquerdoB = sle.rgb()
        calibesquerdoBB = (calibesquerdoB[0] + calibesquerdoB[1] + calibesquerdoB[2])/3
    elif ev3.buttons.pressed() == [Button.RIGHT] and c == 1:
        calibdireitoB = sld.rgb()
        calibdireitoBB = (calibdireitoB[0] + calibdireitoB[1] + calibdireitoB[2])/3
    elif ev3.buttons.pressed() == [Button.RIGHT] and c == 2:
        calibresgated = sld.rgb()
    elif ev3.buttons.pressed() == [Button.LEFT] and c == 2:
        calibresgatee = sle.rgb()
    elif ev3.buttons.pressed() == [Button.LEFT] and c == 3:
        r,g,b = sle.rgb()
        calibbrancosala3esquerdo = (r+g+b)/3
    elif ev3.buttons.pressed() == [Button.RIGHT] and c == 3:
        r,g,b = sld.rgb()
        calibbrancosala3direito = (r+g+b)/3
    elif ev3.buttons.pressed() == [Button.LEFT] and c == 4:
        calibvermelhosala3 = slf.rgb()
    elif ev3.buttons.pressed() == [Button.LEFT] and c == 5:
        calibverdesala3 = slf.rgb()

    if c < 0:
        c = c + 1
    elif c == 0:
        ev3.screen.draw_text(50, 100, "Verde")
    elif c == 1:
        ev3.screen.draw_text(50, 100, "Branco")
    elif c == 2:
        ev3.screen.draw_text(50, 100, "Cinza")
    elif c == 3:
        ev3.screen.draw_text(50, 100, "BrancoSala3")
    elif c == 4:
        ev3.screen.draw_text(50, 100, "VermelhoSala3")
    elif c == 5:
        ev3.screen.draw_text(50, 100, "VerdeSala3")

    elif c > 5:
        c = c - 1

manipulacao = calibesquerdoBB - calibdireitoBB
calibtudao = str(calibesquerdo + calibdireito)
calibresgatetudo = str(calibresgatee + calibresgated)
calibbrancosala3tudo = str(calibbrancosala3direito) + ", " + str(calibbrancosala3esquerdo)

with open("verde.txt", "w+") as calibragem:
    calibragem.write(calibtudao)
    print(calibtudao)
with open("branco.txt", "w+") as calibragem:
    print(manipulacao)
    calibragem.write(str(manipulacao))
with open("resgate.txt", "w+") as calibragem: 
    calibragem.write(calibresgatetudo)
with open ("brancosala3.txt", "w+") as calibragem:
    calibragem.write(calibbrancosala3tudo)
with open ("vermelhosala3.txt", "w+") as calibragem:
    calibragem.write(calibvermelhosala3)
with open ("verdesala3.txt", "w+") as calibragem:
    calibragem.write(calibverdesala3)
ev3.screen.clear()
ev3.screen.draw_text(50, 100, "Finalizado.")
wait(2000)