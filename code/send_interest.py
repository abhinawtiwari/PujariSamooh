#!/usr/bin/env python3

import argparse
import random
import selectors
import socket
import time
import types



def sendData(command):
        """Send sensor data to all peers."""
        sent = False
        # if command == 'ALERT':
        hardcodedPeers = {('10.35.70.34', 33301), ('10.35.70.31', 33301)}
        for peer in hardcodedPeers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(peer)
                msg = command
                s.send(msg.encode())
                sent = True
                s.close()
            except Exception:
                print("An exception occured")
        if sent:
            print("Sensor data sent to known vehicles")

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--command', help='Type of sensor', required=True)
    # args = parser.parse_args()
    command_name = ['vehicle/speed', 'vehicle/proximity', 'vehicle/tyre/pressure']
    while True:
        for c in command_name:
            time.sleep(10)
            sendData(c)
        time.sleep(5)
    # port_table = {'VehiclePort': 33401}  # Hardcoded port table for testing
    # port = port_table['VehiclePort']     # The port used by the server

    # sendData(command_name)
    # initial_message = sensorType + " 1"
    # byte_messages = [initial_message.encode('UTF-8')]

    # The server's hostname or IP address
    # host = socket.gethostbyname(socket.gethostname())


if __name__ == '__main__':
    main()