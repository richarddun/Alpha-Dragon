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
            full_dmg = dmg - (self.armor/2)
            if full_dmg <= 0:
                self.dmgcount = 0
                return (1, 'absorb')
                #counts as an armor absorption
            else :
                self.hp -= full_dmg
                self.dmgcount = full_dmg
                return (full_dmg, 'hit') 
                #counts as a hit
        if special == True:
            if dmg == 16:
                return (0, 'miss')
            else :
                self.hp -= dmg
                self.dmgcount = dmg
                return (dmg, 'hits') 
                #hit, ignore armor

    def heal(self, amount):
        self.hp += amount
        return (amount, 'heal') 

class Peon(Enemy):
    """Peon enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Peon'
        self.description = 'Orc Peon armed with a barbed mace'
        self.armor = 10
        self.hp = 30
        self.atk = 2

class Ogre(Enemy):
    """Ogre enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Ogre'
        self.description = 'Ogre armed with a polearm'
        self.armor = 20
        self.hp = 40
        self.atk = 4

class Troll(Enemy):
    """Troll enemy class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Troll'
        self.description = 'Troll armed with a War-Axe'
        self.armor = 25
        self.hp = 55
        self.atk = 6

class Dragon(Enemy):
    """Dragon boss class"""
    def __init__(self):
        Enemy.__init__(self)
        self.generic = 'Dragon'
        self.description = 'Green Dragon with thick scales'
        self.armor = 50
        self.hp = 150
        self.atk = 12

class Player(object):
    def __init__(self):
        self.defending = False
        self.isalive = True
        self.hp = 100
        self.armor = 20
        self.evasion = 1
        #self.inventory = {'Weapons':[],'Artefacts':[],'Scrolls':[]}
        #self.weapon = ('Shortsword', 5)
        self.potions = 3
        self.AP = 10

    def is_attacked(self,dmg,special):
        if self.defending:
            self.evasion += self.evasion
            self.armor += self.armor
        if dmg <= 0:
            #counts as a miss or absorption
            return (0, 'miss')
        if special == False:
            full_dmg = dmg - ((self.evasion + self.armor)/2)
            if full_dmg <= 0:
                return (0,'absorb')
                #counts as a full absorption
            else :
                self.hp -= full_dmg
                return (full_dmg, 'hit') 
                #successful hit
        if special == True:
            full_dmg = dmg - self.evasion
            if full_dmg <= 0:
                return (0,'evade')
            #counts as an evasion
            else:
                self.hp -= full_dmg
                return (full_dmg, 'hits')
                #didn't evade, full hit no armor count
        if self.defending:
            self.evasion -= self.evasion
            self.armor -= self.armor
            self.defending = False
    def heal(self, amount):
        self.hp += amount
        return amount

