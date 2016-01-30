#!/usr/local/bin/python2.7

"""Window handling classes - assume a 40/40/20 split (enemy/player/status)"""

import curses

class Enemy_win(object):
    """Initialise a new enemy window with predetermined
        positions"""
    def __init__(self,h,w):
        starty, startx = 0,0 #enemy window on top
        len_y = int(round((h/5) * 2))
        len_x = w
        win = curses.newwin(len_y,len_x,starty,startx)
        win.border('|','|','-','-','+','+','+','+')
        #win.addstr(1,1,str(win.getmaxyx))
        win.refresh()

class Player_win(object):
    """Initialise a new player window with predetermined
        positions"""
    def __init__(self,h,w):
        starty, startx = int(round((h/5) * 2)), 0
        len_y = int(round((h/5) * 2))
        len_x = w
        win = curses.newwin(len_y,len_x,starty,startx)
        win.border('|','|','-','-','+','+','+','+')
        #win.addstr(1,1,str(win.getmaxyx))
        win.refresh()

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
            #set the y,x coords to list index containing each one of
            #4 entries for possible selection locations
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
        
        if confirm :
            if self.actions[self.curpos] == 'Attack':
                pass
            
            elif self.actions[self.curpos] == 'Defend':
                pass
            
            elif self.actions[self.curpos] == 'Special':
                pass
            
            elif self.actions[self.curpos] == 'Heal':
                pass


