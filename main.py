import socket,threading,os,random,re,sys,subprocess,requests
from math import floor

# official rac servak 91.192.22.20:42666
VERSION = "1.99"
MOTDS = [
    "also try bRAC",
    "also try Mefedroniy",
    "clRAC is bullshit.",
    "i hate mr.sugoma",
    "what is rac??",
    "give me money $_$",
    "check out RAC-Hub!",
    "idk what to type here",
    "this is motd.",
    "respects user-agents!",
    "supports rac v1.99.2",
    "rac v2 support soon",
    "i want to make iRAC",
    "also see README.md",
    "i love luckyserv",
    "what shto",
    "made in russia",
    "made with love",
    "made not in china",
    "build from source!",
    "licensed with GPL-3.0",
    "WRAC support soon",
    "next update is 1.99+0.5-½*3.14",
    "crack at home:"
]

last_size = 0

NICKNAME = ""
IP = ""
PORT = 0

def filter_ansi(text):
    return re.sub(r'\x1b\[[0-9;?]*[A-DF-HJ-Z]', '', text)

def random_motd(): return random.choice(MOTDS).strip()

def center(text):
    probels = 55-len(text)
    phalf = floor(probels/2)-1
    return " "*phalf+'\"'+text+'\"'

def check_update():
    print("[cRACk] checking for updates...")
    try:
        r = requests.get("https://api.github.com/repos/pansangg/cRACk/releases/latest").json()
        if r["tag_name"].lstrip('v') > VERSION:
            print(f"\033[92m[cRACk] update {r["tag_name"]} available! https://github.com/pansangg/cRACk/releases/latest\033[0m")
        else:
            print(f"\033[92m[cRACk] you're using latest version of cRACk.\033[0m")
    except:
        print("[cRACk] unable to check for updates.")

def useragentize(text):
    text = re.sub("\uB9AC\u3E70<(.*?)> (.*)", r"\033[32m<\1> \2\033[0m", text) # bRAC
    text = re.sub("\u2550\u2550\u2550<(.*?)> (.*)", r"\033[91m<\1> \2\033[0m", text) # CRAB
    text = re.sub("\u00B0\u0298<(.*?)> (.*)", r"\033[95m<\1> \2\033[0m", text) # Mefidroniy
    text = re.sub("\u2042<(.*?)> (.*)", r"\033[1;33m<\1> \2\033[0m", text) # cRACk
    # text = re.sub("<(.*?)> (.*)", r"\033[46m<\1> \2\033[0m", text) // no clRAC support sorry =[
    return text

def sendmsg(text):
    global IP,PORT,last_size
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((IP, PORT))
    # text = re.sub(pattern=r"\{[^}]*\}\s", string=text, repl=" ")
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

            new_data = new_data.decode("utf-8", errors="replace")
            print(filter_ansi(useragentize(new_data)))
        elif data_size < last_size:
            sock.send(b'\x00')

            data_size = sock.recv(1024)
            last_size = int(data_size.split(b'\x00', 1)[0].decode())

            sock.send(b'\x01')
            full = b''

            while True:
                part = sock.recv(4096)
                if not part:
                    break
                full += part

            dfull = full.decode("utf-8", errors="ignore")
            print(useragentize(dfull))

def listen_client():
    while True:
        try:
            newmsg = input("")
            if (newmsg != ""): sendmsg(f"\r⁂<{NICKNAME}> {newmsg}"+" "*50)
        except Exception as e:
            print(f"[cRACk] exception said to exit, bye!")
            os._exit(1)
            break

def hello():
    global IP,PORT,NICKNAME

    print(f'''
\033[1;33m        `7MM"""Mq.        db       .g8"""bgd `7MM
          MM   `MM.      ;MM:    .dP'     `M   MM
  ,p6"bo  MM   ,M9      ,V^MM.   dM'       `   MM  ,MP'
 6M'  OO  MMmmdM9      ,M  `MM   MM            MM ;Y
 8M       MM  YM.      AbmmmqMA  MM.           MM;Mm
 YM.    , MM   `Mb.   A'     VML `Mb.     ,'   MM `Mb.
  YMbmd'.JMML. .JMM..AMA.   .AMMA. `"bmmmd'  .JMML. YA
\033[1;37m ------------------------------------------------------
                \033[1;33mc\033[0mlient for \033[1;33mRAC\033[0m \033[1;33mk\033[0mettles
\x1b[3m{center(random_motd())}\x1b[0m

              version \033[1;33m1.99\033[0m | by \033[1;33mpansangg\033[0m
          https://github.com/pansangg/cRACk
''')
    check_update()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    NICKNAMEINPUT = input("nickname (empty for random): ")
    if (NICKNAMEINPUT == ""):
        NICKNAME = str(random.randint(1000, 9999))+"@cRACk"
    else:
        NICKNAME = NICKNAMEINPUT

    while True:
        IPPORTNOTSPLITTED = input("ip:port (empty for default): ")
        if ":" in IPPORTNOTSPLITTED or IPPORTNOTSPLITTED == "": break
        print("[cRACk] wrong syntax! please type ip:port")
    if (IPPORTNOTSPLITTED == ""):
        IP = "91.192.22.20"
        PORT = 42666
        print("[cRACk] default is 91.192.22.20:42666")
    else:
        IP,PORT = IPPORTNOTSPLITTED.split(":", 1)
        PORT = int(PORT)

    print("[cRACk] connecting...")
    try:
        sock.connect((IP, PORT))
    except:
        print("[cRACk] can't connect to the host!")
        os._exit(1)

    print("[cRACk] 0x00ing...")
    sock.send(b'\x00')

    data_size = sock.recv(1024)
    global last_size
    last_size = int(data_size.split(b'\x00', 1)[0].decode())

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
    print(filter_ansi(useragentize(dfull)))
    threading.Thread(target=listen_client).start()
    threading.Thread(target=chunked_reading).start()

# async def msging():
#     loop = asyncio.get_event_loop()
#     while True:
#         msg = input("message: ")
#         s.send(b'\x01'+msg.encode("utf-8"))

hello()
# with keyboard.Listener(on_press=leave_sharavar) as listener: listener.join()
threading.Event().wait()