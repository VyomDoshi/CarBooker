import socket
from xmlrpc.client import ServerProxy

# ***********************************************************************************
# THESE FUNCTIONS ARE INCLUDED FOR FUNCTIONALITY:
# ***********************************************************************************

def book(PORT):
    # get server proxy
    carBooker = ServerProxy("http://localhost:"+PORT)
    print(f"Connected to Server: {int(PORT)-8090}")
    # Print Server Time
    print("SERVER ENTERING TIME: ", carBooker.getServerTime())
    while(True):
        # we initially print the current status of the cars in the system
        print("\n***************************************************\n***************************************************")
        print("The current status is:")
        print(carBooker.getCurrentStatus())
        print()
        print()
        print()
        print("Intermediate time: ", carBooker.getServerTime())
        print("***************************************************\n***************************************************")
        if(input("Press any character to continue the process or press enter to exit: ") != ""):
            # get car id, using split method to be able to multiple inputs
            id = int(input("Enter respective id of the car you wish to book: "))
            count = int(
                input("Enter respective number of the cars you wish to book: "))
            print(f"Status: {carBooker.book_car(id, count)}")
        else:
            print("SERVER EXIT: ", carBooker.getServerTime())
            break


# Driver function
if __name__ == '__main__':
    s = socket.socket()
    s.connect(('localhost', 8000))
    PORT = s.recv(1024).decode()
    book(PORT)
