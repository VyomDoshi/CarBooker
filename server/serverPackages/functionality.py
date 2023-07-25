import pytz
import json
from datetime import datetime
import socket
import mysql.connector

# ****************************************************************************************************
# THESE METHODS ARE THERE FOR THE FUNCTIONALITY
# ****************************************************************************************************
filePath = ""
mutex = 9998
s = socket.socket()

# ============

# setsthe file path so that its accessed by the other methods


def setFilePath(temp):
    global filePath
    filePath = temp

# ============

# This process takes the necessary parameters to connect with the database so that it can acsess afterwards from the same connection


def takepar(host, user, passwd, database):
    global cursor, mydb
    mydb = mysql.connector.connect(
        host=host, user=user, passwd=passwd, database=database)
    cursor = mydb.cursor()

# ============

# function to book the car, it reads and writes to the database


def book_car(id, count):
    global filePath, mutex, s, mydb, cursor
    string = ""
    # this is the port number for the mutex lock
    s.connect(('localhost', mutex))
    print(s.recv(1024).decode())
    if s.recv(1024).decode() == "Y":
        print(s.recv(1024).decode())
        cursor.execute(
            "SELECT EXISTS (SELECT * FROM car_details WHERE id = %s)", [id])
        for i in cursor.fetchone():
            if i == 1:
                cursor.execute(
                    "SELECT * FROM car_details WHERE id = %s", [id])
                _, _, count_db, _ = cursor.fetchone()
                if count <= count_db:
                    cursor.execute("UPDATE car_details SET quantity = %s WHERE id = %s", [
                                   count_db-count, id])
                    mydb.commit()
                    string = "The Car is booked! ENJOY your RIDE!"
                else:
                    string = "The Car is NOT booked!"
            else:
                string = "No Such Car Exists Please Try Again!"
        s.send(bytes("", "utf-8"))
        s.close()
        return string

# ============

# shows the current stats of the database


def getCurrentStatus():
    cursor.execute("SELECT * FROM car_details")
    status = cursor.fetchall()
    ans = ""
    for details in status:
        id, name, count, price = details
        ans += "id ="+str(id)+"\n"
        ans += "name ="+name+"\n"
        ans += "Quantity ="+str(count)+"\n"
        ans += "Price per KM ="+str(price)+"\n"
        ans += "\n"
    return ans

# ============

# gives the server time


def getServerTime():
    return datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%y, %H:%M:%S")
