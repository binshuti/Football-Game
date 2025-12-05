"""
Unit tests for public methods in
soccer_game_field_controller file
"""

from soccer_game_field_controller import FieldController


def test_get_level_inbounds(monkeypatch):
    """
    Test that when user inputs invalid input
    for level, the game prompts the user again
    and accepts the next valid input
    """
    field_c_instance = FieldController()
    first = True

    def mock_input(_):
        """
        pretend to be human
        """
        nonlocal first
        if first is True:
            first = False
            return 7

        return 3

    monkeypatch.setattr("builtins.input", mock_input)
    assert field_c_instance.get_level() == 3

