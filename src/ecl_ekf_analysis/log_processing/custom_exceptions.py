# /usr/bin/env/ python3
"""
custom exception handling
"""


class PreconditionError(Exception):
    """
    an exception for detecting precondition error
    """


def capture_exception(e: Exception) -> None:
    """
    global way of capturing an exception
    :param e:
    :return:
    """
    print(str(e))


def capture_message(message: str) -> None:
    """
    global way of capturing an exception
    :param e:
    :return:
    """
    print(message)
