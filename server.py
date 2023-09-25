#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #Get method and path
        method, requestPath = self.data.split()[0], self.data.split()[1]
        print("Path: ", requestPath)

        #Don't allow exiting www
        if(b"/.." not in requestPath):

            #Check proper method
            if (method == b"GET"):

                try:

                    #If directory requested
                    if (requestPath.endswith(b'/')):

                        #Read directory index.html
                        fileData = open("www" + requestPath.decode("UTF-8") + "index.html", 'r')
                        outputData = fileData.read()
                        fileData.close()

                        #Build response
                        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: Closed\n\n' + outputData

                    #If file requested
                    else:

                        if b'.html' in requestPath:

                            #Read path
                            fileData = open("www" + requestPath.decode("UTF-8"), 'r')
                            outputData = fileData.read()
                            fileData.close()

                            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: Closed\n\n' + outputData

                        elif b'.css' in requestPath:

                            #Read path
                            fileData = open("www" + requestPath.decode("UTF-8"), 'r')
                            outputData = fileData.read()
                            fileData.close()

                            response = 'HTTP/1.1 200 OK\nContent-Type: text/css\nConnection: Closed\n\n' + outputData

                        #If something besides a directory or file is requested
                        else:

                            #Check for redirect
                            if (requestPath == b"/deep"):
                                
                                response = 'HTTP/1.1 301 Moved Permanently\nLocation: /deep/\nConnection: Closed\n\n'

                            else:
                                
                                #Something strange, try to read path
                                fileData = open("www" + requestPath.decode("UTF-8"), 'r')
                                outputData = fileData.read()
                                fileData.close()

                                response = 'HTTP/1.1 200 OK\nConnection: Closed\n\n' + outputData


                except IOError as e:

                    print(e)
                    response = 'HTTP/1.1 404 Not Found\nContent-Type: text/html\nConnection: Closed\n\n<html><head></head><body><h1>404 Not Found</h1></body></html>'

            else:

                response = 'HTTP/1.1 405 Method Not Allowed\n\n<html><head></head><body><h1>405 Method Not Allowed</h1></body></html>'

        else:

            response = 'HTTP/1.1 404 Not Found\n\n'

        #Display response and send
        print("Sending Response: ", response)
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
