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
    stdscr.refresh()
    Ewin = Enemy_win(maxcoords[y],maxcoords[x])
    Pwin = Player_win(maxcoords[y],maxcoords[x]) 
    Swin = Status_win(maxcoords[y],maxcoords[x])
    
    
    
    p = stdscr.getch()



    #end of program clean up
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

if __name__=='__main__':
    curses.wrapper(main)
