# cRACk v1.075
«_<ins>**c**</ins>lient for <ins>**RAC**</ins> <ins>**k**</ins>ettles_» **→** <ins>**cRACk**</ins>

cRACk is TUI client for [RAC](https://github.com/The-Stratosphere-Solutions/RAC-Hub), written on Python.


## features
- supports [RAC v1.99.2](https://github.com/The-Stratosphere-Solutions/RAC-Hub/blob/main/RACv1.99.md)
- supports [user-agents](https://github.com/MeexReay/bRAC/blob/main/docs/user_agents.md) (except clRAC's)

## quick start
### for Windows
use executable from [latest release](https://github.com/pansangg/cRACk/releases),\
or run `main.py` with python interpreter.

### for Linux
use binary from [latest release](https://github.com/pansangg/cRACk/releases),\
or run `main.py` with python interpreter.

### for other OSes
run `main.py` with python interpreter,\
or [build it from source](#building-from-source) for yourself
> note: there is no guarantee that your build will work

## building from source
1) install python

https://www.python.org/downloads

2) download this repo or clone it using git
```
git clone https://github.com/pansangg/cRACk.git
```
3) install pyinstaller
```
pip install pyinstaller
```
4) in the same directory where the main.py is located run
```
python -m PyInstaller --onefile main.py
```
5) done. check /dist folder

## screenshots
Choosing nickname and host
![ASCII art, choosing a nickname and host](img/hello.png)
Chatting with others
![Chatting with other people, user-agents](img/chat.png)

## TODO
- [x] fix ctrl+c exit
- [x] add user-agents support
- [ ] add first-time config
- [ ] add saving config
- [ ] add MOTDs
- [ ] add support for [RAC v2](https://github.com/The-Stratosphere-Solutions/RAC-Hub/blob/main/RACv2.md) (auth)
- [ ] add support for [WRAC v2](https://github.com/The-Stratosphere-Solutions/RAC-Hub/blob/main/WRAC.md)
- [ ] fix "lower than before 0x00 result" bug
- [ ] add ANSI filter
- [x] add some colors you know
- [x] add random nickname option
- [ ] how to leave the server??
- [x] add screenshots
- [ ] hide your ip

## license
this project is licensed under GPL-3.0 license.

## see also
- [RAC-Hub](https://github.com/The-Stratosphere-Solutions/RAC-Hub)
- [about RAC (v1.99)](https://github.com/The-Stratosphere-Solutions/RAC-Hub/blob/main/RACv1.99.md)
- [about RAC (v2)](https://github.com/The-Stratosphere-Solutions/RAC-Hub/blob/main/RACv2.md)
- [about WRAC (v2)](https://github.com/The-Stratosphere-Solutions/RAC-Hub/blob/main/WRAC.md)
- [bRAC - better RAC client](https://github.com/MeexReay/bRAC)
- [Mefedroniy - TUI RAC client](https://github.com/OctoBanon-Main/mefedroniy-client)