#this code controls only the client/input side of the program. 
#It will eventually send controller values to the other pi using socket


#at some point this will control the motor and the servo

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


#start everything
pygame.init()

#some values for the servo motor
factory = PiGPIOFactory()
servo = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width =2.5/1000, pin_factory = factory)
#brushless = Servo(27, min_pulse_width = 0.5/1000, max_pulse_width =2.5/1000, pin_factory = factory)
pump = Servo(22, min_pulse_width = 0.5/1000, max_pulse_width =2.5/1000, pin_factory = factory)





    #Need this for the servo joystick mapping. I feel like truncating it a bit reduces the jitter
def truncate(number, dec):
    multiplier = 10 ** dec
    return int(number * multiplier)/multiplier
  
    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
joysticks = {}

done = False
while not done:
    controller_input = {
    'brushless_value' : brushless_value,
    'servo_value' : servo_value,
    'pump_value' : pump_value
}
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


        # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()


        # For each joystick:
    for joystick in joysticks.values():
        jid = joystick.get_instance_id()


            # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
     
        guid = joystick.get_guid()
       

        power_level = joystick.get_power_level()
       
            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
        axes = joystick.get_numaxes()
  
    for i in range(axes):
        axis = joystick.get_axis(i)


    buttons = joystick.get_numbuttons()
      
    for i in range(buttons):
        button = joystick.get_button(i)
         

#IMPORTANT THING HERE
            #The following lines of code are what control the servo motor. It's not very clean but it gets the job done for now

        if joystick.get_axis(0) != 3:
            dec_1 = truncate(joystick.get_axis(0), 2)
            servo_value = -dec_1
        else:
            servo_value = 0
        

        if joystick.get_axis(4) > -0.015 and joystick.get_axis(4) < 0.015:
            brushless_value = 0
        else:
            brushless_value = truncate(pow(joystick.get_axis(4), 3),3)
      
              
    
               
            

        if joystick.get_button(4) == 1:
            pump_value = 0.1
    
               
                
        else:
            pump_value = 0
          

    print(controller_input)
    MESSAGE = json.dumps(controller_input)
    encodedString = MESSAGE.encode(encoding = 'utf-8')
    sock.sendto(encodedString, (UDP_IP, UDP_PORT))
    time.sleep(0.01)
