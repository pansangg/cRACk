import socket,threading,os,random,re,requests,time,toml,sys

with open('config.toml', 'r') as f:
    c = toml.load(f)

# VERSION = "2.0ь"
VERSION = "1.99.288"
MOTDS = [
    "also try bRAC",
    "also try Mefedroniy",
    "clRAC is bullshit.",
    "i hate mr.sugoma",
    "what is rac??",
    "check out RAC-Hub!",
    "idk what to type here",
    "this is motd.",
    "respects user-agents!",
    "supports rac v1.99.2",
    "rac v2 support soon",
    "i want to make iRAC",
    "also see README.md",
    "i love luckyserv",
    "what shto blin",
    "made in russia",
    "made with love",
    "made not in china",
    "build from source!",
    "licensed with GPL-3.0",
    "WRAC support never",
    "next update is 2.99alpha+0.5-½*3.14",
    "cracking crack is bannable",
    "crack-unbloated is also good",
    "homemade nuggets",
    "i know where do you live now.",
    "your ip is 127.0.0.1",
    "rarest motd real not fake",
    "no bloatware! (maybe)",
    "doesn't respect mr.sugoma",
    "respects Forbirdden",
    "respects MeexReay",
    "made at home",
    "respects OctoBanon",
    "support: +74959528833",
    "filters ANSI",
    "checks updates",
    "deleting system...",
    "best RAC client ever (real)",
    "stealing passwords...",
    "author is heterogay",
    "shitcoded with love",
    "free robux: pansangg.github.io",
    "thanks camp3rcraft",
    "shRACk soon",
    "also try cRACk-unbloated",
    "star the cRACk repository!"
]
ASCIIART = '''
\033[1;33m        `7MM"""Mq.        db       .g8"""bgd `7MM
          MM   `MM.      ;MM:    .dP'     `M   MM
  ,p6"bo  MM   ,M9      ,V^MM.   dM'       `   MM  ,MP'
 6M'  OO  MMmmdM9      ,M  `MM   MM            MM ;Y
 8M       MM  YM.      AbmmmqMA  MM.           MM;Mm
 YM.    , MM   `Mb.   A'     VML `Mb.     ,'   MM `Mb.
  YMbmd'.JMML. .JMM..AMA.   .AMMA. `"bmmmd'  .JMML. YA\033[1;37m
'''

last_size = 0

NICKNAME = ""
IP = ""
PORT = 0

def filter_ansi(text):
    return re.sub(r'\x1b\[[0-9;?]*[A-DF-HJ-Z]', '', text)

def valid_host(s):
    import re
    return bool(re.fullmatch(r'((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d):([1-9]\d{0,4})', s)) and 0 < int(s.rsplit(':',1)[1]) < 65536

def random_motd(): return random.choice(MOTDS).strip()

def center(text):
    probels = 55-len(text)
    phalf = int(probels/2)-1
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
    return text

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

