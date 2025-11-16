# Football-Game
# Python Project Template Repository

This is the repository for my Mini Soccer Game. This interactive
game is a fun twist on fooseball, allowing the player
to weave their way between defenders to score a goal
and level up in the game.The game is structured into
three main files using M-V-C Architecture. The three files are 
soccer_game_field_model.py, soccer_game_field_controller.py,
and soccer_game_field_view.py. The game is called and run in the
main.py file. 

## How to Use

In order to play this single player game, first run the `main.py`
file. A black screen will appear as a Pygame window, minimize this window.
Then, type the level you would like to start at in the terminal when
prompted. Open the minimized Pygame window and begin playing! Use
the arrow keys to control the movement of the ball. In order to level up,
move the ball into the goal using the arrow keys. Each level places a new
defender on the field and increases the speed of the soccer ball. You lose 
and the game exist if you hit a defender. 

## Minimum Requirements

- python 
- pygame version 
- pytest

## Requirements
The requirements and project dependencies can be found in the 
`requirements.txt` file.
To install the necessary packages run:

```sh
pip install pygame
pip install pytest
```
and

```sh
pip install -r requirements.txt
```
