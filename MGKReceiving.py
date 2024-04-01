# This is the code that runs on the Pi that is located on the vehicle
# It receives motor values from the first Pi
# and sends those values to the motors


import socket
import json
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

# The IP should be the static IP set on the first Pi
# The port should be the same 4 digit value on both devices
UDP_IP = "192.168.1.19"
UDP_PORT = 5005

# Creates a socket instance
# And binds it to the above IP address and Port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


factory = PiGPIOFactory()

# Each of these lines of code corresponds to a different motor
# It assigns a GPIO pin on the Pi to each motor
# And sets it up for receiving PWM
brushless = Servo(27, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
servo = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
pump = Servo(22, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
pump_servo = Servo(5, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)


# This is the main loop
while True:
# This line tells the Pi to listen to information received from the other Pi
# And then takes the values, "decodes" them from UTF-8
# And finally "extracts" the values from the JSON package so they are usable
    data, addr = sock.recvfrom(1024)
    decodedString = data.decode('UTF-8', 'strict')
    controller_data = json.loads(decodedString)
    

# Assigns each value received to a new variable
    brushless_value = controller_data["brushless_value"]
    servo_value = controller_data["servo_value"]
    pump_value = controller_data["pump_value"]
    servo2_value = controller_data["servo2_position"]
    
# Assigns the above variables to their corresponding motor instances
# This is what actually causes the GPIO pins to send signals as needed
    brushless.value = brushless_value
    servo.value = servo_value
    pump.value = pump_value
    pump_servo.value = servo2_value

# This line is for testing purposes only and is not needed to operate the vehicle
    print(controller_data)
