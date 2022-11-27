import socket
import time
import traceback
import random
import base64

PEER_PORT = 33301    # Port for listening to other peers
SENSOR_PORT = 33401  # Port for listening to other sensors
VEHICLE_TYPE = 'truck' # bike, truck possible

def bencode(toEncode):
    ascii_encoded = toEncode.encode("ascii")
    base64_bytes = base64.b64encode(ascii_encoded)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def bdecode(toDecode):
    base64_bytes = toDecode.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

def sendAck(conn, raddr, result):
        try:
            msg = result
            conn.send(bencode(msg).encode())
        except Exception:
            print(traceback.format_exc())
            print('exception occurred while sending acknowledgement: ', Exception)

def senseSpeed():
    baseSpeed = 80
    randomMix = random.randint(-10, 10)
    res = baseSpeed + randomMix
    return res

def senseProximity():
    baseProximity = 20
    randomMix = random.randint(-10, 10)
    res = baseProximity + randomMix
    return res

def sensePressure():
    if VEHICLE_TYPE == 'car':
        val = random.randint(30, 33) # car tyre pressure
    elif VEHICLE_TYPE == 'bike':
        val = random.randint(80, 130) # two wheeler tyre pressure
    else:
        val = random.randint(80, 131) # truck tyre pressure
    return val

def senseLight():
    state = ['on', 'off', 'faulty']
    return random.choice(state)

def senseWiper():
    state = ['off', 'on', 'faulty']
    return random.choice(state)

def sensePassengerCount():
    if VEHICLE_TYPE == 'car':
        val = random.randint(1, 6)
    else: # bike, truck
        val = random.randint(1, 3)
    return val

def senseFuel():
    state = ['low', 'medium', 'full']
    return random.choice(state)

def senseEngineTemperature():
    baseTemp = 200
    randomMix = random.randint(-5, 20)
    res = baseTemp + randomMix
    return res

def callActuator(interest):
    if interest.lower() == "speed":
        return senseSpeed()
    elif interest.lower() == "proximity":
        return senseProximity()
    elif interest.lower() == "pressure":
        return sensePressure()
    elif interest.lower() == "light-on":
        return senseLight()
    elif interest.lower() == "wiper-on":
        return senseWiper()
    elif interest.lower() == "passengers-count":
        return sensePassengerCount()
    elif interest.lower() == "fuel":
        return senseFuel()
    elif interest.lower() == "engine-temperature":
        return senseEngineTemperature()

def receiveData():
        print("listening for actuation requests")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        port = PEER_PORT
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print("addr: ", addr[0])
            # print("connection: ", str(conn))
            data = conn.recv(1024)
            data = bdecode(data.decode())
            print(data, " to actuate on")
            # call actuators
            [vehicle_type, interest] = data.split('/')
            if VEHICLE_TYPE == vehicle_type:
              actuationResult = callActuator(interest)
            
            sendAck(conn, addr[0], actuationResult)
            conn.close()
            time.sleep(1)

def main():
    while True:
        receiveData();


if __name__ == '__main__':
    main()