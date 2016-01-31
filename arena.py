#!/usr/local/bin/python2.7

"""Window writing and handling classes - assume a 40/40/20 split (enemy/player/status)"""

import curses

class Enemy_win(object):
    """Initialise a new enemy window with predetermined
        positions"""
    def __init__(self,h,w):
        self.starty, self.startx = 0,0 #enemy window on top
        self.len_y = int(round((h/5) * 2))
        self.len_x = w
        self.win = curses.newwin(self.len_y,self.len_x,self.starty,self.startx)
        self.win.border('|','|','-','-','+','+','+','+')
        self.win.refresh()

    def update_e_status(self, kind = 0, value = 0):
        self.to_update = kind
        self.valupdate = value
        self.kindlist = ['HP:','Armor:','Atk Dmg:','Evade:']
        if self.to_update == 0: #if just writing first instance
            for index,item in enumerate(self.kindlist,1):
                self.win.addstr(index,self.len_x - 12,item)
                self.win.refresh()
        if self.to_update > 0:
            self.win.addstr(self.to_update,1,'                      ')
            self.win.addstr(self.to_update,1,self.kindlist[self.to_update]+str(self.valupdate))
    def ea_feedback(self,result):
        """Write output to player screen when attacking"""
        if result[1] == 'miss':
            resultstring = 'Enemy attack missed'
        elif result[1] == 'absorb':
            resultstring = 'Your armor absorbs the enemy attack'
        elif result[1] == 'hit':
            resultstring = 'Enemy hits you for ' + str(result[0]) + ' damage'
        elif result[1] == 'evade':
            resultstring = 'Enemy strikes but you dodge the blow'
        self.win.addstr(self.len_y-2,self.len_x -41,' '*40)
        self.win.addstr(self.len_y-2,self.len_x -(len(resultstring)+1),resultstring)
        self.win.refresh()

class Player_win(object):
    """Initialise a new player window with predetermined
        positions"""
    def __init__(self,h,w):
        self.starty, self.startx = int(round((h/5) * 2)), 0
        self.len_y = int(round((h/5) * 2))
        self.len_x = w
        self.win = curses.newwin(self.len_y,self.len_x,self.starty,self.startx)
        self.win.border('|','|','-','-','+','+','+','+')
        #win.addstr(1,1,str(win.getmaxyx))
        self.subsect = 3 #number of subsections in window
        self.win.refresh()

    def update_p_status(self, kind = 0, value = 0):
        self.to_update = kind
        self.valupdate = value
        self.subsectlen = self.len_x / self.subsect
        self.xtextwrite = self.subsectlen - 19#possible length of kinds to write
        self.kindlist = ['HP:','AP:','Armor:','Stamina:','Atk Dmg:','Evade:','Healing Potions:','Lvl:','Exp:']
        if self.to_update == 0: #if just writing first instance
            for index,item in enumerate(self.kindlist,1):
                self.win.addstr(index,1,item)
                self.win.refresh()
        if self.to_update > 0:
            self.win.addstr(self.to_update,1,'                      ')
            self.win.addstr(self.to_update,1,self.kindlist[self.to_update]+str(self.valupdate))
    
    def a_feedback(self,result):
        """Write output to player screen when attacking"""
        if result[1] == 'miss':
            resultstring = 'You attack but miss your target'
        elif result[1] == 'absorb':
            resultstring = 'Your attack barely dents its armor'
        elif result[1] == 'hit':
            resultstring = 'Your attack hits for ' + str(result[0]) + ' damage'
        self.win.addstr(self.len_y-2,self.len_x -41,' '*40)
        self.win.addstr(self.len_y-2,self.len_x -(len(resultstring)+1),resultstring)
        self.win.refresh()

    def d_feedback(self):
        """Write output to player screen while defending"""
        resultstring = 'You defend.  Armor, Evade increase.'
        self.win.addstr(self.len_y-2,self.len_x -41,' '*40)
        self.win.addstr(self.len_y-2,self.len_x - (len(resultstring)+1)
                ,resultstring)
        self.win.refresh()

    def s_feedback(self,result):
        """Write output to player screen when attacking"""
        if result[1] == 'miss':
            resultstring = 'Your special attack misses!'
        elif result[1] == 'hits':
            resultstring = 'Your gore the enemy for ' +str(result[0])+ ' damage'
        self.win.addstr(self.len_y-2,self.len_x -41,' '*40)
        self.win.addstr(self.len_y-2,self.len_x -(len(resultstring)+1)
                ,resultstring)
        self.win.refresh()
    
    def h_feedback(self,amount):
        """Write output to player screen when healed"""
        resultstring = 'Used a potion.  Healed by '+str(amount)
        self.win.addstr(self.len_y-2,self.len_x -41,' '*40)
        self.win.addstr(self.len_y-2,self.len_x -(len(resultstring)+len(str(amount))-1) ,resultstring)
        self.win.refresh()


