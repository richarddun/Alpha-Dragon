#!/usr/local/bin/python2.7

import curses
import time
from arena import *

def main(win):
    global stdscr
    stdscr = win
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)
    y,x=0,1
    maxcoords = stdscr.getmaxyx()
    win1 = Drawwin(maxcoords[y]/2,maxcoords[x],0,0)
    win2 = Drawwin(maxcoords[y]/2,maxcoords[x],maxcoords[y]/2,0)
    win1.draw_border()
    win2.draw_border()
    p = stdscr.getch()
    #end of program clean up
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

if __name__=='__main__':
    curses.wrapper(main)
