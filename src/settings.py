# Uses singleton design pattern
import configparser
from lib import utils

class Settings:


    _instance = None
    def __init__(self):
        path = utils.resource_path('settings.ini')
        if Settings._instance is not None:
            self = Settings._instance
        else:
            Settings._instance = self
            self._config = configparser.ConfigParser()
            try: 
                self._config.read(path)
            except: 
                self.generate_settings()
            self._actions = {
                'accelerate': 'w',
                'decelerate': 's',
                'turn_left': 'a',
                'turn_right': 'd',
                'nozzle_left': 'j',
                'nozzle_right': 'i',
                'shoot': 'space'
            }
            self._actions = ['accelerate', 'decelerate', 'turn_left', 'turn_right', 'shoot',
                             'nozzle_left', 'nozzle_right']
        for key, value in self._config['key_bindings'].items():
            if value == 'space':
                self._config['key_bindings'][key] = ' '

    def generate_settings(self):
        path = utils.resource_path('settings.ini')
        print("[WARNING] Found corrupted or missing 'settings.ini'. Generating new file.")
        self._config['settings'] = {
            'max_fps': '60',
            'resolution': '500x600'
        }
        self._config['key_bindings']  = self._actions
        with utils.open_file('settings.ini', 'w') as config_file:
            self._config.write(config_file)
        self._config.read(path)
    def get_ord(self):
        try:
            keys = self._config['key_bindings']
            key_ords = []
            for action in self._actions:
                key_ords.append(ord(keys[action]))
        except configparser.Error:
            self.generate_settings()
            return get_ord()
        return key_ords