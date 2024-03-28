#this code controls only the client/input side of the program. It will eventually send controller values to the other pi using socket


from gpiozero import Servo
import pygame
from gpiozero.pins.pigpio import PiGPIOFactory

# Import pygame.locals for easier access to key coordinates
from pygame.locals import *

#start everything
pygame.init()

#some values for the servo motor
factory = PiGPIOFactory()
servo = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width =2.5/1000, pin_factory = factory)
brushless = Servo(27, min_pulse_width = 0.5/1000, max_pulse_width =2.5/1000, pin_factory = factory)



# Event processing step.
# Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
# JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        done = True  # Flag that we are done so we exit this loop.

    if event.type == pygame.JOYBUTTONDOWN:
        print("Joystick button pressed.")
        if event.button == 0:
            joystick = joysticks[event.instance_id]
            if joystick.rumble(0, 0.7, 500):
                print(f"Rumble effect played on joystick {event.instance_id}")

    if event.type == pygame.JOYBUTTONUP:
        print("Joystick button released.")

    # Handle hotplugging
    if event.type == pygame.JOYDEVICEADDED:
        # This event will be generated when the program starts for every
        # joystick, filling up the list without needing to create them manually.
        joy = pygame.joystick.Joystick(event.device_index)
        joysticks[joy.get_instance_id()] = joy
        print(f"Joystick {joy.get_instance_id()} connencted")

    if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        print(f"Joystick {event.instance_id} disconnected")

#IMPORTANT THING HERE
#The following lines of code are what control the servo motor. It's not very clean but it gets the job done for now

if joystick.get_axis(0) != 3:
    dec_1 = truncate(joystick.get_axis(0), 2)
    servo.value = dec_1

if joystick.get_axis(4) > -0.2 and joystick.get_axis(4) < 0.2:
    brushless.value = 0
elif joystick.get_axis(4) >=0.4 and joystick.get_axis(4) <= 0.8 or joystick.get_axis(4) <=0.4 and joystick.get_axis(4) >=-0.8:
    brushless.value = joystick.get_axis(4) * 0.1
