"""Window writing and handling classes - assume a 40/40/20 split (enemy/player/status)"""

from unicurses import *
import time

class Title_win(object):
    def __init__(self,h,w):
        self.starty, self.startx = 0,0
        self.len_y,self.len_x = self.starty, w
        self.win = newwin(self.len_y,self.len_x,self.starty,self.startx)

    def draw_title(self,enlist):
        yindex = 1
        xreturn = (self.len_x / 2) - 25
        xloc = xreturn
        for char in enlist:
            if char == '"':
                yindex += 1
                xloc = xreturn
                pass
            if char != '"':
                pxl = ord(char)
                #self.win.delch(yindex,xloc)
                mvwaddch(self.win,yindex,xloc,pxl)
                xloc += 1
        wrefresh(self.win)

    def write_prologue(self,string):
        yindex = 20
        xreturn = (self.len_x /2) -25
        xloc = xreturn
        writing_prologue = True
        halfdelay(1)
        for char in string:
            brkchar = getch()
            if brkchar == ord('Q'):
                nocbreak()
                cbreak()
                return True
                break
            if char == '"':
                time.sleep(2)
                yindex += 1
                xloc = xreturn
            if char != '"':
                txt = ord(char)
                mvwaddch(self.win,yindex,xloc,txt)
                wrefresh(self.win)
                #time.sleep(.1)
                xloc += 1
        time.sleep(4)
        return True

    def rem_title(self):
        werase(self.win)
        wrefresh(self.win)

class Enemy_win(object):
    """Initialise a new enemy window with predetermined
        positions"""
    def __init__(self,h,w):
        self.firstrun = True
        self.starty, self.startx = 0,int(round(w/2)) #enemy window on right
        self.len_y = int(round(h * .7))#70% of total win
        self.len_x = int(round(w / 2))
        self.win = newwin(self.len_y,self.len_x,self.starty,self.startx)
        #self.win.border('|','|','-','-','+','+','+','+')
        wrefresh(self.win)

    def redraw(self):
        wrefresh(self.win)

    def update_e_status(self,index,stat):
        writestring = str(stat[0]) + ':' + str(stat[1])
        mvwaddstr(self.win,index,self.len_x-47,' '*47)
        mvwaddstr(self.win,index,self.len_x-len(writestring)-1,writestring)
        wrefresh(self.win)

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
        elif result[1] == 'hits':
            resultstring = 'Enemy crushes your defense! '+str(result[0])+' damage taken!'
        mvwaddstr(self.win,self.len_y-2,self.len_x -46,' '*45)
        wrefresh(self.win)
        time.sleep(.1)
        mvwaddstr(self.win,self.len_y-2,self.len_x -(len(resultstring)+1),resultstring)
        wrefresh(self.win)
        
    def draw_en_sprite(self,enlist,destruct=False):
        yindex = int(round(self.len_y * .3))
        xreturn = int(round(self.len_x * .1))
        xloc = xreturn
        for char in enlist:
            if char == '"':
                yindex += 1
                xloc = xreturn
                pass
            if char != '"':
                if destruct == True:
                    pxl = ord(' ')
                elif destruct == False:
                    pxl = ord(char)
                #self.win.delch(yindex,xloc)
                mvwaddch(self.win,yindex,xloc,pxl)
                xloc += 1
        wrefresh(self.win)

    def clear_win(self):
        werase(self.win)
        wrefresh(self.win)

