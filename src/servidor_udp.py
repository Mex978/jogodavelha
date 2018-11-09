from src import gamestate
import random
import socket
import time
import sys
import os


def escolherJogadorInicial(listaConectados, udp):
    udp.sendto('X'.encode('utf-8'), listaConectados[0])
    udp.sendto('O'.encode('utf-8'), listaConectados[1])

def main():
    board = gamestate.GameState()
    HOST = "localhost"
    PORT = 2011
    os.system("clear")
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, PORT))

    listaConectados = []
    while (len(listaConectados) < 2):
            os.system("clear")
            print(f'Servidor rodando na porta {PORT}!\nAguardando conexões...')
            print ("\n\n==> Clientes conectados: " + str(len(listaConectados)))
            _,addr = udp.recvfrom(1024)
            print(addr)
            listaConectados.append(addr)

    while True: # Para reiniciar o jogo
        board.placar()
        escolherJogadorInicial(listaConectados, udp)
        resp = 1
        indice = 0
        indice_oposto = 1
        jogoAtual = 1
        while jogoAtual == 1: # Manter o servidor aberto sempre recebendo conexões
            while True:
                try:
                    data,_ = udp.recvfrom(1024)
                    board.placar()
                    board.restore(data.decode('utf-8'))
                    estadoJogo = board.verificarJogo()
                    if estadoJogo != -1:
                        board.reiniciar(estadoJogo)
                        jogoAtual = 0
                        if indice == 0:
                            udp.sendto(data, listaConectados[indice_oposto])
                            indice = 1
                            indice_oposto = 0
                        elif indice == 1:
                            udp.sendto(data, listaConectados[indice_oposto])
                            indice = 0
                            indice_oposto = 1
                        break
                    elif indice == 0:
                        udp.sendto(data, listaConectados[indice_oposto])
                        indice = 1
                        indice_oposto = 0
                        break
                    elif indice == 1:
                        udp.sendto(data, listaConectados[indice_oposto])
                        indice = 0
                        indice_oposto = 1
                        break
                except:
                    resp = input("Continuar? (y/n)")
                    if resp == 'Y' or resp == 'y':
                        pass
                    else:
                        sys.exit(1)

