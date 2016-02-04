#!/usr/local/bin/python2.7
"""control flow, instance handling"""
import curses
import time
import random
from arena import *
from entities import *

def doomselector():
    """Selects a random number identify next enemy"""
    doomroll = random.randint(0,100)
    if doomroll > 0 and doomroll < 40:
        return 1
    if doomroll > 40 and doomroll < 70:
        return 2
    if doomroll > 70:
        return 3

def main(win):
    """Main control flow"""
    global stdscr
    stdscr = win
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)
    y,x=0,1
    maxcoords = stdscr.getmaxyx() #(38,90)
    stdscr.refresh()
    #instantiate the window layout
    Ewin = Enemy_win(maxcoords[y],maxcoords[x])
    Pwin = Player_win(maxcoords[y],maxcoords[x]) 
    Swin = Status_win(maxcoords[y],maxcoords[x])
#    Pwin.update_p_status()
#    Ewin.update_e_status()
    player1=Player()
    new_enemy = Peon()
    enemies = {'Peon':Peon,'Ogre':Ogre,'Troll':Troll,'Dragon':Dragon}
#Write values of each entity to screen
    en_attrlist = ['HP','Armor','Atk','Evade']
    pl_attrlist = ['HP','Armor','Atk','Evade','AP','Potions']
    pl_attrs = [x for x in player1.__dict__.iteritems()if x[0] in pl_attrlist] #get current hp,etc readings from player class
    for index,val in enumerate(pl_attrs,1):
        Pwin.update_p_status(index,val)
    en_attrs = [x for x in new_enemy.__dict__.iteritems()if x[0] in en_attrlist] #get current hp,etc readings from enemy class
    for index,val in enumerate(en_attrs,1):
        Ewin.update_e_status(index,val)
    
    gamecount = 1
    game_is_running = True
    #game flow
    while game_is_running and player1.isalive:
        took_action = False
        keypress = stdscr.getch()
        #player turn
        if keypress == ord('Q'):
            game_is_running = False
            break
        elif keypress == curses.KEY_RIGHT:
            Swin.actselect(1, False)
        elif keypress == curses.KEY_LEFT:
            Swin.actselect(-1, False)
        elif keypress == curses.KEY_ENTER:
            took_action = True
            player1.defending = False
            #Swin.actselect(0, True)
            if Swin.actions[Swin.newpos] == 'Attack':
                pot_dmg = random.randint(5,20)
                #TODO-create a better dmg generator
                Pwin.a_feedback(new_enemy.is_attacked
                        (pot_dmg,False))
                #if new_enemy.dmgcount > 0:
                 #   Ewin.update_e_status(0,new_enemy.dmgcount)
            elif Swin.actions[Swin.newpos] == 'Defend':
               player1.defending = True
               Pwin.d_feedback()
            elif Swin.actions[Swin.newpos] == 'Special':
                pot_dmg = random.randint(15,40)
                Pwin.s_feedback(new_enemy.is_attacked
                        (pot_dmg,True))
            elif Swin.actions[Swin.newpos] == 'Heal':
                if player1.Potions > 0:
                    healed = random.randint(30,50)
                else:
                    healed = 0
                    took_action = False
                Pwin.h_feedback(player1.heal(healed))
                
                #pass
        if took_action:
            en_attrs = [x for x in new_enemy.__dict__.iteritems()
                    if x[0] in en_attrlist] 
                            #get current hp,etc 
                            #readings from enemy class
            for index,val in enumerate(en_attrs,1):
                Ewin.update_e_status(index,val)

            time.sleep(.4)
            enemyattack = random.randint(0,15)
            Ewin.ea_feedback(player1.is_attacked(enemyattack,False))
            pl_attrs = [x for x in player1.__dict__.iteritems()
                    if x[0] in pl_attrlist] 
                            #get current hp,etc 
                            #readings from player class
            for index,val in enumerate(pl_attrs,1):
                Pwin.update_p_status(index,val)


            time.sleep(.1)







    #end of program clean up
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__=='__main__':
    curses.wrapper(main)
