from src import game, player
import pygame
from time import sleep

def main():
    # Pygame window setup
    pygame.init()
    pygame.display.set_caption('Pytanks')
    game_system = game.Game()
    default_player = player.Player("Player 1")
    default_player.set_colour((65,105,225))
    test_ai = player.Player("AI")
    test_ai.set_colour((255,0,0))
    game_system.add_player(default_player)
    game_system.add_player(test_ai)
    game_system.load_map('square.json')
    game_system.assign_tanks()
    game_system.start()


if __name__ == '__main__':
    if __debug__:
        welcome_message = '''
        ===============================
         =    DEBUGGER IS ENABLED    =
        ===============================

               [ O ]
                 \ \      
                  \ \  
                   \ \--'---_
                   /\ \   / ~~\_
             ./---/__|=/_/------//~~~\\
            /___________________/O   O \\
            (===(\_________(===(Oo o o O)          
             \~~~\____/     \---\Oo__o--
               ~~~~~~~       ~~~~~~~~~~

        Note: Debugger Mode is activated and may lag the game.
        Run without debugger: python -O run.py
        '''
    else:
        welcome_message = '''
        ===============================
         =         Pytanks           =
        ===============================

               [ O ]
                 \ \      
                  \ \  
                   \ \--'---_
                   /\ \   / ~~\_
             ./---/__|=/_/------//~~~\\
            /___________________/O   O \\
            (===(\_________(===(Oo o o O)          
             \~~~\____/     \---\Oo__o--
               ~~~~~~~       ~~~~~~~~~~

        dn54321         Developer
        megarcrazy      Beta Tester/helper
        '''
    
    print(welcome_message)
    main()