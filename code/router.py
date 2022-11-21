
import selectors
import socket
import threading
import time
import types

PEER_PORT = 33301    # Port for listening to other peers
BCAST_PORT = 33334   # Port for broadcasting own address
INTEREST_PORT = 33310

map_dict = {}


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()

    def broadcastIP(self):
        """Broadcast the host IP."""
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.settimeout(0.5)
        message = f'HOST {self.host} PORT {self.port}'.encode('utf-8')
        print("What is the message", message)
        while True:
            server.sendto(message, ('<broadcast>', BCAST_PORT))
            # print("Host IP sent!")
            print("Broadcasting my IP {}:{}".format(self.host,self.port))
            time.sleep(10)


    def updatePeerList(self):
        """Update peers list on receipt of their address broadcast."""
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(("", BCAST_PORT))
        while True:
            data, _ = client.recvfrom(1024)
            print("received message:", data.decode('utf-8'))
            data = data.decode('utf-8')
            dataMessage = data.split(' ')
            command = dataMessage[0]
            if command == 'HOST':
                host = dataMessage[1]
                port = int(dataMessage[3])
                if len(dataMessage) > 5:
                    action = dataMessage[5]
                else:
                    action = ''
                # host = dataMessage[1]
                # port = int(dataMessage[3])
                peer = (host, port, action.lower())
                if peer != (self.host, self.port, action) and peer not in self.peers:
                    self.peers.add(peer)
                    print('Known vehicles:', self.peers)
                    self.maintain_router()
            time.sleep(2)
    

    def parse_interest(self, interest):
        inter = interest.split("/")
        return inter[len(inter)-1]
    

    def filter_ips(self,data):
        if data in map_dict.keys():
            return map_dict[data]
    

    def receiveData(self):
        """Listen on own port for other peer data."""
        print("listening for interest data")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        port = INTEREST_PORT
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print("addr: ", addr[0])
            print("connection: ", str(conn))
            data = conn.recv(1024)
            data = data.decode('utf-8')
            print(data, " to actuate on")
            interset = self.parse_interest(data.lower())
            print("Final interset", interset)
            filtered_ips =  self.filter_ips(interset)
            ack = self.route_to_pi(filtered_ips,interset)
            self.send_back_to_interested_node(ack, addr[0],conn)
            # call actuators
            # sendAck(addr[0], actuationResult)
            conn.close()
            time.sleep(1)

    def send_back_to_interested_node(self, message, host, conn):

        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((host,INTEREST_PORT))
        msg = message
        print("Idhar aaya kya", msg)
        conn.send(msg)
        print("Sent command", msg)
        return

    def remove_node(self, node, command):
        try:
            print("REMOVING NODE", node)
            if node in map_dict[command]:
                map_dict[command].remove(node)
            print("UPDATED MAP DICT", map_dict)
        except:
            print("ERROR IN REMOVING NODE")



    def route_to_pi(self,peer_list,command):
        """Send sensor data to all peers."""
        sent = False
        # if command == 'ALERT':
        print("What is peer list and command :{} {}".format(peer_list,command))
        for peer in peer_list:
            print("What is peer inside peerlist", peer)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((peer,PEER_PORT))
                msg = command
                print("Idhar aaya kya", msg)
                s.send(msg.encode())
                print("Sent command", msg)
                sent = True
                ack = s.recv(1024)
                print("Acknowledgement received", ack)
                s.close()
                return ack
            except Exception:
                print("An exception occured")
                continue
                #self.remove_node(peer,command)
                

    def maintain_router(self):
        empty_set = set()
        count = 1
        for peer in self.peers:
            # print("No of iterations", count)
            # print("Inside peer", peer)
            host = peer[0]
            # print("Inside host",host)
            port = peer[1]
            action = peer[2]
            # print("Inside action", action)
            
            if action in map_dict.keys():
                temp_set = map_dict[action]
                temp_set.add(host)
                map_dict[action] = temp_set


            else:
                empty_set.add(host)
                map_dict[action] = empty_set
            count+=1
        print("What is router table now", map_dict)


def main():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    peer = Peer(host, PEER_PORT)
    
    t1 = threading.Thread(target=peer.updatePeerList)
    t2 = threading.Thread(target=peer.receiveData)
    t1.start()
    time.sleep(15)
    t2.start()


if __name__ == '__main__':
    main()
