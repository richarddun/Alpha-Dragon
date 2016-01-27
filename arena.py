#!/usr/local/bin/python2.7

"""Window handling classes"""

import curses

class Drawwin(object):
    """Initialise with a new window at height,width,y,x"""
    def __init__(self,h,w,y,x):
        self.win = curses.newwin(h,w,y,x)
        self.win.refresh()
    def draw_border(self):
        """draw a border"""
        self.win.border('|','|','-','-','+','+','+','+')
        self.win.refresh()
