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
        win.refresh()

class Status_win(object):
    """Initialise a new status window with predetermined
        positions"""
    def __init__(self,h,w):
        starty, startx = int(round((h/5) * 4)), 0
        len_y = int(round(h/5))
        len_x = w
        win = curses.newwin(len_y,len_x,starty,startx)
        win.border('|','|','-','-','+','+','+','+')
        win.refresh()
