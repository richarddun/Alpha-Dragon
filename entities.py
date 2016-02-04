"""Entites handled in-game"""

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
                return (self.full_dmg, 'hit') 
                #counts as a hit
        if special == True:
            if dmg == 16:
                return (0, 'miss')
            else :
                self.HP -= dmg
                self.dmgcount = dmg
                return (dmg, 'hits') 
                #hit, ignore armor
    def heal(self, amount):
        self.HP += amount
        return (amount, 'heal') 

class Peon(Enemy):
    """Peon enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Peon'
        self.description = 'Orc Peon armed with a barbed mace'
        self.HP = 30
        self.Armor = 0
        self.Atk = 2
        self.Evade = 1

class Ogre(Enemy):
    """Ogre enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Ogre'
        self.description = 'Ogre armed with a polearm'
        self.HP = 40
        self.Armor = 20
        self.Atk = 4
        self.Evade = 1

class Troll(Enemy):
    """Troll enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Troll'
        self.description = 'Troll armed with a War-Axe'
        self.HP = 40
        self.Armor = 20
        self.Atk = 4
        self.Evade = 1

class Dragon(Enemy):
    """Dragon boss class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Dragon'
        self.description = 'Green Dragon with thick scales'
        self.HP = 40
        self.Armor = 20
        self.Atk = 4
        self.Evade = 1

class Player(object):
    def __init__(self):
        self.defending = False
        self.isalive = True
        self.HP = 100
        self.Armor = 0
        self.Atk = 5
        self.Evade = 2
        #self.inventory = {'Weapons':[],'Artefacts':[],'Scrolls':[]}
        #self.weapon = ('Shortsword', 5)
        self.AP = 10
        self.Potions = 3

    def is_attacked(self,dmg,special):
        self.full_dmg=dmg
        if self.defending:
            self.Evade += self.Evade
            self.Armor += self.Armor
        if self.full_dmg <= 0:
            #counts as a miss or absorption
            return (0, 'miss')
        if special == False:
            self.full_dmg -= self.Armor
            if self.full_dmg <= 0:
                return (0,'absorb')
                #counts as a full absorption
            else :
                self.HP -= self.full_dmg
                return (self.full_dmg, 'hit') 
                #successful hit
        if special == True:
            self.full_dmg = dmg - self.Evade
            if self.full_dmg <= 0:
                return (0,'evade')
            #counts as an evasion
            else:
                self.HP -= self.full_dmg
                return (self.full_dmg, 'hits')
                #didn't evade, full hit no armor count
        if self.defending:
            self.Evade -= self.Evade
            self.Armor -= self.Armor
            self.defending = False
    def heal(self, amount):
        if amount > 0:
            self.HP += amount
            self.Potions -= 1
        if amount == 0:
            return 0
        return amount

