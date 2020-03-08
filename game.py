import os
from os import system
import sys
import time
import select
import termios
import tty
from math import fmod, sqrt
from random import randint
from objects import *
from file import jet
from boss import *

def is_data():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


t = 0
manda = jet(25, 25)
fight = gun_fight()
seenry = map()
counter = 0
seenry.draw_boundary()
seenry.draw_beams()
seenry.draw_coins()
seenry.draw_magnet()
seenry.draw_boost()
seenry.boss_print(rip.get_x(),rip.get_y())
prx = 0
pry = 0
# score = 0
boost_active = 0
boost_time = 10
rex = 0
t = True
shield_active = 0 
shield_counter = 0
refil = 0
wait = 0
bull=[]
while t:

    global KEY_PRESSED_UP
    global KEY_PRESSED_LEFT
    global KEY_PRESSED_RIGHT
    global KEY_PRESSED_SPACE
    global KEY_PRESSED_FIRE
    KEY_PRESSED_UP = False
    KEY_PRESSED_LEFT = False
    KEY_PRESSED_RIGHT = False
    KEY_PRESSED_SPACE = False
    KEY_PRESSED_FIRE = False

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    STEP = 0.1
    t += 1
    time.sleep(STEP)
    system('clear')

    if is_data():
        ch = sys.stdin.read(1)
        if ch == "w":
            KEY_PRESSED_UP = True
        if ch == "a":
            KEY_PRESSED_LEFT = True
        if ch == "d":
            KEY_PRESSED_RIGHT = True
        if ch == "W":
            KEY_PRESSED_UP = True
        if ch == "A":
            KEY_PRESSED_LEFT = True
        if ch == "D":
            KEY_PRESSED_RIGHT = True
        if ch == " ":
            KEY_PRESSED_SPACE = True
        if ch == "q" or ch == "Q":
            quit()
        if ch == "F" or ch == "f":
            KEY_PRESSED_FIRE = True

        # if this sentence in the game over, graph not right
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if KEY_PRESSED_UP == True:
        manda.moveup()

    if KEY_PRESSED_LEFT == True:
        manda.moveleft()

    if KEY_PRESSED_SPACE == True:
        if shield_counter == 300:
            shield_active = 1

    if KEY_PRESSED_FIRE == True:
        fight.shoot_goli(manda,counter)

    if refil == 1 and KEY_PRESSED_SPACE == True:
        shield_counter -= 4
    
    if shield_counter <= 0:
        shield_counter = 0

    if KEY_PRESSED_RIGHT == True:
        manda.moveright()

    manda.gravity()
    manda.update()

    xc = int(manda.get_x())
    yc = int(manda.get_y())
    # seenry.clear(prx,pry,counter)
    # update due to magnet
    if counter > 60 and counter < 220:
        dx = 220-xc-counter
        dy = 20-yc
        p = sqrt(dx**2+dy**2)
        if p != 0:
            vx = (dx/p)*0.2
            vy = (dy/p)*0.2
            manda.set_vx(manda.get_vx() + vx) 
            manda.set_vy(manda.get_vy() + vy)
            manda.update()
    anna = 0
    if counter >= 830:
        if anna % 4 is 0:
            fight.bshoot_goli(rip,counter)
            fight.bupdate(seenry)
            fight.bprint_goli(seenry,counter)
            print(fight.get_bgoli()[anna])
        anna = anna + 1    

        
    fight.update(seenry)    
    fight.print_goli(seenry,counter)
    
    rip.set_bossh(rip.get_bossh()-fight.hit(seenry)) #used getter and setter functions
    seenry.boss_print(rip.get_x(),rip.get_y())
    print("y-axis:"+str(manda.get_y()))
    rip.interact(seenry.fullmap,manda)
    # COINS
    xvv = 0
    if seenry.fullmap[xc+4+counter][yc] == '$':
        # time.sleep(1)
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+4+counter][yc] = ''


    if seenry.fullmap[xc+3+counter][yc] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+3+counter][yc] = ''
    if seenry.fullmap[xc+2+counter][yc] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+2+counter][yc] = ''
    if seenry.fullmap[xc+1+counter][yc] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+1+counter][yc] = ''
    if seenry.fullmap[xc+0+counter][yc] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+0+counter][yc] = ''
    # 2nd row
    if seenry.fullmap[xc+3+counter][yc+1] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+3+counter][yc+1] = ''
    if seenry.fullmap[xc+2+counter][yc+1] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+2+counter][yc+1] = ''
    if seenry.fullmap[xc+1+counter][yc+1] == '$':
        fight.set_score(fight.get_score() + 10)
        xvv = 1
        seenry.fullmap[xc+1+counter][yc+1] = ''

    # BOOST

    if seenry.fullmap[xc+4+counter][yc] == '@':

        xvv = 1
        boost_active += 1
        seenry.fullmap[xc+4+counter][yc] = ''
    if seenry.fullmap[xc+3+counter][yc] == '@':

        xvv = 1
        boost_active += 1
        seenry.fullmap[xc+3+counter][yc] = ''
    if seenry.fullmap[xc+2+counter][yc] == '@':

        xvv = 1
        boost_active += 1
        seenry.fullmap[xc+2+counter][yc] = ''
    if seenry.fullmap[xc+1+counter][yc] == '@':

        boost_active += 1
        xvv = 1
        seenry.fullmap[xc+1+counter][yc] = ''
    if seenry.fullmap[xc+0+counter][yc] == '@':

        boost_active += 1
        xvv = 1
        seenry.fullmap[xc+0+counter][yc] = ''
    # 2nd row

    if seenry.fullmap[xc+3+counter][yc+1] == '@':
        xvv = 1
        boost_active += 1
        seenry.fullmap[xc+3+counter][yc+1] = ''
    if seenry.fullmap[xc+2+counter][yc+1] == '@':
        xvv = 1
        boost_active += 1
        seenry.fullmap[xc+2+counter][yc+1] = ''
    if seenry.fullmap[xc+1+counter][yc+1] == '@':
        boost_active += 1
        xvv = 1
        seenry.fullmap[xc+1+counter][yc] = ''

   ############################################# < SHIELD > ###########
    if shield_active == 1:

        if seenry.fullmap[xc+4+counter][yc] == ']':
            manda.set_life(manda.get_life()+0)
            seenry.fullmap[xc+4+counter][yc] = ']'
        if seenry.fullmap[xc+3+counter][yc] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc] = ']'
        if seenry.fullmap[xc+2+counter][yc] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc] = ']'
        if seenry.fullmap[xc+1+counter][yc] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc] = ']'
        if seenry.fullmap[xc+0+counter][yc] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+0+counter][yc] = ']'

        if seenry.fullmap[xc+4+counter][yc] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+4+counter][yc] = '['
        if seenry.fullmap[xc+3+counter][yc] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc] = '['
        if seenry.fullmap[xc+2+counter][yc] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc] = '['
        if seenry.fullmap[xc+1+counter][yc] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc] = '['
        if seenry.fullmap[xc+0+counter][yc] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+0+counter][yc] = '['

            # 2nd row
        if seenry.fullmap[xc+3+counter][yc+1] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc+1] = '['
        if seenry.fullmap[xc+2+counter][yc+1] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc+1] = '['
        if seenry.fullmap[xc+1+counter][yc+1] == '[':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc+1] = '['
        if seenry.fullmap[xc+3+counter][yc+1] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc+1] = ']'
        if seenry.fullmap[xc+2+counter][yc+1] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc+1] = ']'
        if seenry.fullmap[xc+1+counter][yc+1] == ']':
            manda.set_life(manda.get_life()+0)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc+1] = ']'
    else:

        if seenry.fullmap[xc+4+counter][yc] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+4+counter][yc] = ']'
        if seenry.fullmap[xc+3+counter][yc] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc] = ']'
        if seenry.fullmap[xc+2+counter][yc] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc] = ']'
        if seenry.fullmap[xc+1+counter][yc] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc] = ']'
        if seenry.fullmap[xc+0+counter][yc] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+0+counter][yc] = ']'

        if seenry.fullmap[xc+4+counter][yc] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+4+counter][yc] = '['
        if seenry.fullmap[xc+3+counter][yc] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc] = '['
        if seenry.fullmap[xc+2+counter][yc] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc] = '['
        if seenry.fullmap[xc+1+counter][yc] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc] = '['
        if seenry.fullmap[xc+0+counter][yc] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+0+counter][yc] = '['
    # 2nd row
        if seenry.fullmap[xc+3+counter][yc+1] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc+1] = '['
        if seenry.fullmap[xc+2+counter][yc+1] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc+1] = '['
        if seenry.fullmap[xc+1+counter][yc+1] == '[':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc+1] = '['
        if seenry.fullmap[xc+3+counter][yc+1] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+3+counter][yc+1] = ']'
        if seenry.fullmap[xc+2+counter][yc+1] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+2+counter][yc+1] = ']'
        if seenry.fullmap[xc+1+counter][yc+1] == ']':
            manda.set_life(manda.get_life()-1)
            xvv = 1
            seenry.fullmap[xc+1+counter][yc+1] = ']'


        ###############################################################boss buleet hit 
        if seenry.fullmap[xc+4+counter][yc] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
        if seenry.fullmap[xc+3+counter][yc] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
        if seenry.fullmap[xc+2+counter][yc] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
        if seenry.fullmap[xc+1+counter][yc] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
        if seenry.fullmap[xc+0+counter][yc] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
    # 2nd row
        if seenry.fullmap[xc+3+counter][yc+1] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
        if seenry.fullmap[xc+2+counter][yc+1] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1
        if seenry.fullmap[xc+1+counter][yc+1] == '<~':
            manda.set_life(manda.get_life()-1)
            xvv = 1

    if manda.get_life() <= 0:
        print('GAME - OVER')
        print('Your Score: ' + str(fight.get_score()))
        quit()

    seenry.printmanda(xc, yc, counter,shield_active)
    
    prx = xc
    pry = yc

    # for i in obj:
    #     if i.upd():
    #         i.prntp()
    #     else:
    #         obj.remove(i)

    print("\033[2;9H" + " _ |^||^__||_ ^ _|  | _ \\  (_)_\\(_)((/ __|| |/ /   _ |^| /^_^\\\\^\\ /^/| _ \\|_^_| |   \\ |^__| ")
    print("\033[3;9H" + "| || || _|   | |    |  _/   / _ \\   | (__   ' <   | || || (_) |\\ V / |   / | |  | |) || _|  ")
    print("\033[4;9H" + " \\__/ |___|  |_|    |_|    /_/ \\_\\   \\___| _|\\_\\   \\__/  \\___/  |_|  |_|_\\|___| |___/ |___|")

    seenry.getprintmap(counter)
    seenry.clear(prx, pry, counter)

    print('Score: ' + str(fight.get_score()) + ', ', end='')
    print('lives: ' + str(manda.get_life()) + ', ', end='')
    if boost_active == 1 and rex < 20:
        counter += 3
        rex += 1
        print('BOOST: ' + 'YES' + ', ', end='')
    else:
        boost_active = 0
        rex = 0
        print('BOOST: ' + 'NO' + ', ', end='')

    if shield_active == 1:
        print('SHIELD_ACTIVE: ' + 'YES' + ', ', end='')
    else:
        print('SHIELD_ACTIVE: ' + 'NO' + ', ', end='')

    if shield_counter == 0:
        shield_active = 0

    if shield_active == 1: 
        shield_counter -= 4

    if shield_active == 0 and shield_counter <= 299:
        shield_counter += 5
    if rip.get_bossh() <=0:
        print('********************************YOU-WIN*************************************',end='')
        print('Your Score: ' + str(fight.get_score()))
        quit()
    print('SHIELD_REFIL: ' + str(shield_counter) + '/' + '300' + ',  ', end='')
    print('BOSS_HEALTH :' + str(rip.get_bossh())  + ', ',end='')
    print('Timer: ', counter)
    
    if counter <= 830:
        counter += 1
