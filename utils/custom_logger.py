"""
Module contains a Logger that can be extended to log elsewhere
"""


class CustomLogger:
    """
    A custom logger class that implements error(), info(), warning(), success() methods
    """

    def error(self, text):
        """
        Logs errors
        """
        print(text)

    def info(self, text):
        """
        Logs general information
        """
        print(text)

    def warning(self, text):
        """
        Logs warnings
        """
        print(text)

    def success(self, text):
        """
        Logs success messages
        """
        print(text)
