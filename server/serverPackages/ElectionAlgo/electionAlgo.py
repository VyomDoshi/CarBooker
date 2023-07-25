import json
import socket
from time import sleep
import os
import select
import mysql.connector


# show variables like "%timeout";
# set global connect_timeout = 600;

# *****************************************************************************************
conn_list = []  # this is a global variable storing all the connections to this program
# we make a process which is run at start time
time = 3
PORT = 0
file_path = ""
mutex = 9999

host1 = ""
user1 = ""
passwd1 = ""
database1 = ""
#============

# sets the file path and port correctly
def setFilePathandPort(stringPath, port):
    global file_path, PORT
    file_path = stringPath
    PORT = port

#============

# takes the parameters used for connections to the database and clears the table for the storage of  new pid
def takepar(host, user, passwd, database):
    global cursor, mydb, host1, user1, passwd1, database1
    host1 = host
    user1 = user
    passwd1 = passwd
    database1 = database
    mydb = mysql.connector.connect(
        host=host, user=user, passwd=passwd, database=database)
    if(mydb):
        print("CONNECTION WITH DATABASE SUCCESSFULL!")
    else:
        print("CONNECTION WITH DATABASE FAILED!")
    cursor = mydb.cursor()
    

#============

# this process runs in the back ground and listens for incoming messages pertaining to elections
def start_proc():
    
    global PORT
    s = socket.socket()
    s.bind(('localhost', PORT))
    s.listen()
    # s.setblocking(False)
    inputs = [s]
    outputs = [s]
    while 1:
        # c, addr = s.accept()
        # we add this function here so that we are able to see if there are any accepting connections requests available
        s.setblocking(False)
        s.settimeout(3)
        readable, writeable, errors = select.select(
            inputs, outputs, inputs,3)
        # if we have a readable(in this case a connection request) we will accept it and go to the next step and if not we will reiterate
        for s in readable:
            conn_list.append(s.accept())
            if conn_list[-1][0].recv(1024).decode() == "Election":
                print(
                    "Some lower pid proccess has told me that elections are taking place so I am going to continue it!!")
                # sends the ok message to the other processes so that they dont have to do anything
                conn_list[-1][0].send(bytes("OK", "utf-8"))
                # we now break the connection as the work is over
                conn_list[-1][0].close()
                # conn_list.remove(-1)
                count, check = bully()
                if check:
                    print("My elders have told me that they will handle the elections")
                elif count == 0:
                    print("I have no elders so I elect MYSELF TO BE THE NEW MASTER")
                    # makes itself the master if no one else is ready to take the responsibility
                    proc_store("master")

                else:
                    # makes itself the master if no one else is ready to take the responsibility
                    print(
                        "Nobody has told me anything hence I elect myself to be the Master")
                    proc_store("master")

#============

# this function implements the bully algorithm and reads the database for all the elders
def bully():  # sends the message that election is being held
    global file_path
    check = False
    count = 0
    # with open(file_path, 'r') as pid:
    #     json_object = json.load(pid)
    #     pid.close()
    # data = {}
    mypid = os.getpid()
    cursor.execute("SELECT EXISTS (SELECT * FROM pid WHERE pid>%s)", [mypid])
    for i in cursor.fetchone():
        if i>=1: # we have some elders to our processes
            count = i
            cursor.execute("SELECT * FROM pid WHERE pid>%s", [mypid])
            for data in cursor.fetchall():
                _, port_num, _ = data
                try:
                    print(f"Trying to connect to one of my elders, {data}")
                    sending = socket.socket()
                    sending.connect(('localhost', port_num))
                    print("Connected!...now sending message of election")
                    sending.send(bytes("Election", "utf-8"))
                    # so that the socket doesn't have to wait idefinitely for the message to come
                    sending.setblocking(False)
                    readable, writeable, errors = select.select(
                        [sending], [sending], [sending], 3)
                    for send in readable:
                        if(sending.recv(1024).decode() == "OK"):
                            check = True
                    sending.close()
                except Exception as e:
                    print(f"There was an Exception {e} while connecting to {data}")
        else:
            print("I have no elders so I elect MYSELF TO BE THE NEW MASTER")
            # makes itself the master if no one else is ready to take the responsibility
            proc_store("master")
    return count, check

#============

# This process stores the status of the process in the database
def proc_store(status):
    global PORT, file_path, mutex
    # data = {}
    # check = False
    # data["pid"] = os.getpid()
    # data["port"] = PORT
    # data["status"] = status
    # We are now trying to make a mutex lock so that  while we edit no body can edit
    m = socket.socket()
    m.connect(('localhost', mutex))
    print(m.recv(1024).decode())
    if m.recv(1024).decode() == "Y":
        print(m.recv(1024).decode() + "****from proc_store****")
        try: #checking if there is an entry for that specific process
            cursor.execute(
                "SELECT EXISTS(select * from pid where pid = %s)", [os.getpid()])
            for i in cursor.fetchone():
                if(i == 1):
                    cursor.execute(
                        "UPDATE pid SET stat = %s WHERE pid = %s", [status, os.getpid()])
                    mydb.commit()
                elif(i == 0):
                    cursor.execute(
                        "INSERT INTO pid VALUES(%s, %s, %s)", [os.getpid(), PORT, status])
                    mydb.commit()
                else:
                    print(
                        "THERE IS AN ERROR in the database more that one same pid present")
        except Exception as e:
            print(e)
        m.send(bytes("", "utf-8"))  # this is just to release the lock
        print("LEFT CRITICAL SECTION ****from proc_store****")
        
        # with open(file_path, 'r') as pid:
        #     json_object = json.load(pid)
        #     print(json_object)
        #     pid.close()
        # try:
        #     for temp in json_object:
        #         if temp["pid"] == data["pid"] and temp["port"] == data["port"]:
        #             temp["status"] = data["status"]
        #             check = True
        #             break
        #     if not check:
        #         json_object.append(data)
        #     with open(file_path, 'w') as pid_write:
        #         pid_write.write(json.dumps(json_object, indent=4))
        #     pid_write.close()

#============

# RETURNS WHETHER OR NOT A SERVER IS MASTER
def is_master():
    cursor.execute(
        "SELECT EXISTS(SELECT * FROM pid WHERE pid = %s AND stat = %s)", [os.getpid(), "master"])
    for i in cursor.fetchone():
        if(i == 1):
            return True
        elif(i == 0):
            return False
        else:
            print("THERE IS AN ERROR in the database more that one same pid present")

# ============

# This process tells us whether or not any master exists in the data base
def master_selected():
    global host1, user1, passwd1, database1
    while True:
        mydbtemp = mysql.connector.connect(host=host1, user=user1, passwd=passwd1, database=database1)
        if(mydbtemp):
            print("CONNECTION WITH DATABASE SUCCESSFULL!")
        else:
            print("CONNECTION WITH DATABASE FAILED!")
        cursortemp = mydbtemp.cursor()
        cursortemp.execute(
            "SELECT EXISTS(SELECT * FROM pid WHERE stat = %s)", ["master"])
        for i in cursortemp.fetchone():
            if(i == 1):
                print("Master found in the database")
                return True
            elif(i == 0):# no master in the database
                print("master not yet found")
                continue
            else:
                print("THERE IS AN ERROR in the database more that one same pid present")
        sleep(3)
