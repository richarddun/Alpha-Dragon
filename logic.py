#!/usr/local/bin/python2.7
"""control flow, instance handling"""
import curses
import time
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
    maxcoords = stdscr.getmaxyx()
    stdscr.refresh()
    #instantiate the window layout
    Ewin = Enemy_win(maxcoords[y],maxcoords[x])
    Pwin = Player_win(maxcoords[y],maxcoords[x]) 
    Swin = Status_win(maxcoords[y],maxcoords[x])
    Pwin.update_p_status()
    Ewin.update_e_status()
    player1=Player()
    new_enemy = Peon()
    enemies = {'Peon':Peon,'Ogre':Ogre,'Troll':Troll,'Dragon':Dragon}
    gamecount = 1
    game_is_running = True
    #game flow
    while game_is_running and player1.isalive():
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
            if Swin.actions[Swin.curpos] == 'Attack':
                pot_dmg = random.randint(5,20)
                #TODO-create a better dmg generator
                Pwin.a_feedback(new_enemy.is_attacked
                        (pot_dmg,False))
                if new_enemy.dmgcount > 0:
                    Ewin.update_e_status(0,new_enemy.dmgcount)
            elif Swin.actions[Swin.curpos] == 'Defend':
                player1.defending = True
                Pwin.d_feedback()
            elif Swin.actions[Swin.curpos] == 'Special':
                pot_dmg = random.randint(15,40)
                Pwin.s_feedback(new_enemy.is_attacked
                        (pot_dmg,True)
            elif Swin.actions[Swin.curpos] == 'Heal':
                if player1.potions > 0:
                    healed = random.randint(30,50)
                    Pwin.h_feedback(player1.heal(healed))

                #pass
        if took_action:
            if new_enemy.is_hostile:
                enemyattack = 





    #end of program clean up
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__=='__main__':
    curses.wrapper(main)
