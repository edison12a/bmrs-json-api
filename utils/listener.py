"""
Module Contains the Stomp Listener
"""
import stomp
import xmltodict


class StompListener(stomp.ConnectionListener):
    """
    Class to handle the connection to the messaging server via STOMP protocol
    """

    def __init__(self, callback, disconnection_handler, xml_to_json=True, *args, **kwargs):
        self.__callback = callback
        self.__disconnection_handler = disconnection_handler
        self.__xml_to_json = xml_to_json

    def on_error(self, headers, message):
        """
        Handler for when an error occurs
        """
        self.__callback(error=message, message_dict=None)

    def on_message(self, headers, message):
        """
        Handler for when a message comes in
        """
        parsed_message = xmltodict.parse(
            message) if self.__xml_to_json else message
        self.__callback(
            error=None, message_dict=parsed_message, headers=headers)

    def on_disconnected(self):
        """
        Handler for when the client is disconnected
        """
        self.__disconnection_handler('disconnected')

    def on_heartbeat_timeout(self):
        """
        Handler for when heartbeat does not come in on time
        """
        self.__disconnection_handler('heartbeat timed out')
