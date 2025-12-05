"""
Unit tests for public methods in
soccer_game_field_model file

"""

from soccer_game_field_model import Level
from soccer_game_field_model import Defender
from soccer_game_field_model import defend_move
from soccer_game_field_model import make_def_dict
from soccer_game_field_model import initialize_def
from soccer_game_field_model import level_images
from soccer_game_field_model import make_level_rect


def test_create_numdef_one():
    """
    Test that level one has exactly
    one defender
    """
    tester_level = Level(1)
    assert tester_level.create_numdef() == 1


def test_numdef_same_level():
    """
    Test that upper bound, level 5, creates
    number of defenders equal to the level number
    5
    """
    new_test_level = Level(5)
    assert new_test_level.create_numdef() == 5


def test_newvel_increase():
    """
    Test that when level increases
    the velocity change is positive
    """
    first_level = Level(3)
    f_level_vel = first_level.create_newvel()
    second_level = Level(4)
    s_level_vel = second_level.create_newvel()
    assert (s_level_vel - f_level_vel) >= 0


def test_newvel_fifteen():
    """
    Test that when level changes by one
    velocity changes by 4 pixels
    """
    one_level = Level(3)
    o_level_vel = one_level.create_newvel()
    two_level = Level(4)
    t_level_vel = two_level.create_newvel()
    assert (t_level_vel - o_level_vel) == 4


def test_newvel_double():
    """
    Test that when game skips one level,
    velocity changes by 8
    """
    init_level = Level(2)
    i_level_vel = init_level.create_newvel()
    double_level = Level(4)
    d_level_vel = double_level.create_newvel()
    assert (d_level_vel - i_level_vel) == 8


def test_def_bounds():
    """
    Test that if the y-position of a
    certain defender number is off the
    screen, the y-position is not
    returned
    """
    tester_def = Defender(6)
    tester_y_pos = tester_def.find_y_pos(6)
    assert tester_y_pos is None


def test_def_distance():
    """
    Test that the distance between two
    defenders created is 150 pixels
    """
    one_def = Defender(3)
    o_def_pos = one_def.find_y_pos(3)
    two_def = Defender(4)
    t_def_pos = two_def.find_y_pos(4)
    assert (t_def_pos - o_def_pos) == 150


def test_def_one():
    """
    Test that first defender has a
    y-position of 175
    """
    first_def = Defender(1)
    f_defender = first_def.find_y_pos(1)
    assert f_defender == 175


def test_defend_move():
    """
    Test that when given an x-position
    that is off the screen (outside the
    bounds of the screen),
    an in-screen value for x-position
    is returned
    """
    new_pos = defend_move(-100)
    assert 900 >= new_pos >= 200


def test_make_def_dict_length():
    """
    Test that the number of keys in
    defender dictionary matches the
    total number of defenders inputted
    """
    mock_def_dict = make_def_dict(4)
    assert len(mock_def_dict) == 4


def test_make_def_dict_none():
    """
    Test that when given 0
    defenders to make, the dictionary
    is empty
    """
    zero_def_dict = make_def_dict(0)
    assert len(zero_def_dict) == 0


def test_make_def_dict_one_value():
    """
    Test that the value of the
    defender dictionary key is one
    integer representing the
    y-position of that defender
    """
    one_def_dict = make_def_dict(1)
    one_value = one_def_dict[1]
    assert one_value == 175


def test_initialize_def_length():
    """
    Test that the length of the
    initialized defender dictionary
    is the same length as the defender
    dictionary; same number of defenders
    """
    reg_dict = make_def_dict(3)
    initial_reg_dict = initialize_def(reg_dict)
    assert len(initial_reg_dict) == len(reg_dict)


def test_initialize_dict_value_length():
    """
    Test that values of a key in the
    initialized dictionary is a list of
    three elements.
    """
    reg_dict = make_def_dict(3)
    new_initial_dict = initialize_def(reg_dict)
    defender_two = new_initial_dict[2]
    assert len(defender_two) == 3


def test_level_image_length():
    """
    Test that when called, the
    dictionary length is always
    six
    """
    level_dict = level_images()
    assert len(level_dict) == 6


def test_make_level_rect_length():
    """
    Test that the value of a
    key in the image dictionary
    is a list with the length of
    two
    """
    level_dict_im = level_images()
    rect_level = make_level_rect(3, level_dict_im)
    assert len(rect_level) == 2
