import os
import sys
import time
import select
import termios
import tty
from math import fmod, sqrt
from random import randint
class busdi():
    def __init__(self):
        ng = [" " for i in range(300)]
        ng[9] ="""                   /^/   /^/        ^_^_^_^_^ """
        ng[10]="""                  /^/~~-/^/  `.`_^-~/- ````/ )\\ """
        ng[11]="""  		       {\\   _/} ~~~/_\\`_>- )<__\\ )``` ))\\"""
        ng[12]="""                  /'   (_/  _-~  | |__>--<`_|_` """
        ng[13]="""                 |0  0 _/) )-~     | |__>--<-` """
        ng[14]="""                 / /~ ,_/       / /__>---<__/ """  
        ng[15]="""                o o _//        /-~_>---<__-~"""
        ng[16]="""                (^(~          /~_>---<__- ~  """          
        ng[17]="""               ,/|           /__>--<__/_~ """       
        ng[18]="""            ,//('(          |__>--<__| /                 .----_ """
        ng[19]="""           ( ( '))          |__>--<__| |                 /' _---_~\\"""
        ng[20]="""        `-)) )) (           |__>--<__| |                /'  /     ~\\`\\"""
        ng[21]="""       ,/,'//( (             \\__>--<__^\\    \\           /'  //        ||"""
        ng[22]="""     ,( ( ((, ))              ~-__>--<_~`-_~--____---~' _/'/        /'"""
        ng[23]="""   `~/  )` ) ,/|                 ~-_~>--<_/-__       __-~ _/ """
        ng[24]="""  ._-~//( )/ )) `                    ~~-'_/_/ /~~~~~~~__--~ """
        ng[25]="""                                          ~~~~~~~~~~ """

        '''
        x = 100
        y = 10
        '''
        self.__bossh = 400
        self.__x = 925
        self.__y = 10
        self.__vx=0
        self.__vy=0
		
        #print(len(ng[21]))
        self.array = [["" for i in range(100)] for j in range(100)]        
        for i in range(17):
            for j in range(75):
                if j < len(ng[9+i]):
                    self.array[i][j] = ng[i+9][j]
                else:
                    self.array[i][j] = " "
	
    # def __init__(self):
        self.fullmap = list()
        for i in range(1010):
            bgoli = list()
            for j in range(50):
                bgoli.append(" ")
            self.fullmap.append(bgoli)
    def get_x(self):
        return self.__x
    def set_x(self,value):
        self.__x = value
    def get_y(self):
        return self.__y
    def set_y(self,value):
        self.__y = value
    def moveup(self):
        self.__vy -= 0.3
    def moveleft(self):
        self.__vx -= 0.2
    def moveright(self):  
        self.__vx += 0.2	
    def gravity(self):     #gravity effect
        self.__vy+=0.1 
    def update(self):
        self.__x+=self.__vx
        self.__y+=self.__vy
        xc = self.__x
        yc = self.__y
        if xc <=1:
            self.__x=2
            self.__vy=0
            self.__vx=0
        if xc >150:
            self.__x=150
            self.__vy=0
            self.__vx=0
        if yc <= 7:
            self.__y=7
            self.__vy=0
            self.__vx=0
        if yc > 35:
            self.__y=35
            self.__vx=0
            self.__vy=0

    def get_bossh(self):				# Getter boss health
        return self.__bossh

    def set_bossh(self,value):			# Setter boss health
        self.__bossh = value

    def interact(self,map,mandu):           #Boss up-down movment
        if mandu.get_y() > self.get_y(): 
            for i in range(self.get_x(),self.get_x()+75):
                map[i][self.get_y()] = " "
            if self.get_y() <= 20:
                self.set_y(self.get_y()+1)
        elif mandu.get_y() < self.get_y():
            for i in range(self.get_x(),self.get_x()+75):
                map[i][self.get_y()+16] = " "
            self.set_y(self.get_y()-1)

class gun_fight():
    def __init__(self):
        self.__golis = list()
        self.__score = 0
        self.__bgolis = list()
    def get_bgoli(self):
        return self.__bgolis
    
    def get_goli(self):
        return self.__golis
    
    def set_goli(self,value):
        self.__golis = value
    
    def set_bgoli(self,value):
        self.__bgolis = value

    def shoot_goli(self,manda,counter):
        self.__golis.append([int(manda.get_x())+counter,int(manda.get_y()),1])
    
    def bshoot_goli(self,boss,counter):
        self.__bgolis.append([int(boss.get_x()-10),int(boss.get_y()),1])
    
    def bupdate(self,map):
        ana = 0
        for i in self.__bgolis:
            ana = ana + 1
            if i[2] == 1:
                if i[0] > 8:
                    i[0]-=8
                else:
                    self.__bgolis.pop(ana)
                if i[0]>=950:
                    i[2] = 0
    
    def update(self,map):
        for i in self.__golis:
            if i[2] == 1:
                i[0]+=3
                if i[0]>= 990:
                    i[2] = 0

    def get_score(self):
        return self.__score
    def set_score(self,value):
        self.__score = value
    def print_goli(self,map,counter):
        for i in self.__golis:
            if i[2] == 1:	
                map.fullmap[i[0]-3][i[1]]=" "
                map.fullmap[i[0]-2][i[1]]=" "
                map.fullmap[i[0]][i[1]]="~>"
            else:
                map.fullmap[i[0]-3][i[1]]=" "
                map.fullmap[i[0]-2][i[1]]=" "
                map.fullmap[i[0]][i[1]]=" "
		
    def bprint_goli(self,map,counter):
        # print( 'heloo:'+str(len(self.__bgolis))+"|||")
        # map.fullmap[840][5] = "?"
        for i in self.__bgolis:
            if i[2] == 1:
                map.fullmap[i[0]+8][i[1]] = " "
                map.fullmap[i[0]+7][i[1]] = " "
                map.fullmap[i[0]+6][i[1]] = " "
                map.fullmap[i[0]+5][i[1]] = " "
                map.fullmap[i[0]+4][i[1]] = " "
                map.fullmap[i[0]+3][i[1]] = " "
                map.fullmap[i[0]+2][i[1]] = " "
                map.fullmap[i[0]+1][i[1]]=" "
                map.fullmap[i[0]][i[1]]="<~"
            # else:
            #     if len(map.fullmap[i[0]-3])>i[1]:
            #         map.fullmap[i[0]-3][i[1]]=" "
            #     if len(map.fullmap[i[0]-2])>i[1]:
            #         map.fullmap[i[0]-2][i[1]]=" "
            #     if len(map.fullmap[i[0]])>i[1]:
            #         map.fullmap[i[0]][i[1]]=" "

    def hit(self,map):
        x=0
        for i in self.__golis:
            if i[0]>925 and i[1]<30 and i[1]>9:
                self.__golis.remove(i)
                map.fullmap[i[0]][i[1]]=" "
                map.fullmap[i[0]+1][i[1]]=" "
                x+=10
                self.__score += 10
        return x		