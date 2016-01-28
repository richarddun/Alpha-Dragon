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
        self.textpos = {}
        self.posref = []
        self.actions = ['Attack','Defend','Special','Heal']
        self.newpos = 3
        starty, startx = int(round((h/5) * 4)), 0
        len_y = int(round(h/5))
        len_x = w
        self.win = curses.newwin(len_y,len_x,starty,startx)
        self.win.border('|','|','-','-','+','+','+','+')
        #win.addstr(1,1,str(win.getmaxyx))

        for i in range(4):
            padding = ((((len_x/4)*i) / len(self.actions[i])) + 24) 
                    #the +24 is a hack to avoid 0'th' index returning 0\
                    #this needs to be changed when factoring in different 
                    #sized terminals.  TODO
            self.textpos.update({self.actions[i]:((len_y/2)+1,(((len_x/4)*i) + 
                (padding/2))+2)})#add dict key/values for each action to 
                                 #contain the corresponding y,x (plus 1 to
                                 #y to ensure it is ref'd below by 1 row)
            if padding <= 1:
                self.win.addstr(len_y/2,((len_x/4)*i) + (padding/2), 
                        self.actions[i][:2])#len/4 because we have 4 opts
        #padding if/ else  blocks could be removed with a 
        #'check terminal size' flow.  they seem sub-optimal
            else:
                self.win.addstr(len_y/2,((len_x/4)*i) + (padding/2), 
                        self.actions[i]) 
        #win.addch((len_y/2)+1,((len_x/4)*0 + (padding/2))+2, ord('^'))
        for action in self.actions:
            self.posref.append(self.textpos[action])
        self.win.addch(self.posref[0][0],self.posref[0][0] + 9, ord('^'))
        #win.addstr(3,1,str(self.posref)) just debugging
        #win.addstr(2,1,str(self.textpos)) just debugging 
        self.win.refresh()
    def actselect(self,way=0,confirm=False):
        """move the selection icon and handle an enter key press to 
            activate a selection"""
        self.curpos = self.newpos
        if not confirm:
            if self.newpos + way < 0:
                self.newpos = 4
            if self.newpos + way > 3:
                self.newpos = 0
            else :
                self.newpos += way
            #set the y,x coords to list index containing each one of
            #4 entries for possible selection locations
            self.addy, self.addx = self.posref[self.newpos]
            self.remy, self.remx = self.posref[self.curpos]
            self.win.addch(self.addy, self.addx, ord('^'))
            self.win.addch(self.remy, self.remx, ord(' '))
            self.win.refresh()
        if confirm :
            #'Attack','Defend','Special','Heal'
            if self.actions[self.curpos] == 'Attack':
                pass
            elif self.actions[self.curpos] == 'Defend':
                pass
            elif self.actions[self.curpos] == 'Special':
                pass
            elif self.actions[self.curpos] == 'Heal':
                pass


