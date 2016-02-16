"""Entites handled in-game"""
"""Richard Dunne 2016, richard.w.dunne@gmail.com"""
import random
import time

class Enemy(object):
    """Generic Enemy class"""
    def __init__(self):
        self.isalive = True
        self.ishostile = True
        self.status = []
        self.dmgcount = 0

    def is_attacked(self,dmg,special):
        if dmg <= 0:
            self.dmgcount = 0
            #counts as a miss
            return (0, 'miss')
        if special == False:
            self.full_dmg = dmg - self.Armor
            if self.full_dmg <= 0:
                self.dmgcount = 0
                return (1, 'absorb')
                #counts as an armor absorption
            else :
                self.HP -= self.full_dmg
                self.dmgcount = self.full_dmg
                if self.HP <= 0:
                    self.HP = 0
                    self.isalive = False
                return (self.full_dmg, 'hit') 
                #counts as a hit
        if special == True:
            if dmg == 16:
                return (0, 'miss')
            else :
                self.HP -= dmg
                self.dmgcount = dmg
                if self.HP <= 0:
                    self.HP = 0
                    self.isalive = False
                return (dmg, 'hits') 
                #hit, ignore armor
    def heal(self, amount):
        self.HP += amount
        return (amount, 'heal') 

class Peon(Enemy):
    """Peon enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Peon'
        self.Description = 'Orc Peon armed with a barbed mace'
        self.HP = 70
        self.Armor = 5
        self.Atk = 4
        self.Evade = 1
        self.EXP = 5

class Ogre(Enemy):
    """Ogre enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Ogre'
        self.Description = 'Ogre armed with a polearm'
        self.HP = 80
        self.Armor = 8
        self.Atk = 5
        self.Evade = 1
        self.EXP = 10

class Troll(Enemy):
    """Troll enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Troll'
        self.Description = 'Troll armed with a War-Axe'
        self.HP = 80
        self.Armor = 10
        self.Atk = 6
        self.Evade = 1
        self.EXP = 15

class Dragon(Enemy):
    """Dragon boss class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Dragon'
        self.Description = 'Green Dragon with thick scales'
        self.HP = 300
        self.Armor = 15
        self.Atk = 10
        self.Evade = 1
        self.EXP = 100

class Player(object):
    def __init__(self):
        self.defending = False
        self.isalive = True
        self.HP = 100
        self.maxhp = 100
        self.maxlevhp = 200
        self.EXP = 0
        self.explim = 20
        self.Armor = 10
        self.maxarmor = 50
        self.Atk = 6
        self.maxatk = 10 
        self.Evade = 2
        self.maxevade = 5
        #self.inventory = {'Weapons':[],'Artefacts':[],'Scrolls':[]}
        #self.weapon = ('Shortsword', 5)
        self.AP = 10
        self.Potions = 3
        self.maxpotions = 6
        self.Level = 1
        self.maxlevel = 12
        self.maxndmg = 50
        self.maxsdmg = 90
        self.expeval = 0
        self.usedspecial = False

    def is_attacked(self,dmg,hitroll=0,special=False):
        self.hitch = hitroll
        if self.defending:
            self.Armor += self.Armor
            self.Evade += 2
        if special == False:
            self.full_dmg=dmg - self.Armor
            if self.hitch > self.Evade:
                if self.full_dmg <= 0:
                    return (0,'absorb')
                    #counts as a full absorption
                else:
                    self.HP -= self.full_dmg
                if self.HP <= 0:
                   self.HP = 0
                   self.isalive = False
                return (self.full_dmg, 'hit')
            elif self.hitch <= self.Evade:
                return (0,'miss')
                #successful hit
        if special == True:
            if self.hitch > self.Evade:
                self.full_dmg = dmg 
                if self.full_dmg <= 0:
                    return (0,'evade')
                else:
                    self.HP -= self.full_dmg
                    if self.HP <= 0:
                        self.HP = 0
                        self.isalive = False
                    return (self.full_dmg, 'hits')
            elif self.hitch <= self.Evade:
                return (0,'miss')
    def heal(self, amount):
        if amount > 1 and amount < 999:
            self.HP += amount
            self.Potions -= 1
        elif amount == 0:
            return 0
        elif amount == 999:
            return 999
        return amount

