import numpy as np
import os

limpa	= "os.system('cls' if os.name == 'nt' else 'clear')"


def jogo(board, jogando):
    aux = [
        str(board.board[0][0]),
        str(board.board[0][1]),
        str(board.board[0][2]),
        str(board.board[1][0]),
        str(board.board[1][1]),
        str(board.board[1][2]),
        str(board.board[2][0]),
        str(board.board[2][1]),
        str(board.board[2][2])
    ]
    for i in range(9):
        if aux[i] == 'X':
            aux[i] = '\033[1;31m'+aux[i]+'\033[0;0m'
        elif aux[i] == 'O':
            aux[i] = '\033[1;33m'+aux[i]+'\033[0;0m'
    print("\n")
    print("\t|=====================================================|")
    print("\t|                    JOGO DA VELHA                    |")
    print("\t|=====================================================|")
    print("\t|                     Sua peça: "+board.minhaPeca+"                     |")
    print("\t|=====================================================|")
    print("\t|                     Jogando > "+str(jogando)+"                     |")	 
    print("\t|=====================================================|")	 
    print("\t|                 +-----+-----+-----+                 |")
    print("\t|                 |  "+aux[0]+"  |  "+aux[1]+"  |  "+aux[2]+"  |                 |")
    print("\t|                 +-----+-----+-----+                 |")
    print("\t|                 |  "+aux[3]+"  |  "+aux[4]+"  |  "+aux[5]+"  |                 |")
    print("\t|                 +-----+-----+-----+                 |")
    print("\t|                 |  "+aux[6]+"  |  "+aux[7]+"  |  "+aux[8]+"  |                 |")
    print("\t|                 +-----+-----+-----+                 |")
    print("\t|-----------------------------------------------------|")


class GameState:
    def __init__(self, minhaPeca=''):
        self.board = [
                ['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9']
        ]
        self.player2 = 0
        self.player1 = 0
        self.E = 0
        self.minhaPeca = minhaPeca

    def reiniciar(self, ganhador):
        self.board = [
                ['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9']
        ]
        # Se indice = 0:
            # Player1: X
            # Player2: O
        # Se indice = 1:
            # Player1: O
            # Player2: X
        self.contabilizar(ganhador)


    def placar(self):
        eval(limpa)
        print("\n")
        print("\t|=====================================================|")
        print("\t|                   JOGO DA VELHA                     |")
        print("\t|=====================================================|")
        print("\t|                       PLACAR                        |")
        print("\t|     ( Player 1 ) => "+str(self.player1)+"        "+str(self.player2)+" <= ( Player 2 )      |")
        print("\t|     EMPATES => "+str(self.E)+"                                    |")
        print("\t|=====================================================|")

    def contabilizar(self, ganhador):
        if ganhador == 0:
            self.E += 1
        elif ganhador == 1:
            self.player1 += 1
        elif ganhador == 2:
            self.player2 += 1

    def verificarJogo(self):
        if self.board[0][0] == 'X' and self.board[1][1] == 'X' and self.board[2][2] == 'X':
            return 1 # Jogador X venceu
        elif self.board[2][0] == 'X' and self.board[1][1] == 'X' and self.board[0][2] == 'X':
            return 1 # Jogador X venceu
        elif self.board[0][0] == 'O' and self.board[1][1] == 'O' and self.board[2][2] == 'O':
            return 2 # Jogador O venceu
        elif self.board[2][0] == 'O' and self.board[1][1] == 'O' and self.board[0][2] == 'O':
            return 2 # Jogador O venceu

        for i in range(3):
            if self.board[i][0] == 'X' and self.board[i][1] == 'X' and self.board[i][2] == 'X':
                return 1 # Jogador X venceu
            elif self.board[0][i] == 'X' and self.board[1][i] == 'X' and self.board[2][i] == 'X':
                return 1 # Jogador X venceu
            elif self.board[i][0] == 'O' and self.board[i][1] == 'O' and self.board[i][2] == 'O':
                return 2 # Jogador O venceu
            elif self.board[0][i] == 'O' and self.board[1][i] == 'O' and self.board[2][i] == 'O':
                return 2 # Jogador O venceu

        for i in range(3):
            for j in range(3):
                if self.board[i][j].isdigit():
                    return -1 # Ainda há espaço para jogadas
        return 0 # Empate

    def save(self):
        return ';'.join([';'.join(x) for x in self.board])

    def restore(self, data):
        self.board = np.reshape(data.split(';'), (3,3)).tolist()

    def print(self, jogando):
        eval(limpa)
        jogo(self, jogando)

    def move(self, opt, piece):
        # Valida os parâmetros de entrada
        if opt < 1 or opt > 9:
            raise RuntimeError('Número inválido: {}'.format(opt))
        dicionario = {
            '1': (0, 0),
            '2': (0, 1),
            '3': (0, 2),
            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '7': (2, 0),
            '8': (2, 1),
            '9': (2, 2)
        }
        (linha, coluna) = dicionario[str(opt)]

        # Verifica se a posição jogada está vazia
        if not str(self.board[linha][coluna]).isdigit():
            raise RuntimeError('Posição do tabuleiro já preenchida: {}x{}'.format(linha, coluna))

        # Faz a jogada
        self.board[linha][coluna] = piece
        if piece == 'X':
            self.print('O')
        else:
            self.print('X')