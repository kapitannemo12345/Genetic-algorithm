import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt


class Osobnik:
    def __init__(self, n):
        self.N = n
        self.Chessboard = 1 + np.random.permutation(n)  # tablica z NxN wymiarem permutacji liczby chetmanow N
        # self.AttackCounter = []  #funkcja przystosowania osobnika na przestrzeni eliminacji

    def Eveluate(self, ):
        attackCounter = 0

        for i in range(self.N):  # wszystkie wiersze
            if self.Chessboard[i] != 0:
                row = i
                column = self.Chessboard[i]
                # j = i + 1

                for j in range(i + 1, self.N):  # cala szachwonice
                    if column == self.Chessboard[j]:  # sprawdz po kolumnach
                        attackCounter = attackCounter + 1

                    if self.Chessboard[j] != 0:  # sprawdz po skosie
                        if abs(self.Chessboard[j] - column) == abs(j - row):
                            attackCounter = attackCounter + 1

        # self.AttackCounter.append(attackCounter)  #aktualizacja wartosci przystosowania
        return attackCounter


class Populacja:
    def __init__(self, n, pop, genmax, pc, pm, ffmax, mapSectionSize):
        self.Pop = pop
        self.N = n
        self.GenMax = genmax
        self.Pc = pc
        self.Pm = pm
        self.list = []
        self.ffmax = ffmax
        self.MapSectionSize = mapSectionSize
        self.median = []
        self.Value = []
        for i in range(pop):
            self.list.append(Osobnik(n))

        # self.list2 = []
        # self.list2.append(list)

    def Selection(self):
        #print('S lista przed', self.Value)
        Pn = []  # nowa lista

        AT = []#self.Value
        i = 0
        while i < self.Pop:

            i1 = random.randint(0, self.Pop - 1)
            i2 = random.randint(0, self.Pop - 1)
            if i1 != i2:  # Pytanie 1: co w wypadku gdy sa takie same i lista jest mniejsza???
                i = i + 1
                if self.list[i1].Eveluate() <= self.list[i2].Eveluate():
                    Pn.append(self.list[i1])
                    AT.append(self.Value[i1])
                    #nested = self.Value[i1]
                    #nested.append(self.list[i1].Eveluate())
                else:
                    Pn.append(self.list[i2])
                    AT.append(self.Value[i2])
                    #AT.append(self.Value[i2])


        self.list = Pn  # P<-Pn
        print('nowy rozmiar listy: ', np.size(self.list))
        self.Pop = np.size(self.list)  # atkualizacja zmiennych
        self.Value = AT
        #print('S lista po', self.Value)
    # for i in range (self.Pop):
    # self.list[i].AttackCounter = AT[i]

    def Crossover(self):
        i = 0
        while i < self.Pop - 2:
            if random.random() <= self.Pc:
                self.Cross(i, i + 1)
            i = i + 2  # Pytanie 4 czy t linijka powinna byc pod if???

    def Cross(self, i1, i2):  # Pytanie 2: co jesli 2 tablice maja bicia??? i mapping list ma 2 takie same liczby
        Mp1 = []
        Mp2 = []
        for i in range(self.MapSectionSize):  # zaczniemy od 1 lemetnu talbicy do rozmiaru map section
            Mp1.append([self.list[i1].Chessboard[i], self.list[i2].Chessboard[i]])  # lista list???
            # Mp2.append(self.list[i2].Chessboard[i])
            a = self.list[i1].Chessboard[i]
            self.list[i1].Chessboard[i] = self.list[i2].Chessboard[i]
            self.list[i2].Chessboard[i] = a

        # print('mapping w cross:', Mp1)
        # print('mapsection', self.MapSectionSize)
        # print('ograniczenie', self.N-1)

        h1 = 0
        h2 = 0

        # print('po zamianie ', self.list[i1].Chessboard)
        # print('po zamianie ', self.list[i2].Chessboard)
        for i in range(self.MapSectionSize, self.N):
            h1 = 0
            while h1 == 0:  # zamian musi sie kontynuowaca do momentu gdy zamienina liczba nei bedzie w liscie mapping list
                h1 = 1
                for j in range(self.MapSectionSize):
                    if self.list[i1].Chessboard[i] == Mp1[j][1]:
                        # print('wykryto ', self.list[i1].Chessboard[i], 'i ', Mp1[j][1])
                        # print('zamieniam ', self.list[i1].Chessboard[i], 'na  ', Mp1[j][0])
                        h1 = 0
                        self.list[i1].Chessboard[i] = Mp1[j][0]

        for i in range(self.MapSectionSize, self.N):
            h2 = 0
            while h2 == 0:
                h2 = 1
                for j in range(self.MapSectionSize):
                    if self.list[i2].Chessboard[i] == Mp1[j][0]:
                        # print('wykryto ', self.list[i2].Chessboard[i], 'i ', Mp1[j][0])
                        # print('zamieniam ', self.list[i2].Chessboard[i], 'na  ', Mp1[j][1])
                        h2 = 0
                        self.list[i2].Chessboard[i] = Mp1[j][1]

    def Mutation(self):
        i = 0
        while i < self.Pop:
            if random.random() <= self.Pm:
                self.Mutate(i)  # tutaj mutate
            i = i + 2

    def Mutate(self, i):
        # print('pop to:', self.Pop)
        i1 = random.randint(0, self.N - 1)  # -1 bo indeksowanie od 0
        i2 = random.randint(0, self.N - 1)

        a = self.list[i].Chessboard[i1]
        self.list[i].Chessboard[i1] = self.list[i].Chessboard[i2]
        self.list[i].Chessboard[i2] = a

    def Min(self):
        best = 0

        for i in range(2, self.Pop):
            if self.list[i].Eveluate() < self.list[best].Eveluate():
                best = i

        # print('najlepszy index to :', best)

        return best

    def CalculateMedian(self):
        sum = 0
        #print('test',self.Value[-1])
        for i in range(self.Pop):
            a = self.Value[i][-1]#-1 ostatni oddana wartosc
            sum = sum + a
            # sum = sum + self.list[i].AttackCounter.pop()

        median = sum / self.Pop

        return median

    def EvoAlgorithm(self):

        for i in range(self.Pop):
            self.Value.append([self.list[i].Eveluate()])
        m1 = self.CalculateMedian()
        #m1 = self.median
        self.median.append(m1)
        gen = 0
        best = self.Min()
        print('wagi poczotkowe')
        print(self.Value)
        print('------------')
        while gen < self.GenMax and self.list[best].Eveluate() > self.ffmax:
            self.Selection()
            self.Crossover()
            self.Mutation()

            #print('lista przed', self.Value)

            for i in range(self.Pop):#dodaj jeden elment do lsity wag

                a = self.list[i].Eveluate()#list to lista list
                #b = self.Value[i]
                nested = self.Value[i].copy()
                nested.append(a)
                self.Value[i] = nested
            #print('lsita po ', self.Value)


            best = self.Min()
            m2 = self.CalculateMedian()
            self.median.append(m2)

            gen = gen + 1
        # print('rozwiozanie to ', self.list[best].Chessboard)
        print('gen to ', gen)
        print('best to ', best)

        return self.list[best].Chessboard, self.Value, self.Value[best], self.median


if __name__ == '__main__':


    P3 = Populacja(8, 20, 1000, 0.7, 0.2, 0, 3)
    a, b, c, d = P3.EvoAlgorithm()
    print('rozwiazanie dla szachownicy: ', a)
    print('tabela wag: ', b)
    print('waga dla roziwazania: ', c)
    print('mediana', d)

    plt.figure(1)
    plt.plot(d)
    plt.ylabel('y')
    plt.xlabel('generacje')
    plt.title('średnia wartość funkcji przystosowania')

    plt.figure(2)
    plt.plot(c)
    plt.ylabel('y')
    plt.xlabel('generacje')
    plt.title('wartość funkcji przystosowania dla rozwiazania')
    plt.show()




