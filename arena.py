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
        self.actions = ['Attack','Defend','Special','Heal']
        starty, startx = int(round((h/5) * 4)), 0
        len_y = int(round(h/5))
        len_x = w
        win = curses.newwin(len_y,len_x,starty,startx)
        win.border('|','|','-','-','+','+','+','+')
        #win.addstr(1,1,str(win.getmaxyx))

        for i in range(4):
            padding = ((((len_x/4)*i) / len(self.actions[i])) + 24) #hack to avoid 0'th' index returning 0\
                    #this needs to be changed when factoring in different sized terminals.  TODO
            self.textpos.update({self.actions[i]:((len_y/2)+1,(((len_x/4)*i) + (padding/2))+2)})
            if padding <= 1:
                win.addstr(len_y/2,((len_x/4)*i) + (padding/2), self.actions[i][:2])
            else:
                win.addstr(len_y/2,((len_x/4)*i) + (padding/2), self.actions[i]) #ugly, but ok for now
            win.addch((len_y/2)+1,(((len_x/4)*i) + (padding/2))+2, ord('^'))
            win.addstr(2,1,str(self.textpos))
        win.refresh()

