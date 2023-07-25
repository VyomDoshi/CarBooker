import socket

PORT = [8091, 8092, 8093, 8094] #port numbers of the servers

def roundRobin_algorithm():
 global PORT
 s= socket.socket()
 s.bind(('localhost', 8000))
 s.listen()
 i=-1
 while True:
  i += 1
  i = i % len(PORT)
  c, addr = s.accept()
  c.send(bytes(str(PORT[i]), "utf-8"))
  c.close()

if __name__ == '__main__':
 roundRobin_algorithm()