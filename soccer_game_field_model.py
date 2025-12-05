"""
File contains methods that change the state
of instances and variables during the
soccer game
"""

import random
import pygame


class Level:
    """
    Create a level that generates
    the number of defenders on that level
    and the velocity of the ball on
    that level
    Attributes:
        numdef: The number of defenders
        vel: The number of pixels moved
        per keyboard click
    """

    def __init__(self, level):
        self.level = int(level)
        self.numdef = 0
        self.vel = 10

    def create_numdef(self):
        """
        Return the number of defenders
        created based on the level
        Args: No arguments
        Return:
            numdef: number of
            defenders as integers
        """
        self.numdef = self.level
        return self.numdef

    def create_newvel(self):
        """
        Return number of pixels based
        on the current level
        Args: No arguments
        Return:
            vel: Integer representing
            the number of pixels the
            ball will move per click
        """
        self.vel = (4 * self.level) + 20
        return self.vel


class Defender:
    """
    Defender instance created and used
    for all levels and to find y-position
    of each new defender

    Attributes:
        def_y_pos: The defender y-position as
        an integer
    """

    def __init__(self, def_rank):
        self.def_y_pos = self.find_y_pos(def_rank)

    def find_y_pos(self, def_rank):
        """
        Return the y-position of a
        defender given what number
        defender it is
        Args:
            def_rank: integer representing
            the number defender the y-position
            is for
        Return:
            def_y_pos: integer representing
            y-position of the defender on screen
        """
        self.def_y_pos = 25 + (def_rank * 150)
        if self.def_y_pos <= 900:
            return self.def_y_pos
        return None


def defend_move(current_x):
    """
    Given current position, move
    the defender a random distance away
    Args:
        current_x: An integer representing
        the current x-position of the defender
    Return:
        move_pos: An integer representing
        the new x-position of the defender
    """
    move_pos = current_x + random.randrange(-50, 50)
    if move_pos >= 950 or move_pos <= 200:
        current_x = 500
        return current_x
    return move_pos


def make_def_dict(number_def):
    """
    Given the number of defenders
    needed to make, creates a dictionary
    of defender instances with the values
    being each instance's y-position
    Args:
        number_def: The number of defenders
        to be created
    Returns:
        A dictionary with length of number_def,
        keys are an integer of which number
        defender the instance is, values are
        integer of the y-position of the defender
    """
    count = 1
    defender_dict = {}
    make = True
    while make is True:
        if count <= number_def:
            new_defender = Defender(count)
            new_y_pos = new_defender.find_y_pos(count)
            defender_dict[count] = new_y_pos
            count = count + 1
        else:
            make = False
    return defender_dict


def initialize_def(defender_dict):
    """
    Return a dictionary with each key
    being the defender number and the
    values being the defender image, the
    x-position of the defender, and
    y-position of the defender
    Args:
        defender_dict: A dictionary
        with the intantiated defenders,
        each key being an integer
        representing which defender it is,
        and the values being an integer
        for the y-position
    Returns:
        defender_pos_dict: a dictionary
        with a length of the number
        of defenders, each key being the
        number defender, and the values being a
        list of three items: the surface image
        of the defender, the x-position
        of the defender, and y-position of defender


    """
    defender_pos_dict = {}
    for i in defender_dict:
        player_pos_stat = []
        player = pygame.image.load("images/soccerplayer.png")
        player = pygame.transform.scale(player, (150, 150))

        player_rect = player.get_rect()
        player_rect = (400, defender_dict[i])
        player_rect = list(player_rect)

        player_pos_stat.append(player)
        player_pos_stat.append(player_rect[0])
        player_pos_stat.append(player_rect[1])
        defender_pos_dict[i] = player_pos_stat
    return defender_pos_dict


def ball_move(user_input, ball_rect, vel):
    """
    Given a user's keyboard presses,
    change the location of the ball
    accordingly
    Args:
        user_input: The key the user pressed
        ball_rect: A 2 element list of integers
        with the location of the ball
        vel: the number of pixels the ball
        will move
    Return: No returns
    """
    if user_input[pygame.K_LEFT]:
        ball_rect[0] -= vel
    if user_input[pygame.K_RIGHT]:
        ball_rect[0] += vel
    if user_input[pygame.K_UP]:
        ball_rect[1] -= vel
    if user_input[pygame.K_DOWN]:
        ball_rect[1] += vel


def level_images():
    """
    create a dictionary with
    the level as the key and
    it's associated graphic image
    as a surface as it's value
    Args: None
    Return: None
    """
    level_one = pygame.image.load("images/level_one.png")
    level_two = pygame.image.load("images/level_two.png")
    level_three = pygame.image.load("images/level_three.png")
    level_four = pygame.image.load("images/level_four.png")
    level_five = pygame.image.load("images/level_five.png")
    level_six = pygame.image.load("images/level_six.png")
    level_dict = {
        1: level_one,
        2: level_two,
        3: level_three,
        4: level_four,
        5: level_five,
        6: level_six,
    }
    return level_dict


def make_level_rect(level, diction):
    """
    Given the current level and the
    dictionary containing all of
    the level images, return a list
    containing the current level image
    and it's rectangular dimensions

    Args:
        level: integer representing the
        current level
        diction: dictionary with
        the level as the key and
        the values as their associated
        images
    Returns:
        List with first element being
        surface image and second element
        the rectangular dimensions of the
        image
    """
    level_image = pygame.transform.scale(diction[level], (100, 100))
    level_rect = level_image.get_rect(center=(900, 100))
    return [level_image, level_rect]
