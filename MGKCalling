from math import e
from gpiozero import Servo
import pygame
from gpiozero.pins.pigpio import PiGPIOFactory
import socket
import threading
import time
import json

UDP_IP = "192.168.1.19"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

brushless_value = 0
servo_value = 0
pump_value = 0

pygame.init()

def truncate(number, dec):
    multiplier = 10 ** dec
    return int(number * multiplier)/multiplier
    
joysticks = {}

done = False
while not done:
    controller_input = {
    'brushless_value' : brushless_value,
    'servo_value' : servo_value,
    'pump_value' : pump_value
}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    joystick_count = pygame.joystick.get_count()
    
    for joystick in joysticks.values():
        jid = joystick.get_instance_id()
        name = joystick.get_name()
        guid = joystick.get_guid()
        power_level = joystick.get_power_level()
        axes = joystick.get_numaxes()
        
        for i in range(axes):
            axis = joystick.get_axis(i)
            
        buttons = joystick.get_numbuttons()
        
        for i in range(buttons):
            button = joystick.get_button(i)
            
        if joystick.get_axis(0) !=3:
            dec_1 = truncate(joystick.get_axis(0), 2)
            servo_value = -dec_1
        else:
            servo_value = 0
            
        if joystick.get_axis(4) > -0.015 and joystick.get_axis(4) < 0.015:
            brushless_value = 0
        else:
            brushless_value = truncate(pow(joystick.get_axis(4), 3), 3)
        
        if joystick.get_button(4) == 1:
            pump_value = 0.1
            
        else:
            pump_value = 0
            
print(controller_input)
MESSAGE = json.dumps(controller_input)
encodedString = MESSAGE.encode(encoding = 'UTF-8')
sock.sendto(encodedString, (UDP_IP, UDP_PORT))
time.sleep(0.01)
