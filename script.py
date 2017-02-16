from Tkinter import *
import random
from constants import *


class Game(object):
    def __init__(self, i=Tk()):
        self.i = i

        self.img = Label(text='')
        self.img.grid(row=0, column=0, rowspan=4)

        self.palavraSecreta = random.choice(PALAVRAS)
        Label(text='Palavra ').grid(row=0, column=1)
        self.palavra_inc = Label(text='___ '*len(self.palavraSecreta))
        self.palavra_inc.grid(row=0, column=2)

        Label(text='Letras Erradas ').grid(row=1, column=1)
        self.l_letrasErradas = Label(text='')
        self.l_letrasErradas.grid(row=1, column=2)

        Label(text='Advinha uma letra:').grid(row=2, column=1)
        self.palpite = Entry(self.i, width=2)
        self.palpite.grid(row=2, column=2)
        self.i.bind('<Return>', self.entrada)
        self.palpite.focus_force()

        self.b = Button(text='Novo Jogo', command=self.novo_jogo)
        self.msg = Label(text='')
        self.msg.grid(row=3, column=1, columnspan=2)

        self.letrasErradas = []
        self.letrasAcertadas = []
        self.palpitesFeitos = []

        self.imprime_jogo()

        self.i.mainloop()

    def imprime_jogo(self):
        """
        Feito a partir da variavel global que contem as imagens
        do jogo em ASCII art, e tambem as letras chutadas de
        maneira correta e as letras erradas e a palavra secreta
        """

        self.img['text'] = FORCA_IMG[len(self.letrasErradas)]

        l = ''
        for s in self.palavraSecreta:
            if s in self.letrasAcertadas:
                l += s + ' '
            else:
                l += '_ '
        self.palavra_inc['text'] = l

        l = ''
        for e in self.letrasErradas:
            if e == self.letrasErradas[len(self.letrasErradas) - 1]:
                l += e
            else:
                l = l + e + ', '
        self.l_letrasErradas['text'] = l

        if len(self.letrasErradas) < len(FORCA_IMG) - 1 and\
                not self.verifica_se_ganhou():
            return True
        elif self.verifica_se_ganhou():
            self.msg['text'] = 'GANHASTE!'
        else:
            self.msg['text'] = 'Excedeste o teu limite de palpites!'
        self.palpite.grid_forget()
        self.msg['text'] += \
            '\ndepois de %i letras erradas e %i palpites corretos,\n \
            a palavra era %s.' \
                  % (len(self.letrasErradas), len(self.letrasAcertadas), self.palavraSecreta)
        self.b.grid(row=2, column=2)

    def entrada(self, event):
        self.recebe_palpite()

    def recebe_palpite(self):
        """
        Funcao feita para garantir que o usuario coloque uma
        entrada valida, ou seja, que seja uma unica letra
        que ele ainda nao tenha chutado
        """
        palpite = self.palpite.get()
        self.palpite.delete(0, last=len(palpite))

        if not palpite.isalpha() or len(palpite) != 1 \
                or palpite in self.palpitesFeitos:
            self.msg['text'] = \
                'tens de escrever apenas uma unica letra, que nao tenhas dito'
        else:
            palpite.lower()
            self.palpitesFeitos.append(palpite)

            if palpite in self.palavraSecreta:
                self.letrasAcertadas.append(palpite)
            else:
                self.letrasErradas.append(palpite)
            self.imprime_jogo()

    def novo_jogo(self):
        """
        Funcao que pede para o usuario decidir se ele quer
        jogar novamente e retorna um booleano representando
        a resposta
        """
        self.l_letrasErradas['text'] = ''
        self.b.grid_forget()
        self.msg['text'] = ''
        Game()

    def verifica_se_ganhou(self):
        """
        Funcao que verifica se o usuario acertou todas as
        letras da palavra secreta
        """
        for s in self.palavraSecreta:
            if s not in self.letrasAcertadas:
                return False
        return True


if __name__ == '__main__':
    Game()
