import datetime
import socket
import threading
from dateutil import parser
import time
#****************************************************************************************************
# THIS IS THE CLIENT SIDE OF THE CLOCK SYNCHRONISATION ( Will be used if this server is not elected as the master node )
#****************************************************************************************************

# client thread function used to send time at client side
def startSendingTime(slave_client):

    while (True):
        # provide server with clock time at the client
        slave_client.send(str(datetime.datetime.now()).encode())
        # print("Recent time sent successfully", end="\n\n")
        time.sleep(5)


# client thread function used to receive synchronized time
def startReceivingTime(slave_client):

    while True:
        # receive data from the server
        Synchronized_time = parser.parse(slave_client.recv(1024).decode())
        print("Synchronized time at the client is: " +
              str(Synchronized_time), end="\n\n")


# function used to Synchronize client process time
def initiateSlaveClient(port=8080):

    slave_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the clock server on local computer
    slave_client.connect(('localhost', port))

    # start sending time to server
    # print("Starting to receive time from server\n")
    send_time_thread = threading.Thread(
        target=startSendingTime, args=(slave_client, ))
    send_time_thread.start()

    # start receiving synchronized from server
    # print("Starting to receiving " + "synchronized time from server\n")
    receive_time_thread = threading.Thread(
        target=startReceivingTime,
        args=(slave_client, ))
    receive_time_thread.start()