class Player_win(object):
    """Initialise a new player window with predetermined
        positions"""
    def __init__(self,h,w):
        self.starty, self.startx = 0,0#player win on left
        self.len_y = int(round(h * .7))
        self.len_x = int(round(w/2))
        self.win = newwin(self.len_y,self.len_x,self.starty,self.startx)
        #self.win.border('|','|','-','-','+','+','+','+')
        #win.addstr(1,1,str(win.getmaxyx))
        #self.subsect = 3 #number of subsections in window
        wrefresh(self.win)

    def redraw(self):
        wrefresh(self.win)

    def update_p_status(self,index,stat):
        self.writestring = str(stat[0]) + ':' + str(stat[1])
        mvwaddstr(self.win,index,1,'          ')
        mvwaddstr(self.win,index,1,self.writestring)
        wrefresh(self.win)

    def a_feedback(self,result):
        """Write output to player screen when attacking"""
        if result[1] == 'miss':
            resultstring = 'You attack but miss your target'
        elif result[1] == 'absorb':
            resultstring = 'Your attack barely dents its armor'
        elif result[1] == 'hit':
            resultstring = 'Your attack hits for ' + str(result[0]) + ' damage'
        mvwaddstr(self.win,self.len_y-2,self.len_x -44,' '*43)
        wrefresh(self.win)
        time.sleep(.1)
        mvwaddstr(self.win,self.len_y-2,self.len_x -(len(resultstring)+1),resultstring)
        wrefresh(self.win)

    def d_feedback(self):
        """Write output to player screen while defending"""
        resultstring = 'You defend.  Armor, Evade increase.'
        mvwaddstr(self.win,self.len_y-2,self.len_x -41,' '*40)
        mvwaddstr(self.win,self.len_y-2,self.len_x - (len(resultstring)+1)
                ,resultstring)
        wrefresh(self.win)

    def s_feedback(self,result):
        """Write output to player screen when attacking"""
        if result[1] == 'miss':
            resultstring = 'Your special attack misses!'
        elif result[1] == 'hits':
            resultstring = 'Your gore the enemy for ' +str(result[0])+ ' damage'
        elif result == 'noap':
            resultstring = 'No AP to use this attack'
        mvwaddstr(self.win,self.len_y-2,self.len_x -44,' '*43)
        wrefresh(self.win)
        time.sleep(.1)
        mvwaddstr(self.win,self.len_y-2,self.len_x -(len(resultstring)+1)
                ,resultstring)
        wrefresh(self.win)
    
    def h_feedback(self,amount):
        """Write output to player screen when healed"""
        if amount == 0:
            resultstring = 'No potions left!'
            mvwaddstr(self.win,self.len_y-2,self.len_x -44,' '*44)
            wrefresh(self.win)
            time.sleep(.1)
            mvwaddstr(self.win,self.len_y-2,
                    (self.len_x - len(resultstring))-1 ,resultstring)
            wrefresh(self.win)
        elif amount == 999:
            resultstring = 'Already at max health!'
            mvwaddstr(self.win,self.len_y-2,self.len_x -44,' '*44)
            wrefresh(self.win)
            time.sleep(.1)
            mvwaddstr(self.win,self.len_y-2,
                    (self.len_x - len(resultstring))-1 ,resultstring)
            wrefresh(self.win)
        else:
            resultstring = 'Used a potion.  Healed by '+str(amount)
            mvwaddstr(self.win,self.len_y-2,self.len_x -44,' '*44)
            wrefresh(self.win)
            time.sleep(.1)
            mvwaddstr(self.win,self.len_y-2,self.len_x -
                (len(resultstring)+len(str(amount))) ,resultstring)
            wrefresh(self.win)
           
    def draw_pl_sprite(self,enlist):
        yindex = int(round(self.len_y * .3))
        xreturn = int(round(self.len_x * .2))
        xloc = xreturn
        for char in enlist:
            if char == '"':
                yindex += 1
                xloc = xreturn
                pass
            if char != '"':
                pxl = ord(char)
                #self.win.delch(yindex,xloc)
                mvwaddch(self.win,yindex,xloc,pxl)
                xloc += 1
        wrefresh(self.win)

    def clear_win(self):
        werase(self.win)
        wrefresh(self.win)

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
        self.win = newwin(self.len_y,self.len_x,starty,startx)
        wborder(self.win,'|','|','-','-','+','+','+','+')
        mvwaddstr(self.win,2,2,'Shift and q to quit')    
        for index, value in enumerate(self.actions, 1):
            padding = (subsect_len - len(value))/2
            xstrloc = (subsect_len*index)- padding - len(value) 
            self.textpos.update({value:
                ((self.len_y/2)+1,xstrloc + (len(value)/2))})
            self.posref.append(self.textpos[value])
            if padding <= 1:
                mvwaddstr(self.win,self.len_y/2,xstrloc,value[:2])
            else:
                mvwaddstr(self.win,self.len_y/2,xstrloc,value)
        
        mvwaddch(self.win,self.posref[0][0],self.posref[0][1], ord('^'))
        mvwaddstr(self.win,self.len_y-2,
            self.len_x -75,'Standard Attack '+
            'with your main weapon. Higher chance of hit '+
            'with less dmg.')
        wrefresh(self.win)
    
    def redraw(self):
        wrefresh(self.win)

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
                mvwaddstr(self.win,infoloc_y,infoloc_x, '                                                                          ')
                mvwaddstr(self.win,infoloc_y,
                    infoloc_x,'Standard Attack '+
                    'with your main weapon. Higher chance '+
                    'of hit with less dmg.')
            elif self.newpos == 1:
                mvwaddstr(self.win,infoloc_y,infoloc_x,'                                                                          ')
                mvwaddstr(self.win,infoloc_y,infoloc_x, 
                        'Increase armor and evade chance '+
                        'for the next enemy attack.')
            elif self.newpos == 2:
                mvwaddstr(self.win,infoloc_y,infoloc_x, '                                                                          ')
                mvwaddstr(self.win,infoloc_y,infoloc_x,
                        'Double damage, ignore armor, '+
                        'lower chance of hit.')
            elif self.newpos == 3:
                mvwaddstr(self.win,infoloc_y,infoloc_x, '                                                                          ')
                mvwaddstr(self.win,infoloc_y,infoloc_x, 
                        'Use a potion to heal HP.')
            
            self.addy, self.addx = self.posref[self.newpos]
            self.remy, self.remx = self.posref[self.curpos]
            mvwaddch(self.win,self.addy, self.addx, ord('^'))
            mvwaddch(self.win,self.remy, self.remx, ord(' '))
            wrefresh(self.win)

class Miniwin(object):
    """Mini Window for interim updates"""
    def __init__(self,h,w,starty,startx):
        self.leny,self.lenx = h, w
        self.win = newwin(self.leny,self.lenx,starty,startx)
        wborder(self.win,'|','|','-','-','+','+','+','+')
        wrefresh(self.win)

    def message(self,string,control=' ',yindex=1):
        self.msg = string
        self.ystartpoint,self.xstartpoint = yindex,5
        if control == 'remline':
            mvwaddstr(self.win,self.ystartpoint,self.xstartpoint,' '*18)
            wrefresh(self.win)
        if control == 'reline':
            mvwaddstr(self.win,self.ystartpoint,self.xstartpoint,' '*18)
            mvwaddstr(self.win,self.ystartpoint,self.xstartpoint,self.msg)
            wrefresh(self.win)
        elif control == ' ':
            try:
                mvwaddstr(self.win,self.ystartpoint,self.xstartpoint,self.msg)
                wrefresh(self.win)
            except:
                pass

    def clear_win(self):
        werase(self.win)
        wrefresh(self.win)




