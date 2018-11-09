from src import servidor_tcp
from src import servidor_udp
import os

def main():
    os.system('clear')
    print(">>> Deseja rodar o aplicativo em TCP ou UDP? <<<")
    while True:
        x = input("1 - UDP | 2 - TCP >> ")
        if x == '1':
            servidor_udp.main()
        elif x == '2':
            servidor_tcp.main()
        else:
            continue
