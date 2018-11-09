from src import cliente_main
from src import servidor_main

if __name__ == '__main__':
    resp = ''
    while resp != 'c' and resp != 'C' and resp != 's' and resp != 'S':
        resp = input("Deseja rodar o cliente ou o servidor? (s - Servidor | c - Cliente)>> ")
    if resp == 'c' or resp == 'C':
        cliente_main.main()
    elif resp == 's' or resp == 'S':
        servidor_main.main()
        
            