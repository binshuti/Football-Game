"""
Controller File responsible for
obtaining input from the user
"""

# pylint: disable
import pygame


class FieldController:
    """
    Create a class that holds
    the level as an input from
    the user
    Attributes:
        current_level: string
        representing the
        level the user inputted
    """

    def __init__(self):
        self.current_level = ""

    def get_level(self):
        """
        Returns the user inputted
        level as an integer
        Args: None
        Returns:
            current_level: integer of
        the user inputted value for level
        """
        try:
            current_level = input("Please enter a starting level from 1 - 5: ")
            # current_level = int(current_level)
            if int(current_level) < 1 or int(current_level) > 5:
                raise ValueError
            if isinstance(int(current_level), int) is False:
                raise ValueError

            return int(current_level)
        except (IndexError, ValueError):
            print(f"Error: {current_level} is not a valid level.")
            current_level = int(self.get_level())
            return current_level


def get_ball_move():
    """
    Returns the key the user pressed
    Arg: None
    Returns:
        user_input: ScancodeWrapper
        of the key the user pressed
    """
    user_input = pygame.key.get_pressed()
    return user_input
