#!/usr/bin/env python2
"""control flow, instance handling"""
"""Richard Dunne 2016, richard.w.dunne@gmail.com"""

import curses
import time
import random
import os
from arena import *
from entities import *

def draw_pstats():
    pl_attrlist = ['HP','Armor','Atk','Evade','AP','Potions','Level']
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
    if doomroll >= 0 and doomroll <= 40:
        return 1
    elif doomroll >= 40 and doomroll <= 70:
        return 2 
    elif doomroll >= 70:
        return 3
    else:
        return 1

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
    enemlist = ['Peon','Ogre','Troll','Dragon']
    enemies = {'Peon':Peon,'Ogre':Ogre,'Troll':Troll,'Dragon':Dragon}
    gamecount = 1
    game_is_running = True
    picref = {'Peon':3,'Troll':24,'Ogre':45,'Dragon':66,'Knight':87,'Title':108,'Prologue':121}
    #title=68
    if (stdscr.getmaxyx()[y] < 40) or (stdscr.getmaxyx()[x] < 143):
        curses.endwin()
        print "Full screen terminal required to experience the game in SLD (super low definition)"
        return
    maxcoords = stdscr.getmaxyx() #(51,150)#(38,90)
    stdscr.refresh()
    title = Title_win(maxcoords[y],maxcoords[x])
    title.draw_title(get_ch_pic(picref['Title']))
    #title_display = True
    if title.write_prologue(get_ch_pic(picref['Prologue'])):
        title.rem_title()

    #instantiate the window layout
    Ewin = Enemy_win(maxcoords[y],maxcoords[x])
    Pwin = Player_win(maxcoords[y],maxcoords[x]) 
    Swin = Status_win(maxcoords[y],maxcoords[x])
    player1=Player()
    while player1.isalive and game_is_running:
        if gamecount % 15 != 0:
            doom = doomselector()
            if doom == 1:
                new_enemy = Peon()
                monster = 'Peon'
            if doom == 2:
                new_enemy = Ogre()
                monster = 'Ogre'
            if doom == 3:
                new_enemy = Troll()
                monster = 'Troll'
        elif gamecount % 15 == 0:
            new_enemy = Dragon()
            monster = 'Dragon'

        announce = Miniwin(5,40,maxcoords[y]/2,(maxcoords[x]/2)-12)
        if gamecount == 1:
            announce.message('Your First Opponent is: ',' ',1)
            time.sleep(1)
        else:
            announce.message('Your Next Opponent is: ',' ',1)
        time.sleep(1)
        announce.message(monster,' ',2)
        time.sleep(3)
        announce.clear_win()
        
        Ewin.draw_en_sprite(get_ch_pic(picref[monster]))
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
                return
            elif keypress == curses.KEY_RIGHT:
                Swin.actselect(1, False)
            elif keypress == curses.KEY_LEFT:
                Swin.actselect(-1, False)
            elif (keypress == curses.KEY_ENTER) or (keypress == 10) or (keypress == 13):
                took_action = True
                if Swin.actions[Swin.newpos] == 'Attack':
                    pot_dmg = random.randint(player1.Atk+6,player1.Atk*4)
                    if pot_dmg > player1.maxndmg:
                        real_dmg = player1.maxndmg
                    else:
                        real_dmg = pot_dmg
                    #TODO-create a better dmg generator
                    Pwin.a_feedback(new_enemy.is_attacked
                            (real_dmg,False))
                elif Swin.actions[Swin.newpos] == 'Defend':
                   player1.defending = True
                   if player1.AP <= 8:
                       player1.AP += 2
                   Pwin.d_feedback()
                   #player1.Armor = player1.Armor * 2
                elif Swin.actions[Swin.newpos] == 'Special':
                    player1.usedspecial = True
                    pot_dmg = player1.Atk*player1.Atk
                    if pot_dmg > player1.maxsdmg:
                        real_dmg = player1.maxsdmg
                    else:
                        real_dmg = pot_dmg
                    if player1.AP > 9:
                        hit = 3
                        if random.randint(1,3) == hit:
                            Pwin.s_feedback(new_enemy.is_attacked
                                (real_dmg,True))
                            player1.AP -= 10
                        else:
                            player1.AP -= 10
                            Pwin.s_feedback(('miss','miss'))
                    elif player1.AP <= 9:
                        Pwin.s_feedback('noap')
                        took_action = False
                elif Swin.actions[Swin.newpos] == 'Heal':
                    pot_heal = random.randint(30,50)
                    if player1.Potions > 0:
                        if player1.HP >= player1.maxhp:
                            healed = 999
                            #already at max HP
                            took_action = False
                        elif pot_heal + player1.HP > player1.maxhp:
                            healed = player1.maxhp - player1.HP
                            #can't heal past maxhp at cur level
                        else:
                            healed = pot_heal
                    elif player1.Potions <= 0:
                        healed = 0
                        took_action = False
                    else:
                        healed = pot_heal
                    Pwin.h_feedback(player1.heal(healed))
            draw_pstats()
            draw_estats()
            #enemy turn
            if took_action:
                if new_enemy.isalive:
                    if player1.defending:
                        if random.randint(1,3) == 1:
                            en_hitroll = random.randint(0,5) #if defending, en has a chance to fiercely hit
                            enemyattack = random.randint(new_enemy.Atk*2, new_enemy.Atk*new_enemy.Atk+new_enemy.Atk + player1.Level)
                            Ewin.ea_feedback(player1.is_attacked(enemyattack,en_hitroll,True))
                            time.sleep(.4)
                        else:
                            en_hitroll = random.randint(0,10)
                            enemyattack = random.randint(new_enemy.Atk,new_enemy.Atk*new_enemy.Atk)
                            Ewin.ea_feedback(player1.is_attacked(enemyattack,en_hitroll,False))

                    else:
                        en_hitroll = random.randint(0,10)
                        enemyattack = random.randint(new_enemy.Atk*2,new_enemy.Atk*new_enemy.Atk)
                        Ewin.ea_feedback(player1.is_attacked(enemyattack,en_hitroll,False))
                    draw_pstats()
                    time.sleep(.4)
                if player1.HP <= 0:
                    death_notice = Miniwin(10,60,maxcoords[y]/3,(maxcoords[x]/2)-15)
                    death_notice.message('You have been slain.',' ',2)
                    time.sleep(2)
                    death_notice.message('Final score: ',' ',3)
                    time.sleep(3)
                    death_notice.message(str(player1.EXP),' ',4)
                    time.sleep(2)
                    death_notice.message('Thanks for playing!',' ',5)
                    time.sleep(4)
                    death_notice.clear_win()
                    return
                if player1.defending:
                    player1.Evade = player1.Evade /2
                    player1.Armor = player1.Armor /2
                    player1.defending = False
                    draw_pstats()
                if not player1.usedspecial:
                    if player1.AP <= 8:
                        player1.AP += 2
                    draw_pstats()
                player1.usedspecial = False
        
        Ewin.draw_en_sprite(get_ch_pic(picref[monster]),True)#call True to remove ascii
        en_ack_win = Miniwin(7,55,maxcoords[y]/3,(maxcoords[x]/2)-15)
        en_ack_win.message('You have slain ' + new_enemy.Type,' ',2)
        player1.EXP += new_enemy.EXP
        time.sleep(1)
        gamecount += 1
        if gamecount > 15:
            final_summary = Miniwin(10,60,maxcoords[y]/3,(maxcoords[x]/2)-15)
            final_summary.message('Congratulations!',' ',2)
            time.sleep(.5)
            final_summary.message('You have defeated the Alpha Dragon.',' ',3)
            time.sleep(1)
            final_summary.message('Your final score :',' ',4)
            time.sleep(.2)
            score = '--> ' + str(player1.EXP)
            final_summary.message(score,' ',6)
            time.sleep(1)
            final_summary.message('Thanks for playing!',' ',8)
            time.sleep(5)
            final_summary.clear_win()
            return
        if player1.HP % 2 == 0:
            en_ack_win.message('Searching the enemy corpse you find 2 potions',' ',4)
            if player1.Potions <= 6:
                player1.Potions += 2
                time.sleep(2)
            elif player1.Potions >=8:
                en_ack_win.message('Cannot hold any more potions!',' ',5)
                time.sleep(2)
        else:
            en_ack_win.message('You find a potion near to the enemy corpse',' ',4)
            if player1.Potions <= 7:
                player1.Potions += 1
                time.sleep(2)
            elif player1.Potions >=8:
                en_ack_win.message('Cannot hold any more potions!',' ',5)
                time.sleep(2)
        en_ack_win.clear_win()
        lev_evaluated = False
        levels = 0
        if (player1.EXP + new_enemy.EXP) >= player1.explim:
            summary = Miniwin(15,60,maxcoords[y]/3,(maxcoords[x]/2)-15)
            while player1.expeval >= 0:
                player1.expeval = ((player1.EXP + new_enemy.EXP) - player1.explim)
                if player1.expeval >= 0:
                    levels += 1
                player1.explim += 20
            player1.EXP += new_enemy.EXP
            player1.expeval = 0
            for lv in range(levels):
                summary.message('                                                   ',' ',1)
                time.sleep(.3)
                summary.message('Level Up! Welcome to Level '+str(player1.Level+1),
                        ' ',1)
                player1.Level += 1
                if player1.HP + 20 > player1.maxlevhp:
                    player1.HP = player1.maxlevhp
                    summary.message('HP has been maxed out   ','reline',2)
                    time.sleep(2)
                else: 
                    player1.maxhp += 20
                    summary.message('Max HP increased by 20   ','reline',2)
                    time.sleep(1)
                if (player1.Armor + 1) > player1.maxarmor:
                    summary.message('Armor has been maxed out','reline',4)
                    player1.Armor = player1.maxarmor
                    time.sleep(1)
                else:
                    player1.Armor += 1
                    summary.message('Armor increased by 1    ','reline',4)
                    time.sleep(1)
                if (player1.Atk + 1) > player1.maxatk:
                    player1.Atk = player1.maxatk
                    summary.message('Atk has been maxed out ','reline',6)
                    time.sleep(1)
                else:
                    player1.Atk += 1
                    summary.message('Atk increased by 1  ','reline',6)
                    time.sleep(1)
                if (player1.Evade + 1) > player1.maxevade:
                    player1.Evade = player1.maxevade
                    summary.message('Evade has been maxed out  ','reline',8)
                    time.sleep(1)
                else:
                    player1.Evade += 1
                    summary.message('Evade increased by 1     ','reline',8)
                    time.sleep(1)
            time.sleep(2)
            summary.clear_win()

        draw_pstats()


    #end of program clean up
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__=='__main__':
    curses.wrapper(main)
