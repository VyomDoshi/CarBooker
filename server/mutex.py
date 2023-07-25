# import socket
# import threading

# PORT_PID = 9999 #will be used to listen for making chaneges to the PID file
# PORT_func = 9998  # will be used to listen for making chaneges to the Car Details file
# s = socket.socket()
# s.bind(('localhost', PORT_PID))
# s.listen()
# waitingList_PID = []
# readinglist_PID = []

# s1 = socket.socket()
# s1.bind(('localhost', PORT_func))
# s1.listen()
# waitingList_func = []
# readinglist_func = []
# # *************************THE FIRST 3 FUNCTIONS ARE FOR PID*************************
# def inCriticalSection_PID():
#   print("function inCriticalSection started!")
#   while 1:
#     if len(waitingList_PID) > 0:
#       c, addr = waitingList_PID[0]
#       if len(readinglist_PID)>0:#there is someone who is trying to read the data
#         stopReading_PID()
#       print(f"Process {addr} is now in critical section:")
#       c.send(bytes("Y", "utf-8"))
#       c.send(bytes("you are now in critical section! send all the messages that you want to, press enter to exit!", "utf-8"))
#       while 1:
#         mssg = c.recv(1024).decode()
#         print(mssg)
#         if(mssg == ""):
#           break
#       waitingList_PID.pop(0)
#       print(f"Process {addr} has now left the critical section!")
#       print()

# def stopReading_PID():#to tell the processe to stop reading as one of the processes is about to write
#   print("TELLING READING PROCESSES TO STOP")
#   for (c, addr) in readinglist_PID:
#     c.send(bytes("Stop", "utf-8"))
#     c.close()
#     readinglist_PID.remove((c, addr))


# def contact_PID():
#  print("function contact started!")
#  while 1:
#   c, addr = s.accept()
#   temp = c.recv(1024).decode()
#   if temp == "w":
#     waitingList_PID.append((c, addr))
#   elif temp == "":
#     readinglist_func.remove((c, addr))
#     continue
#   elif len(waitingList_PID) == 0:
#     readinglist_PID.append((c, addr))
#   # print(f"Got a connection: {waitingList_PID[-1][1]}")
#   c.send(bytes("You are clear to READ ONLY", "utf-8"))

# # *************************THE NEXT 3 FUNCTIONS ARE FOR Functionality part*************************
# def inCriticalSection_func():
#   print("function inCriticalSection started!")
#   while 1:
#     if len(waitingList_func) > 0:
#       c, addr = waitingList_func[0]
#       if len(readinglist_func) > 0:  # there is someone who is trying to read the data
#         stopReading_func()
#       print(f"Process {addr} is now in critical section:")
#       c.send(bytes("Y", "utf-8"))
#       c.send(bytes("you are now in critical section! send all the messages that you want to, press enter to exit!", "utf-8"))
#       while 1:
#         mssg = c.recv(1024).decode()
#         print(mssg)
#         if(mssg == ""):
#           break
#       waitingList_PID.pop(0)
#       print(f"Process {addr} has now left the critical section!")
#       print()


# def stopReading_func():  # to tell the processe to stop reading as one of the processes is about to write
#   print("TELLING READING PROCESSES TO STOP")
#   for (c, addr) in readinglist_func:
#     c.send(bytes("Stop", "utf-8"))
#     c.close()
#     readinglist_func.remove((c, addr))

# def contact_func():
#  print("function contact started!")
#  while 1:
#   c, addr = s1.accept()
#   temp = c.recv(1024).decode()
#   if temp == "w":
#     waitingList_func.append((c, addr))
#   elif temp == "":
#     readinglist_func.remove((c,addr))
#     continue
#   elif len(waitingList_func) == 0:
#     readinglist_func.append((c, addr))
#   # print(f"Got a connection: {waitingList_func[-1][1]}")
#   c.send(bytes("You are clear to READ ONLY", "utf-8"))

# if __name__ ==  '__main__':
#  t1 = threading.Thread(target=inCriticalSection_PID)
#  t2 = threading.Thread(target=contact_PID)
#  t3 = threading.Thread(target=inCriticalSection_func)
#  t4 = threading.Thread(target=contact_func)
#  t1.start()
#  t2.start()
#  t3.start()
#  t4.start()


import socket
import threading
import mysql.connector

host = "localhost"
user = "root"
passwd = "vyom@1234"
database = "db"
PORT = 9999  # will be used to listen
s = socket.socket()
s.bind(('localhost', PORT))
s.listen()
waitinglist = []


def inCriticalSection():
    print("function inCriticalSection started!")
    while 1:
        if len(waitinglist) > 0:
            c, addr = waitinglist[0]
            print(f"Process {addr} is now in critical section:")
            c.send(bytes("Y", "utf-8"))
            c.send(bytes(
                "you are now in critical section! send all the messages that you want to, press enter to exit!", "utf-8"))
            while 1:
                mssg = c.recv(1024).decode()
                print(mssg)
                if(mssg == ""):
                    break
            waitinglist.pop(0)
            print(f"Process {addr} has now left the critical section!")
            print()


def contact():
    global s
    print("function contact started!")
    while 1:
        waitinglist.append(s.accept())
        # print(f"Got a connection: {waitinglist[-1][1]}")
        waitinglist[-1][0].send(
            bytes("Please wait for your turn to access the critical section", "utf-8"))


if __name__ == '__main__':
  for i in range(1,5):
    mydb = mysql.connector.connect(
        host=host, user=user, passwd=passwd, database=(database+str(i)))
    if(mydb):
        print("CONNECTION WITH DATABASE SUCCESSFULL!")
    else:
        print("CONNECTION WITH DATABASE FAILED!")
    cursor = mydb.cursor()
    cursor.execute("TRUNCATE TABLE pid")
    mydb.close()
  t1 = threading.Thread(target=inCriticalSection)
  t2 = threading.Thread(target=contact)
  t1.start()
  t2.start()
