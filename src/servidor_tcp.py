from src import gamestate
import random
import socket
import time
import sys
import os


def escolherJogadorInicial(listaConectados):
    listaConectados[0].sendall('X'.encode('utf-8'))
    listaConectados[1].sendall('O'.encode('utf-8'))

def main():
    os.system("clear")
    board = gamestate.GameState()
    HOST = "localhost"
    PORT = None
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            PORT = random.randint(2000, 2010)
            tcp.bind((HOST, PORT))
            break
        except:
            pass
    tcp.listen(2)
    listaConectados = []
    print(f'Servidor rodando na porta {PORT}!\nAguardando conexões...')
    print ("\n\n==> Clientes conectados: " + str(len(listaConectados)))
    while (len(listaConectados) < 2):
            conn,_ = tcp.accept()
            listaConectados.append(conn)
            os.system("clear")
            print(f'Servidor rodando na porta {PORT}!\nAguardando conexões...')
            print ("\n\n==> Clientes conectados: " + str(len(listaConectados)))

    while True: # Para reiniciar o jogo
        board.placar()
        escolherJogadorInicial(listaConectados)
        resp = 1
        indice = 0
        indice_oposto = 1
        jogoAtual = 1
        while jogoAtual == 1: # Manter o servidor aberto sempre recebendo conexões
            conn = listaConectados[indice]
            while True:
                try:
                    data = conn.recv(1024)
                    board.placar()
                    board.restore(data.decode('utf-8'))
                    estadoJogo = board.verificarJogo()
                    if estadoJogo != -1: # Se aconteceu alguma vitória ou empate
                        board.reiniciar(estadoJogo)
                        jogoAtual = 0
                        if indice == 0:
                            listaConectados[indice_oposto].sendall(data)
                            indice = 1
                            indice_oposto = 0
                        elif indice == 1:
                            listaConectados[indice_oposto].sendall(data)
                            indice = 0
                            indice_oposto = 1
                        break
                    elif indice == 0:
                        listaConectados[indice_oposto].sendall(data)
                        indice = 1
                        indice_oposto = 0
                        break
                    elif indice == 1:
                        listaConectados[indice_oposto].sendall(data)
                        indice = 0
                        indice_oposto = 1
                        break
                except:
                    sys.exit(1)

    for conn in listaConectados:
        conn.close()

