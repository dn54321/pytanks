# Python Libraries
import configparser

# Project Libraries
import src.settings as setting

# External Libaries
import pygame

# Uses singleton design pattern

class KeyBind():
    _instance = None
    def __init__(self):
        if KeyBind._instance is None:
            self._key_bind = setting.Settings().get_ord()
            KeyBind._instance = self
        else:
            self._key_bind = KeyBind._instance._key_bind
            
    def get_keys(self):
        bitset = 0
        key_pressed = pygame.key.get_pressed()
        for i in range(len(self._key_bind)):
            action_key = self._key_bind[i]
            if key_pressed[action_key]:
                bitset += (1 << i)
        return bitset
