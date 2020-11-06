import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
import socketio
import asyncio
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialization
car_control_server="https://example.com?username=rpicontrol_p1"
kit = MotorKit()
loop = asyncio.get_event_loop()

# Arrow Up = 30-38
# Arrow Down = 40-48
# Arrow Left = 50
# Arrow Right = 60
# Stop Left Joystick = 10
# Stop Right Joystick = 20

def code_to_action(code):
    if code == "30":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.60
    elif code == "31":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.65
    elif code == "32":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.70
    elif code == "33":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.75
    elif code == "34":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.80
    elif code == "35":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.85
    elif code == "36":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.90
    elif code == "37":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 0.95
    elif code == "38":
        print("Arrow Up: " +str(code))
        kit.motor2.throttle = 1.00
    elif code == "40":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.60
    elif code == "41":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.65
    elif code == "42":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.70
    elif code == "43":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.75
    elif code == "44":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.80
    elif code == "45":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.85
    elif code == "46":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.90
    elif code == "47":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -0.95
    elif code == "48":
        print("Arrow Down: " +str(code))
        kit.motor2.throttle = -1.00
    elif code == "50":
        print("Arrow Left")
        kit.motor4.throttle = -1.00
    elif code == "60":
        print("Arrow Right")
        kit.motor4.throttle = 1.00
    elif code == "10":
        print("Stop Left Joystick")
        kit.motor2.throttle = None
    elif code == "20":
        print("Stop Right Joystick")
        kit.motor4.throttle = None
    else:
        print("Not valid command")

# Car GPIO
userLed=27

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(userLed, GPIO.OUT) # userLed pin set as output

# Socket IO Configuration
# Self Signed Certificate
sio = socketio.AsyncClient(ssl_verify=False)

@sio.event
async def connect():
    print("Connected to Car Control Server!")
    GPIO.output(userLed, GPIO.HIGH)

@sio.event
async def connect_error():
    print("Connection Error to Car Control Server!")

@sio.event
async def disconnect():
    print("Disconnected from Car Control Server!")
    GPIO.output(userLed, GPIO.LOW)

@sio.on('check_rpi_connectivity_ping')
async def on_message(data):
    print("Received Ping from Car Control Server")
    await sio.emit('check_rpi_connectivity_pong', 'pong')

@sio.on('rpi_car_control')
async def on_message(data):
    code_to_action(str(data))

async def start_server():
    await sio.connect(car_control_server)
    await sio.wait()

if __name__ == '__main__':
    loop.run_until_complete(start_server())
