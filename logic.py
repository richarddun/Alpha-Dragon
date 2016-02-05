#!/usr/local/bin/python2.7
"""control flow, instance handling"""
import curses
import time
import random
import os
from arena import *
from entities import *

def draw_pstats():
    pl_attrlist = ['HP','Armor','Atk','Evade','AP','Potions']
    pl_attrs = [x for x in player1.__dict__.iteritems()
                if x[0] in pl_attrlist] 
                #get current hp,etc 
                #readings from player class
    for index,val in enumerate(pl_attrs,1):
        Pwin.update_p_status(index,val)

def draw_estats():
    en_attrlist = ['Type','Description','HP','Armor','Atk','Evade']
    en_attrs = [x for x in new_enemy.__dict__.iteritems()
                if x[0] in en_attrlist] 
                #get current hp,etc 
                #readings from enemy class
    for index,val in enumerate(en_attrs,1):
        Ewin.update_e_status(index,val)

def doomselector():
    """Selects a random number identify next enemy"""
    doomroll = random.randint(0,100)
    if doomroll > 0 and doomroll < 40:
        return 1
    if doomroll > 40 and doomroll < 70:
        return 2
    if doomroll > 70:
        return 3

def get_ch_pic(index):
    enlist = [' ']
    path = os.getcwd()
    with open(os.path.join(path,'resources'),'rb') as picfile:
        for pointer,line in enumerate(picfile,1):
            if pointer >= index:
                for char in line:
                    if char == '&':
                        return enlist
                    enlist.append(char)

def main(win):
    """Main control flow"""
    #put vars in globals to access in functions
    global stdscr,player1,new_enemy,Ewin,Pwin,Swin
    stdscr = win
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)
    y,x=0,1
    if (stdscr.getmaxyx()[0] < 52) or (stdscr.getmaxyx()[1] < 100):
        curses.endwin()
        print "Minimum terminal size to play is 52,100 (cols,lines)"
        return
    maxcoords = (52,100) #stdscr.getmaxyx() #(38,90)
    stdscr.refresh()
    #instantiate the window layout
    Ewin = Enemy_win(maxcoords[y],maxcoords[x])
    Pwin = Player_win(maxcoords[y],maxcoords[x]) 
    Swin = Status_win(maxcoords[y],maxcoords[x])
    player1=Player()
    new_enemy = Peon()
    enemlist = ['Peon','Ogre','Troll','Dragon']
    enemies = {'Peon':Peon,'Ogre':Ogre,'Troll':Troll,'Dragon':Dragon}
    gamecount = 1
    game_is_running = True
    picref = {'Peon':3,'Ogre':23,'Troll':11,'Dragon':31,'Knight':47}
    Ewin.draw_en_sprite(get_ch_pic(31))
    Pwin.draw_pl_sprite(get_ch_pic(picref['Knight']))
    draw_pstats()
    draw_estats()
    #game flow
    while player1.isalive and new_enemy.isalive:
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
                pot_dmg = random.randint((player1.Atk/2)*player1.Atk,player1.Atk*player1.Atk)
                if player1.AP > 9:
                    Pwin.s_feedback(new_enemy.is_attacked
                        (pot_dmg,True))
                    player1.AP -= 10
                elif player1.AP <= 9:
                    Pwin.s_feedback('noap')
                    took_action = False
            elif Swin.actions[Swin.newpos] == 'Heal':
                if player1.Potions > 0:
                    healed = random.randint(30,50)
                else:
                    healed = 0
                    took_action = False
                Pwin.h_feedback(player1.heal(healed))
        draw_pstats()
        draw_estats()
                #pass
        if took_action:
            time.sleep(.3)
            enemyattack = random.randint((new_enemy.Atk/2)*new_enemy.Atk,new_enemy.Atk*new_enemy.Atk)
            Ewin.ea_feedback(player1.is_attacked(enemyattack,False))
            draw_pstats()
            time.sleep(.4)
            if player1.defending:
                player1.Evade = player1.Evade/2
                player1.Armor = player1.Armor/2
                player1.defending = False
                draw_pstats()
            if player1.AP <= 8:
                player1.AP += 2
                draw_pstats()


    #end of program clean up
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__=='__main__':
    curses.wrapper(main)
