import os
import sys
import time
import select
import termios
import tty
from math import fmod, sqrt
from random import randint
from colorama import Fore, Back, Style
from boss import *
rip = busdi()

class cloud():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def upd(self):
        self.__x -= 0.5
        self.__y -= 0
        xc = self.__x
        yc = self.__y
        if xc <=1:
            return 0
        else:
            return 1

    def prntp(self):
        xc=int(self.__x)
        yc=int(self.__y)
        print("\033[{};{}H <*=*>".format(yc,xc))

class map():
    def __init__(self):
        self.fullmap = list()
        for i in range(1010):
            temp = list()
            for j in range(50):
                temp.append(" ")
            self.fullmap.append(temp)

    def draw_boundary(self):         #draws sky and ground of the game 
        
        for i in range(0,790):
            for j in range(3,6,1):
                self.fullmap[i][j] = 'Z'
            for k in range(37,40,1):
                self.fullmap[i][k] = 'Z'

    def draw_beams(self):           #Draws beams in the game randomly
        for i in range(80,800,40):
            rnd = randint(0,2)
            #vertical beam
            if rnd == 0 :
                rv = randint(14,30)
                for j in range(0,7):
                    self.fullmap[i][j+rv] = '['
                    self.fullmap[i+1][j + rv] = ']'
            #horizontal beam
            elif rnd == 1:
                rh = randint(14,30)
                for k in range(0,7):
                    self.fullmap[i+k][rh] = '['
                    self.fullmap[i+k][rh+1] = ']'
            #tilted beams
            elif rnd == 2:
                rt = randint(14,30)
                for l in range(0,7):
                    self.fullmap[i+l][rt-l] = '['
                    self.fullmap[i+l+1][rt-l] = ']'

    def draw_coins(self):                   #draw coins in the game randomly
        for i in range(95,800,40):
            rnd = randint(0,2)
                #vertical coins
            if rnd == 0:
                rv = randint(14,30)
                for j in range(0,7):
                    self.fullmap[i][j+rv] = '$'
                    self.fullmap[i+1][j + rv] = '$'
            #horizontal coins
            if rnd == 1:
                rh = randint(14,30)
                for k in range(0,7):
                    self.fullmap[i+k][rh] = '$'
                    self.fullmap[i+k][rh+1] = '$'
            #tilted coins
            if rnd == 2:
                rt = randint(14,30)
                for l in range(0,7):
                    self.fullmap[i+l][rt-l] = '$'
                    self.fullmap[i+l+1][rt-l] = '$'

    def boss_print(self,xco,yco): 
      #prints the boss ememy in the last phase of the game 
        print(str(xco)+"||"+str(yco))
        for i in range(xco,xco+75):
            for j in range(yco,yco+17):
                if j<=35:       
                    self.fullmap[i][j] = rip.array[j-yco][i-xco]
                    # else:
                        # self.fullmap[i][j] = "F"

    def draw_boost(self):       #Activates the boost 
        for i in range(100,800,100):
            rnd = 1
            #horizontal coins
            if rnd == 1:
                rh = randint(15,29)
                for k in range(0,1):
                    self.fullmap[i+k][rh] = '@'

    def draw_magnet(self):          # draws the magnet which attracts the  mandolorian to itself
        self.fullmap[220][19] = '('
        self.fullmap[221][19] = '+'
        self.fullmap[222][19] = ')'
        self.fullmap[220][20] = '*'
        self.fullmap[221][20] = '*'
        self.fullmap[222][20] = '*'
        self.fullmap[219][19] = '*'
        self.fullmap[223][19] = '*'


    def printmanda(self,x,y,c,shield_active):
        if shield_active == 1:
            man = 'S~O~S'
        else:     #It prints our Mandalorian in the game
            man='<~O~>'
        man1 = ' /~\\ '
        for i in range(5):
            self.fullmap[x+i+c][y]=man[i]
            self.fullmap[x+i+c][y+1] = man1[i]


    def clear(self,x,y,c):          #clears the lag
        for i in range(-1,5):
            self.fullmap[x+i+c][y]=" "
            self.fullmap[x+i+c][y+1] = " "
    def getprintmap(self, counter):     #PRINTS THE WHOLE COLORFUL MAP
        print("\033[4;0H")    

        for j in range(3,40):
            for i in range(0,165):
                if self.fullmap[i+counter][j] == 'Z':
                    print(Fore.CYAN + self.fullmap[i+counter][j],end = '')
                elif self.fullmap[i + counter][j] == '[':
                    print(Fore.GREEN + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == ']':
                    print(Fore.GREEN + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == '*':
                    print(Fore.RED + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == '+':
                    print(Fore.RED + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == ')':
                    print(Fore.RED + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == '(':
                    print(Fore.RED + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == '$':
                    print(Fore.YELLOW + self.fullmap[i + counter][j],end = '')
                elif self.fullmap[i + counter][j] == '@':
                    print(Fore.BLUE + self.fullmap[i + counter][j],end = '')
                else:
            
                    print(self.fullmap[i + counter][j],end = '')
            print("")





