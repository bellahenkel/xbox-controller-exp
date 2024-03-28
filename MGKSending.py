import socket
import json
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

UDP_IP = "192.168.1.19"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

factory = PiGPIOFactory()
brushless = Servo(27, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
servo = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
pump = Servo(22, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
pump_servo = Servo(23, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)

while True:
    data, addr = sock.recvfrom(1024)
    decodedString = data.decode('UTF-8', 'strict')
    controller_data = json.loads(decodedString)
    
    brushless_value = controller_data["brushless_value"]
    servo_value = controller_data["servo_value"]
    pump_value = controller_data["pump_value"]
    servo2_value = controller_data["servo2_position"]
    
    brushless.value = brushless_value
    servo.value = servo_value
    pump.value = pump_value
    pump_servo.value = servo2_value
    
    print(controller_data)
