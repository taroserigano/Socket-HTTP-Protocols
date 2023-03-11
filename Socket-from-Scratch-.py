# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# (Internet address family for IPv4. socket type for TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect((HOST, PORT))    # connect to server 
    s.sendall(b"Hello, world") # send everyone 
    data = s.recv(1024)   # read the server's reply 

print(f"Received {data!r}")


# echo-server.py 

    
# (Internet address family for IPv4. socket type for TCP)
with s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    # you’re using socket.AF_INET (IPv4). So it expects a two-tuple: (host, port).
    # host can be a hostname or AP address
    # port is TCP port for connection with clients 
    s.bind((self.host, self.port)) 
    
    # enables a server to accept connections by making server a listening socker 
    # It specifies the number of unaccepted connections that the system will allow before refusing new connections
    s.listen(5) 
    print("listening at ", s.getsockname())
    
    # The .accept() method blocks execution and waits for an incoming connection. When a client connects, it returns a new socket object representing the connection and a tuple holding the address of the client. The tuple will contain (host, port) for IPv4 connections or (host, port, flowinfo, scopeid) for IPv6.
    
    conn, addr = s.accept() # accepts incoming connection from cllient 
    # socket connection obj | IPv4 or 6 
    
    # use this conn(socket obj) to start communicate 
    with conn: 
        print(f "Connected by {addr}") 
        
        while True: 
            data = conn.recv(1024)  # read the response 
            
            if not data:
                break 
            
            conn.sendall(data) 

Client:             
$ python echo-client.py 
Received b'Hello, world'            

Server: 
$ python echo-server.py 
Connected by ('127.0.0.1', 64623)



HANDLING MULTIPLE CONNECTIONS 


# multiconn-server.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# ...

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")

# Calls made to this socket will no longer block / fails 
lsock.setblocking(False)

# To store whatever arbitrary data you’d like along with the socket, you’ll use data. It’s returned when .select() returns. You’ll use data to keep track of what’s been sent and received on the socket.
sel.register(lsock, selectors.EVENT_READ, data=None)


try:
    while True:
        events = sel.select(timeout=None) # no timeout 
                                    # gets events 
        
        for key, mask in events: 
            if key.data is None:
                accept_wrapper(key.fileobj) # accept the data 
            else: # there IS data 
                service_connection(key, mask) # process the data 
                
            # If key.data is not None, then you know it’s a client socket that’s already been accepted, and you need to service it. service_connection() is then called with key and mask as arguments, and that’s everything you need to operate on the socket.
                
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read / accept 
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)    # set as non-blocking mode 
    data = types.SimpleNamespace(addr=addr, inbound=b"", outbound=b"")
    # switch if event is read or write when connection with
    # client is established 
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


# handle multi-connection server 
def service_connection(key, mask): 
    # key is the socket object 
    # mask is the event (that is ready)  
    
    sock = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ: # if the event is ready for READ,  
        recv_data = sock.recv(1024)  # retrieve the data 
        if recv_data:                # if there's the data 
            data.outb += recv_data   # accumulate it 
        else:                        # if data is empty, 
                                     # client closed the connection
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)     # remove from select monitor 
            sock.close()             # close connection 
            
    if mask & selectors.EVENT_WRITE: # socket is ready for WRITE 
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # send to client 
            data.outb = data.outb[sent:] # remove the sent part from the entire data.outb 

































































        
    
    