class Status_win(object):
    """Initialise a new status window with predetermined
        positions"""
    def __init__(self,h,w):
        subsect = 4 #no. of subsections in window
        self.textpos = {}
        self.posref = []
        self.actions = ['Attack','Defend','Special','Heal']
        self.newpos = 0
        starty, startx = int(round((h/5) * subsect)), 0
        self.len_y = int(round(h/5))
        self.len_x = w
        subsect_len = self.len_x / subsect
        self.win = curses.newwin(self.len_y,self.len_x,starty,startx)
        self.win.border('|','|','-','-','+','+','+','+')
        self.win.addstr(2,2,'Shift and q to quit')    
        for index, value in enumerate(self.actions, 1):
            padding = (subsect_len - len(value))/2
            xstrloc = (subsect_len*index)- padding - len(value) 
            self.textpos.update({value:((self.len_y/2)+1,xstrloc + (len(value)/2))})
            self.posref.append(self.textpos[value])
            if padding <= 1:
                self.win.addstr(self.len_y/2,xstrloc,value[:2])#len/4 because we have 4 opts
            else:
                self.win.addstr(self.len_y/2,xstrloc,value)
        
        self.win.addch(self.posref[0][0],self.posref[0][1], ord('^'))
        self.win.addstr(self.len_y-2, self.len_x -75, 'Standard Attack with your main weapon. Higher chance of hit with less dmg.')
        self.win.refresh()
    
    def actselect(self,way=0,confirm=False):
        """move the selection icon and handle an enter key press to 
            activate a selection"""
        self.curpos = self.newpos
        infoloc_y, infoloc_x = self.len_y-2, self.len_x - 75
        if not confirm:
            if self.newpos + way < 0:
                self.newpos = 4
            
            if self.newpos + way > 3:
                self.newpos = 0
            
            else :
                self.newpos += way
            
            if self.newpos == 0:
                self.win.addstr(infoloc_y,infoloc_x, '                                                                          ')
                self.win.addstr(infoloc_y,infoloc_x, 'Standard Attack with your main weapon. Higher chance of hit with less dmg.')
            elif self.newpos == 1:
                self.win.addstr(infoloc_y,infoloc_x, '                                                                          ')
                self.win.addstr(infoloc_y,infoloc_x, 'Increase armor and evade chance for the next enemy attack.')
            elif self.newpos == 2:
                self.win.addstr(infoloc_y,infoloc_x, '                                                                          ')
                self.win.addstr(infoloc_y,infoloc_x,'Double damage, ignore armor, lower chance of hit.')
            elif self.newpos == 3:
                self.win.addstr(infoloc_y,infoloc_x, '                                                                          ')
                self.win.addstr(infoloc_y,infoloc_x, 'Use a potion to heal HP.')
            
            self.addy, self.addx = self.posref[self.newpos]
            self.remy, self.remx = self.posref[self.curpos]
            self.win.addch(self.addy, self.addx, ord('^'))
            self.win.addch(self.remy, self.remx, ord(' '))
            self.win.refresh()
        