def oobe():
    print("\n"*100)
    print(f'''
 {ASCIIART}
 ------------------------------------------------------
             version \033[1;33m{VERSION}\033[0m | by \033[1;33mpansangg\033[0m
          https://github.com/pansangg/cRACk

''')
    print("[cRACk] hello! looks like its your \033[1;33mfirst time using cRACk\033[0m. lets configure it for you!")
    print("[cRACk] note: if you want to \033[1;33mchange something\033[0m, start \033[1;33mcRACk with --reset or -r argument\033[0m.\n")

    password = ""

    while True:
        nickname = input("[cRACk] choose your nickname (leave empty for manual entry): ")
        if nickname == "":
            print("[cRACk] great! you are entering nickname \033[1;33mmanually\033[0m from now.")
            break
        elif nickname != "" and not nickname.isspace():
            print(f"[cRACk] great! your nickname is \033[1;33m{nickname}\033[0m now.")
            break
        print("[cRACk] nickname can't be only whitespaces")
    while True:
        auth = input("[cRACk] enable auth? (y/n, default:n): ")
        if auth.lower() == "y":
            print(f"[cRACk] great! auth is \033[1;33menabled\033[0m now.")
            auth = True
            break
        elif auth.lower() == "n" or auth == "":
            print("[cRACk] great! auth is \033[1;33mdisabled\033[0m.")
            auth = False
            break
        print("[cRACk] choose y or n")
    if auth and nickname != "" and not nickname.isspace():
        while True:
            password = input("[cRACk] choose a password (leave empty for manual entry): ")
            if password == "":
                print("[cRACk] great! you're entering password \033[1;33mmanually\033[0m from now.")
                break
            print(f"[cRACk] great! your password is \033[1;33m{password}\033[0m now.")
            break
    while True:
        check_for_updates = input("[cRACk] check for updates? (y/n, default:y): ")
        if check_for_updates.lower() == "y" or check_for_updates == "":
            print(f"[cRACk] great! update checking is \033[1;33menabled\033[0m now.")
            check_for_updates = True
            break
        elif check_for_updates.lower() == "n":
            print("[cRACk] great! update checking is \033[1;33mdisabled\033[0m.")
            check_for_updates = True
            break
        print("[cRACk] choose y or n")
    while True:
        default_server = input("[cRACk] choose default server ip:port (leave empty for mr.sugoma's): ")
        if default_server == "":
            print("[cRACk] great! default server is \033[1;33m91.192.22.20:42666\033[0m now.")
            default_server = "91.192.22.20:42666"
            break
        elif valid_host(default_server):
            print(f"[cRACk] great! default server is \033[1;33m{default_server}\033[0m now.")
            break
        print("[cRACk] invalid server!")
    while True:
        motd_enabled = input("[cRACk] enable MOTD? (y/n, default:y): ")
        if motd_enabled.lower() == "y" or motd_enabled == "":
            print("[cRACk] great! MOTD is \033[1;33menabled\033[0m now.")
            motd_enabled = True
            break
        elif motd_enabled.lower() == "n":
            print(f"[cRACk] great! MOTD is \033[1;33mdisabled\033[0m now.")
            break
        print("[cRACk] choose y or n")

    print("\n[cRACk] lets summarize everything. here is your config:\n")
    print(f"nickname: \033[1;33m{"*manual entry*" if nickname=="" else nickname}\033[0m")
    print(f"auth: \033[1;33m{"enabled" if auth else "disabled"}\033[0m")
    print(f"password: \033[1;33m{"-" if not auth else "*manual entry*" if password=="" else password}\033[0m")
    print(f"check for updates: \033[1;33m{"enabled" if check_for_updates else "disabled"}\033[0m")
    print(f"default server: \033[1;33m{default_server}\033[0m")
    print(f"MOTD: \033[1;33m{"enabled" if motd_enabled else "disabled"}\033[0m\n")

    while True:
        config_confirm = input("\n[cRACk] is everything perfect? (y/n): ")
        if config_confirm.lower() == "y":
            print("[cRACk] saving config...")
            # save config logic

            input("[cRACk] everything is set up! now cRACk needs to restart so that everything goes correctly. open cRACk after it closes! (press enter to continue)")
            print("[cRACk] 5...")
            time.sleep(1)
            print("[cRACk] 4...")
            time.sleep(1)
            print("[cRACk] 3...")
            time.sleep(1)
            print("[cRACk] 2...")
            time.sleep(1)
            print("[cRACk] 1...")
            time.sleep(1)
            print("[cRACk] exiting...")
            break
        elif config_confirm.lower() == "n":
            while True:
                reconfig_confirm = input("\n[cRACk] do you want to set up everything again? (y/n): ")
                if reconfig_confirm.lower() == "y":
                    print("[cRACk] restarting oobe...")
                    with open('config.toml', 'w') as f:
                        toml.dump(c, f)
                    input("[cRACk] everything is set up! now cRACk needs to restart so that everything goes correctly. open cRACk after it closes! (press enter to continue)")
                    print("[cRACk] 5...")
                    time.sleep(1)
                    print("[cRACk] 4...")
                    time.sleep(1)
                    print("[cRACk] 3...")
                    time.sleep(1)
                    print("[cRACk] 2...")
                    time.sleep(1)
                    print("[cRACk] 1...")
                    time.sleep(1)
                    print("[cRACk] exiting...")
                    sys._exit(1)
                    break
                elif reconfig_confirm.lower() == "n":
                    break
        print("[cRACk] choose y or n")


def main():
    global IP,PORT,NICKNAME
    print("\n"*100)
    print(f'''
 {ASCIIART}
 ------------------------------------------------------
                \033[1;33mc\033[0mlient for \033[1;33mRAC\033[0m \033[1;33mk\033[0mettles
\x1b[3m{center(random_motd())}\x1b[0m

            version \033[1;33m{VERSION}\033[0m | by \033[1;33mpansangg\033[0m
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
        part = sock.recv(4096)
        if not part:
            break
        full += part

    print("[cRACk] we'll meet again")
    dfull = full.decode("utf-8", errors="ignore")
    print(filter_ansi(useragentize(dfull)))
    threading.Thread(target=listen_client).start()
    threading.Thread(target=chunked_reading).start()

    while True:
        time.sleep(1)

if "--reset" in sys.argv or "-r" in sys.argv:
    c["configured"] = False
    with open('config.toml', 'w') as f:
        toml.dump(c, f)

# if c["configured"]:
    main()
# else:
#     oobe()