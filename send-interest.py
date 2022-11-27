import socket
import time
import base64
import traceback
import pickle
import random 

filename = 'finalized_model.sav'

ROUTER_IP = '10.35.70.28'
ROUTER_PORT = 33310

vehicle_status_dict = {}

def prediction(input_list):
    try:
        loaded_model = pickle.load(open(filename, 'rb'))
        # [predicted_val] = loaded_model.predict([[2,91.04624672,13.92933001,26.18824997,0,0,4,1,217]])
        [predicted_val] = loaded_model.predict([input_list])
        val = int(predicted_val)
        # print(val)
        if val == 1:
            return True 
        return False
    except:
        state = [True, False]
        return random.choice(state)

def aimlPrediction(interest_packet):
    # print('starting AI/ML prediciton')
    # print(vehicle_status_dict)
    # print(list(vehicle_status_dict.values()))
    # do prediction
    
    vehicle = interest_packet.split('/')[0]

    predictionResult = prediction(list(vehicle_status_dict.values()))
    if predictionResult:
        print("\033[1;35m AI/ML prediction: ", vehicle, " needs inspection \033[0m \n")
        # print("AI/ML prediction: ", vehicle, " needs inspection")
    else:
        print("\033[1;35m AI/ML prediction: ", vehicle, " does not need inspection \033[0m \n")
        # print("AI/ML prediction: ", vehicle, " does not need inspection")

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

def actuate(interest_packet, data_packet):
    print("Data packet received: ", data_packet, ' for interest packet ', interest_packet)
    if interest_packet == 'truck/speed':
        print('Truck approaching at speed ', data_packet, ' km/h')
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'truck/proximity':
        print('Truck is near at ', data_packet, ' metres')
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'truck/pressure':
        print('Truck tyre pressure is at ', data_packet, ' psi')
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'truck/light-on':
        print('Truck light is ', data_packet)
        feature = interest_packet.split('/')[1]
        val = 0
        if data_packet == 'on':
            val = 0
        elif data_packet == 'off':
            val = 1
        else:
            val = 2
        vehicle_status_dict[feature] = val
    elif interest_packet == 'truck/wiper-on':
        print('Truck wiper is ', data_packet)
        feature = interest_packet.split('/')[1]
        val = 0
        if data_packet == 'on':
            val = 0
        elif data_packet == 'off':
            val = 1
        else:
            val = 2
        vehicle_status_dict[feature] = val
    elif interest_packet == 'truck/passengers-count':
        print('Truck is approaching with ', data_packet, ' number of passengers')
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'truck/fuel':
        print('Truck is approaching with fuel at ', data_packet)
        feature = interest_packet.split('/')[1]
        val = 0
        if data_packet == 'low':
            val = 0
        elif data_packet == 'medium':
            val = 1
        else:
            val = 2
        vehicle_status_dict[feature] = val
    elif interest_packet == 'truck/engine-temperature':
        print('Truck is appraoching with engine temperature of ', data_packet, ' degree Fahrenheit')
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/speed':
        print('Bike is appraoching with speed of ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/proximity':
        print('Bike is appraoching with proximity of ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/pressure':
        print('Bike is appraoching with tyre pressure of ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/light-on':
        print('Bike is appraoching with headlight ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/wiper-on':
        print('Bike is appraoching with wiper ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/passengers-count':
        print('Bike is appraoching with passengers count ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/fuel':
        print('Bike is appraoching with fuel quantity ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet
    elif interest_packet == 'bike/engine-temperature':
        print('Bike is appraoching with engine temperature of ', data_packet)
        feature = interest_packet.split('/')[1]
        vehicle_status_dict[feature] = data_packet

    if len(vehicle_status_dict) >= 8:
        # print("\033[1;32;40m Bright Green  \n")
        # print("\033[1;35;40m Bright Magenta  \n")
        print("\033[1;32m \n *** Sending data for AI/ML prediction ***  \033[0m \n")
        # print('\n *** Sending data for AI/ML prediction ***')
        aimlPrediction(interest_packet)
    
def sendInterest(interest):
        routers = {(ROUTER_IP, ROUTER_PORT)}
        print('attempting to send interest packet: ', interest)
                
        for router in routers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(router)
                base64encoded = str(bencode(interest))
                s.send(base64encoded.encode())
                ack = s.recv(1024)
                actuate(interest, bdecode(ack.decode('utf-8')))
                s.close()
            except Exception:
                print(traceback.format_exc())
                print("An exception occured")

def main():
    truck_interest_packets = ['truck/speed', 'interest/corrupted', 'truck/proximity', 'truck/pressure', 'truck/light-on', 'truck/wiper-on', 'truck/passengers-count', 'truck/fuel', 'truck/engine-temperature']
    bike_interest_packets = ['bike/speed', 'interest/corrupted', 'bike/proximity', 'bike/pressure', 'bike/light-on', 'bike/wiper-on', 'bike/passengers-count', 'bike/fuel', 'bike/engine-temperature']
    car_interest_packets = ['car/speed', 'interest/corrupted', 'car/proximity', 'car/pressure', 'car/light-on', 'car/wiper-on', 'car/passengers-count', 'car/fuel', 'car/engine-temperature']
    
    print("\n \033[1;35m *** Secure zone vehicular inspection system *** \033[0m \n")

    while True:
        print('\n')
        print('Press 1 to send truck interest packets')
        print('Press 2 to send bike interest packets')
        print('Press 3 to send car interest packets\n')
        val = input()
        vehicle_status_dict.clear()

        if val == '1':
            for c in truck_interest_packets:
                print('press 1 to send next packet, press 2 to change vehicle type')
                inp = input()
                if inp != '1':
                    vehicle_status_dict.clear()
                    break
                sendInterest(c)
                print('\n')
        elif val == '2':
            for c in bike_interest_packets:
                print('press 1 to send next packet, press 2 to change vehicle type')
                inp = input()
                if inp != '1':
                    vehicle_status_dict.clear()
                    break
                sendInterest(c)
                print('\n')
        elif val == '3':
            for c in car_interest_packets:
                print('press 1 to send next packet, press 2 to change vehicle type')
                inp = input()
                if inp != '1':
                    vehicle_status_dict.clear()
                    break
                sendInterest(c)
                print('\n')

if __name__ == '__main__':
    main()
