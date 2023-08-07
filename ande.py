#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

# Inicialização do robô EV3
ev3 = EV3Brick()

# Inicialização dos motores
motor_esquerdo = Motor(Port.B)
motor_direito = Motor(Port.C)

# Definindo a velocidade dos motores
velocidade = 500  # Ajuste conforme necessário

# Andar para a frente por 1 segundo
motor_esquerdo.run(velocidade)
motor_direito.run(velocidade)

wait(1000)  # Aguarda 1 segundo

# Parar os motores
motor_esquerdo.stop()
motor_direito.stop()
