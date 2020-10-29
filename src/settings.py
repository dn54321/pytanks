# Uses singleton design pattern
import configparser

class Settings:


    _instance = None
    def __init__(self):
        if Settings._instance is not None:
            self = Settings._instance
        else:
            Settings._instance = self
            self._config = configparser.ConfigParser()
            try: 
                self._config.read('settings.ini')
            except: 
                self.generate_settings()
            self._actions = ['accelerate', 'decelerate', 'turn_left', 'turn_right', 'shoot']
        for key, value in self._config['key_bindings'].items():
            if value == 'space':
                self._config['key_bindings'][key] = ' '

    def generate_settings(self):
        print("[WARNING] Found corrupted or missing 'settings.ini'. Generating new file.")
        self._config['settings'] = {
            'max_fps': '60',
            'resolution': '500x600'
        }
        self._config['key_bindings']  = {
            'turn_left': 'a',
            'turn_right': 'd',
            'accelerate': 'w',
            'decelerate': 's',
            'shoot': 'space'
        }
        with open('settings.ini', 'w') as config_file:
            self._config.write(config_file)
        self._config.read('settings.ini')
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