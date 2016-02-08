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
        self.HP = 50
        self.Armor = 2
        self.Atk = 2
        self.Evade = 1
        self.EXP = 10

class Ogre(Enemy):
    """Ogre enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Ogre'
        self.Description = 'Ogre armed with a polearm'
        self.HP = 90
        self.Armor = 5
        self.Atk = 4
        self.Evade = 1
        self.EXP = 30

class Troll(Enemy):
    """Troll enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Troll'
        self.Description = 'Troll armed with a War-Axe'
        self.HP = 130
        self.Armor = 10
        self.Atk = 4
        self.Evade = 1
        self.EXP = 50

class Dragon(Enemy):
    """Dragon boss class"""
    def __init__(self):
        Enemy.__init__(self)
        self.Type = 'Dragon'
        self.Description = 'Green Dragon with thick scales'
        self.HP = 450
        self.Armor = 15
        self.Atk = 4
        self.Evade = 1
        self.EXP = 150

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

    def is_attacked(self,dmg,special):
        self.full_dmg=dmg
        if self.defending:
            self.Evade += self.Evade
            self.Armor += self.Armor
        if self.full_dmg <= 0:
            #counts as a miss or absorption
            return (0, 'miss')
        if special == False:
            if self.full_dmg <= 0:
                return (0,'absorb')
                #counts as a full absorption
            else :
                self.HP -= self.full_dmg
                if self.HP <= 0:
                   self.HP = 0
                   self.isalive = False
                return (self.full_dmg, 'hit') 
                #successful hit
        if special == True:
            self.full_dmg = dmg - self.Evade
            if self.full_dmg <= 0:
                return (0,'evade')
            #counts as an evasion
            else:
                self.HP -= self.full_dmg
                if self.HP <= 0:
                    self.HP = 0
                    self.isalive = False
                return (self.full_dmg, 'hits')
                #didn't evade, full hit no armor count
    def heal(self, amount):
        if amount > 0:
            self.HP += amount
            self.Potions -= 1
        if amount == 0:
            return 0
        return amount

