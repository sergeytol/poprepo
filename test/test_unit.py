import unittest

from poprepo.service import is_popular, calc_score


class MainTest(unittest.TestCase):
    """"""
    def test_calc_score(self):
        try:
            calc_score()
        except TypeError as exc:
            assert (
                str(exc) == "calc_score() missing 2 required positional arguments: "
                "'stargazers_count' and 'forks_count'"
            )

        try:
            calc_score(500, "1")
        except TypeError as exc:
            assert str(exc) == "unsupported operand type(s) for +: 'int' and 'str'"

        try:
            calc_score("500", 1)
        except TypeError as exc:
            assert str(exc) == 'can only concatenate str (not "int") to str'

        result = calc_score(500, 1)
        assert isinstance(result, int)
        assert result == 502

    def test_is_popular(self):
        try:
            is_popular()
        except TypeError as exc:
            assert (
                str(exc) == "is_popular() missing 1 required positional argument: 'score'"
            )

        result = is_popular(499)
        assert isinstance(result, bool)
        assert result is False

        result = is_popular(500)
        assert isinstance(result, bool)
        assert result is True
