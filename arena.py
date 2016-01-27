#!/usr/local/bin/python2.7

"""Window handling classes - assume a 40/40/20 split (enemy/player/status)"""

import curses

class Enemy_win(object):
    """Initialise a new enemy window with predetermined
        positions"""
    def __init__(self,h,w):
        win = curses.newwin(h,w,y,x)
        win.border('|','|','-','-','+','+','+','+')
        win.refresh()

class Player_win(object):
    """Initialise a new player window with predetermined
        positions"""
    def __init__(self,h,w):
        win = curses.newwin(h,w,y,x)
        win.border('|','|','-','-','+','+','+','+')
        win.refresh()

class Status_win(object):
    """Initialise a new status window with predetermined
        positions"""
    def __init__(self,h,w):
        win = curses.newwin(h,w,y,x)
        win.border('|','|','-','-','+','+','+','+')
        win.refresh()
