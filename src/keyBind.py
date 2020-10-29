# Python Libraries
import configparser

# Project Libraries
import src.settings as setting

# External Libaries
import pygame

class KeyBind():
    def __init__(self):
        self._key_bind = setting.Settings().get_ord()

    def get_keys(self):
        bitset = 0
        key_pressed = pygame.key.get_pressed()
        for i in range(len(self._key_bind)):
            action_key = self._key_bind[i]
            if key_pressed[action_key]:
                bitset += (1 << i)
        return bitset
