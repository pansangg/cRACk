import socket,threading,os

# official rac servak 91.192.22.20:42666

last_size = 0

IP = ""
PORT = 0

def sendmsg(text):
    global IP,PORT,last_size
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((IP, PORT))
    sock.send(b'\x01'+text.encode("utf-8"))
    sock.close()

def chunked_reading():
    global last_size

    while True:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        sock.send(b'\x00')

        data_size_raw = sock.recv(1024)
        data_size = int(data_size_raw.split(b'\x00', 1)[0].decode())

        if data_size > last_size:
            sock.send(b'\x02' + str(last_size).encode('ascii'))

            last_size = data_size

            new_data = b''
            while True:
                part = sock.recv(4096)
                if not part:
                    break
                new_data += part

            print(new_data.decode("utf-8", errors="ignore"))

def listen_client():
    while True:
        try:
            newmsg = input("")
            if (newmsg != ""): sendmsg(newmsg)
        except Exception:
            print(f"[cRACk] exception said goodbye")
            os._exit(1)
            break

def hello():
    global IP,PORT

    print('''
       `7MM"""Mq.        db       .g8"""bgd `7MM
         MM   `MM.      ;MM:    .dP'     `M   MM
 ,p6"bo  MM   ,M9      ,V^MM.   dM'       `   MM  ,MP'
6M'  OO  MMmmdM9      ,M  `MM   MM            MM ;Y
8M       MM  YM.      AbmmmqMA  MM.           MM;Mm
YM.    , MM   `Mb.   A'     VML `Mb.     ,'   MM `Mb.
 YMbmd'.JMML. .JMM..AMA.   .AMMA. `"bmmmd'  .JMML. YA
------------------------------------------------------
               client for RAC kettles

        version 1.0 | contributors: pansangg
 https://the-stratosphere-solutions.github.io/RAC-Hub
''')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    IPPORTNOTSPLITTED = input("ip:port (empty for default): ")
    if (IPPORTNOTSPLITTED == ""):
        IP = "91.192.22.20"
        PORT = 42666
        print("[cRACk] default is 91.192.22.20:42666")
    else:
        IP,PORT = IPPORTNOTSPLITTED.split(":", 1)
        PORT = int(PORT)

    print("[cRACk] connecting...")
    sock.connect((IP, PORT))

    print("[cRACk] 0x00ing...")
    sock.send(b'\x00')

    data_size = sock.recv(1024)
    global last_size
    last_size = int(data_size.split(b'\x00', 1)[0].decode())
    print("data_size в первый раз: "+str(last_size))

    print("[cRACk] asking for messages...")
    sock.send(b'\x01')
    full = b''
    print("[cRACk] receiving messages...")
    while True:
        part = sock.recv(4096)  # 4096 — размер буфера, можно изменить
        if not part:
            break
        full += part

    print("[cRACk] we'll meet again")
    dfull = full.decode("utf-8", errors="ignore")
    print(dfull)
    threading.Thread(target=listen_client).start()
    threading.Thread(target=chunked_reading).start()

# async def msging():
#     loop = asyncio.get_event_loop()
#     while True:
#         msg = input("message: ")
#         s.send(b'\x01'+msg.encode("utf-8"))

hello()
threading.Event().wait()