from src import gamestate
import socket
import random
import sys
import os

def verificarJogo(board, opt, dest, socket=None):
    resultadoJogada = board.verificarJogo()
    if opt == 1:
        if resultadoJogada == 0:
            input("\t                 ###### EMPATE! ######\nDigite enter...")
            return True
        elif resultadoJogada == 1 and board.minhaPeca == 'X':
            input("\t                 #### VOCÊ VENCEU ####\nDigite enter...")
            return True
        elif resultadoJogada == 1 and board.minhaPeca == 'O':
            input("\t                 #### VOCÊ PERDEU ####\nDigite enter...")
            return True
        elif resultadoJogada == 2 and board.minhaPeca == 'O':
            input("\t                 #### VOCÊ VENCEU ####\nDigite enter...")
            return True
        elif resultadoJogada == 2 and board.minhaPeca == 'X':
            input("\t                 #### VOCÊ PERDEU ####\nDigite enter...")
            return True
        elif resultadoJogada == -1:
            return False
    elif opt == 2:
        if resultadoJogada == 0:
            socket.sendto(board.save().encode('utf-8'), dest)
            input("\t                 ###### EMPATE! ######\nDigite enter...")
            return True
        elif resultadoJogada == 1 and board.minhaPeca == 'X':
            socket.sendto(board.save().encode('utf-8'), dest)
            input("\t                 #### VOCÊ VENCEU ####\nDigite enter...")
            return True
        elif resultadoJogada == 1 and board.minhaPeca == 'O':
            socket.sendto(board.save().encode('utf-8'), dest)
            input("\t                 #### VOCÊ PERDEU ####\nDigite enter...")
            return True
        elif resultadoJogada == 2 and board.minhaPeca == 'O':
            socket.sendto(board.save().encode('utf-8'), dest)
            input("\t                 #### VOCÊ VENCEU ####\nDigite enter...")
            return True
        elif resultadoJogada == 2 and board.minhaPeca == 'X':
            socket.sendto(board.save().encode('utf-8'), dest)
            input("\t                 #### VOCÊ PERDEU ####\nDigite enter...")
            return True
        elif resultadoJogada == -1:
            return False

def main():
    # Variáveis principais
    HOST = "localhost"
    PORT = 2011
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    os.system("clear")
    dest = (HOST, PORT)
    udp.sendto(''.encode('utf-8'), dest)
    
    print('Conectando ao servidor {} na porta {}'.format(HOST, PORT))
    contador = 0
    aux = 0
    temp = ''
    aux2 = ''
    while True:
        variavelDeJogada,_ = udp.recvfrom(1024)
        variavelDeJogada = variavelDeJogada.decode('utf-8')
        board = gamestate.GameState(variavelDeJogada)
        variavelOpostaDeJogada = ''
        if variavelDeJogada != 'O':
            if variavelDeJogada.find('O') != -1:
                temp = 'O'
                variavelDeJogada = variavelDeJogada.replace('O', '')
                aux2 = variavelDeJogada
                variavelDeJogada = temp
                aux = 1
        if variavelDeJogada == 'X':
            variavelOpostaDeJogada = 'O'
        elif variavelDeJogada == 'O':
            variavelOpostaDeJogada = 'X'
        board.print('X')
        if variavelDeJogada == 'X':
            while 1:
                try:
                    opt = int(input('Digite o numero onde deseja marcar>> '))
                    board.move(opt, variavelDeJogada)
                    break
                except:
                    eval("os.system('cls' if os.name == 'nt' else 'clear')")
                    board.print('X')
                    print('Opção inválida. Tente novamente.')
                    continue
            
            board.print(variavelOpostaDeJogada)

            # Envia o tabuleiro para o servidor
            if contador > 0:
                udp.sendto((board.save() + 'O').encode('utf-8'), dest)
            else:
                udp.sendto(board.save().encode('utf-8'), dest)
        while True:
            # Recebe a jogada do servidor
            if contador > 0 and aux == 1:
                data = aux2
                aux = 0
                board.restore(data)
            else:
                data,_ = udp.recvfrom(1024)
                data = data.decode('utf-8')
                if data.find('9O') != -1:
                    data = data.replace('9O', '9')
                board.restore(data)
            
            board.print(variavelDeJogada)
            if verificarJogo(board, 1, dest): break
            nok = True
            while nok:
                nok = False
                try:
                    opt = int(input('Digite o numero onde deseja marcar>> '))
                    board.move(opt, variavelDeJogada)
                except:
                    nok = True
                    eval("os.system('cls' if os.name == 'nt' else 'clear')")
                    board.print(variavelDeJogada)
                    print('Opção inválida. Tente novamente.')

            board.print(variavelOpostaDeJogada)
            
            # Envia o tabuleiro para o servidor
            if verificarJogo(board, 2, dest, udp): break
            udp.sendto(board.save().encode('utf-8'), dest)
        contador += 1