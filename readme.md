# Introduction #

This program is a simple tank game that runs on python. The initial intentions with this game was to build a tank game similiar to wii tanks that also offered multiplayer. Graphics are rendered using pygames.


# Features #

- [ ] Multiplayer
- [ ] Collision Detection
- [ ] Bullets can bounce of walls
- [ ] Map Builder
- [ ] Decorative Blocks
- [ ] Artificial Intelligence


# Designing your own level #

This game has levels stored as json files in /maps folder.
A level consist of 4 things that must be specified in the json file.
- The level name.
- The dimensions of the level.
- The level map.
- The tank orientations.

Look at default.json for an example of what a map looks like.

## Legend ##
Name | Key | Information
--- | --- | ---
Wall Floor | w | Blocks tanks going through. Bullets bounce off walls a maximum of 3 times.
Wall | W | A different type of wall.
Air | a | Allows tanks and bullets to pass through.
Player Tank | p | The tank the player will be able to control.

When designing a map, there are a few rules to consider and a guidelines to follow to ensure consistency between all levels.

### Rules ###
The following rules must be followed during the construction of the map. Failure to do so will result in the game crashing or acting extremely buggy.

1. A wall structure must consist of two tiles. 
    * Wall floor.
    * Wall.

    Every wall floor tile must be on top of any of the two tiles mentioned above.

2. A boundary of walls must exist that enclose the space the tanks can move in.

3. A level must consist of a minimum of 2 tanks. For a multiplayer level, only a maxium of 4 tanks can be placed in a level.

### Guidelines ###
1. A wall structure that isn't the boundary should not contain a stacked 'wall' tile.

2. A wall boundary should have two wall tiles stacked on top of each other and a wall tile surrounding the border. 
### Credit ###