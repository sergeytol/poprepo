import unittest

from app.main import error_response, is_popular


class MainTest(unittest.TestCase):
    """"""
    def test_error_response(self):
        try:
            error_response()
        except TypeError as exc:
            assert str(exc) == "error_response() missing 1 required positional argument: 'message'"

        result = error_response(message="test")
        assert isinstance(result, dict)
        assert "detail" in result
        assert result["detail"] == "test"

    def test_error_response(self):
        try:
            is_popular()
        except TypeError as exc:
            assert str(exc) == "is_popular() missing 2 required positional arguments: " \
                               "'stargazers_count' and 'forks_count'"

        try:
            is_popular(500, "1")
        except TypeError as exc:
            assert str(exc) == "unsupported operand type(s) for +: 'int' and 'str'"

        try:
            is_popular("500", 1)
        except TypeError as exc:
            assert str(exc) == 'can only concatenate str (not "int") to str'

        result = is_popular(500, 1)
        assert isinstance(result, bool)
        assert result is True
