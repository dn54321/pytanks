from src import game
import pygame
def main():
    pygame.init()
    game_system = game.Game()
    game_system.load_map('default.json')
    game_system.start()
if __name__ == '__main__':
    main()