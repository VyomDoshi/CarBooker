import threading
from time import sleep
from xmlrpc.server import SimpleXMLRPCServer
from serverPackages import functionality as fun
from serverPackages.ClockSync import clientClockSync as ccs, serverClockSync as scs
from serverPackages.ElectionAlgo import electionAlgo as ea
PORT = 8003
data_con_port = 8083
pid_path = "D:\VYOM\College\SEM 5\DC\data consistency\server\pid.json"
car_details_path = "D:\VYOM\College\SEM 5\DC\data consistency\server\carDetails3.json"
host = "localhost"
user = "root"
passwd = "vyom@1234"
database = "db3"

# Driver function
if __name__ == '__main__':
    # initially we start the server so that the user can access the functionality
    s_s = SimpleXMLRPCServer(("localhost", 8093))
    print("The XML RPC Server is up and running!")
     # ALL OTHER FUNCTIONALITY RELATED TO CAR BOOKING
    s_s.register_function(fun.getServerTime)
    s_s.register_function(fun.book_car)
    s_s.register_function(fun.getCurrentStatus)
    fun.takepar(host, user, passwd, database)
    ea.takepar(host, user, passwd, database)
    # then we run this so that the process gets stored in the json file
    fun.setFilePath(car_details_path)
    ea.setFilePathandPort(pid_path, PORT)
    ea.proc_store("slave")
    tb = threading.Thread(target=ea.start_proc)
    tb.start()  # we then keep running the election process in the background
    # Trigger the Clock Server
    if ea.master_selected():
        pass
    print("now moving on to clock synchronisation")
    if ea.is_master():
        t1 = threading.Thread(target=scs.initiateClockServer, args=[8080])
    else:
        t1 = threading.Thread(target=ccs.initiateSlaveClient, args=[8080])

    t1.start()  # start time synchronisation based on the role
    print("started to synchronize time")
    # running the server forever so that it can listen continuouly
    s_s.serve_forever()