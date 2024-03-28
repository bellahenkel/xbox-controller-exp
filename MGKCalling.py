# This is the code that runs on the controller-end Raspberry Pi

from math import e
from gpiozero import Servo
import pygame
from gpiozero.pins.pigpio import PiGPIOFactory
import socket
import threading
import time
import json

# Set IP and port 
# Port value must be the same on both Pis
# IP should be the static IP address set on the receiving Pi

UDP_IP = "192.168.1.19"
UDP_PORT = 5005

# Defines "socket" object that will send values over Ethernet
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Defines values that will be sent to other Pi
brushless_value = 0
servo_value = 0
pump_value = 0
servo2_position = 0

tube_lowered = False

# This is required for the code that identifies the controller
pygame.init()

# Function that reduces the number of decimal values of a very long float
# This is used for some values to reduce lag between the two Pis
def truncate(number, dec):
    multiplier = 10 ** dec
    return int(number * multiplier)/multiplier
 
joysticks = {}

# This is the start of the main loop
done = False
while not done:

# The values that will be sent to the other Pi
# Each one is a value that denotes the speed and/or position of a motor
    controller_input = {
    'brushless_value' : brushless_value,
    'servo_value' : servo_value,
    'pump_value' : pump_value,
    'servo2_position' : servo2_position
}
    
# This is some more code needed to initialize the controller inputs
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

# This code is for getting input from the controller
# And converting it into the positioning of the servo motor that controls steering
        if joystick.get_axis(0) !=3:
            dec_1 = truncate(joystick.get_axis(0), 2)
            servo_value = -dec_1
        else:
            servo_value = 0

# This code that takes controller input and converts it into the forward/backward driving
# As well as speed         
        if joystick.get_axis(4) > -0.015 and joystick.get_axis(4) < 0.015:
            brushless_value = 0
        else:
# This line specifically controls how the vehicle accelerates
# In relation to how much the joystick is pressed in either direction
            brushless_value = truncate(pow(joystick.get_axis(4), 3), 3)

# This code changes whether the pump tubing is lowered or raised based on button input
        if joystick.get_button(5) == 1:
            if tube_lowered == False:
                servo2_position = 0.5/1000
                tube_lowered = True
            if tube_lowered == True:
                servo2_position = 2.5/1000
                tube_lowered = False

# This code takes button input from the controller
# And turns on the pump motor while the button is pressed
        if joystick.get_button(4) == 1:
            pump_value = 0.1
        else:
            pump_value = 0

# This line is only for testing and is not needed for the vehicle to run          
print(controller_input)

# This code is what packages the motor values using JSON
# and then sends them over the Ethernet
# This process occurs 100 times per second
MESSAGE = json.dumps(controller_input)
encodedString = MESSAGE.encode(encoding = 'UTF-8')
sock.sendto(encodedString, (UDP_IP, UDP_PORT))
time.sleep(0.01)
