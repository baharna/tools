#!/usr/bin/python

# To do: add error handling and close out

import threading
import SocketServer

class EchoHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        print "Got a connection from: ", self.client_address
        data = "stuff"
        cur_thread = threading.current_thread()

        while len(data):
            data = self.request.recv(2048)
            print "Received from thread " + cur_thread.name + ": " + data
            self.request.send(data)

        print "Client exited: ", self.client_address

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def main():

    serverAddr = ("0.0.0.0", 9001)

    server = ThreadedTCPServer(serverAddr, EchoHandler)

    server.serve_forever()

if __name__ == '__main__':
    main()
