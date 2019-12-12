"""
Module to Connect to the Elexon BMRS service and return REMIT notifications among others
"""
import stomp
import time
from utils.listener import StompListener
from utils.custom_logger import CustomLogger
import socket


def get_hostname():
    """
    Returns hostname of computer
    """
    return socket.gethostname()


class DurableStompConnection:
    """
    Handles the creation of the durable STOMP connection and the processing of the data
    """

    def __init__(
        self,
        api_key,
        bmrs_message_processor,
        logger=CustomLogger(),
        client_id=get_hostname(),
        message_types=[],
        bmrs_host="api.bmreports.com",
        port=61613,
        durable=True,
        poll_interval=1,
        xml_to_json=True,
    ):
        self.__logger = logger
        self.__durable = durable
        self.__poll_interval = poll_interval
        self.__bmrs_message_processor = bmrs_message_processor
        self.__api_key = api_key
        self.__client_id = client_id
        self.__message_types = message_types
        self.__xml_to_json = xml_to_json
        self.__connection = stomp.Connection12(
            host_and_ports=[(bmrs_host, port)], use_ssl=True
        )

    def __diconnection_handler(self, message):
        self.__logger.error(f'ERROR! : "{message}"')
        self.__restart()

    def __generate_jms_type_selector_string(self):
        """
        Generates a selector string that allows all the message_types
        passed to be listened to
        """
        selector_substrings = [
            "JMSType='{}'".format(message_type) for message_type in self.__message_types
        ]
        return " OR ".join(selector_substrings)

    def __acknowledge_message(self, ack):
        """
        Sends an ACK frame to the server to acknowledge receipt
        http://jasonrbriggs.github.io/stomp.py/api.html#acks-and-nacks
        """
        self.__connection.ack(ack)

    def __process_bmrs_message(self, error, message_dict, headers={}):
        """
        Processes parsed bmrs messages
        """
        if error is not None:
            self.__logger.error("Error thrown {}".format(error))

        try:
            ack = headers["ack"]
            self.__acknowledge_message(ack)

        except KeyError as exception:
            self.__logger.error("No Message Id received")
            raise exception

        if message_dict is not None:
            self.__bmrs_message_processor(message_dict)
            self.__logger.info("NEW MESSAGE RECEIVED \n\n")

    def __restart(self):
        """
        Restarts listening for messages but must first clean up
        """
        try:
            self.disconnect()
        except stomp.exception.NotConnectedException:
            pass
        self.start()

    def disconnect(self):
        """
        Unsubscribes and Disconnects the listener from the server
        """
        self.__connection.unsubscribe(self.__client_id)
        return self.__connection.disconnect()

    def __connect(self):
        """
        Connects to the remote broker
        For durable connections:
            - parameter 'ack' = 'client-individual' for the connection
        """
        self.__connection.connect(
            self.__api_key,
            self.__api_key,
            wait=True,
            headers={"client-id": self.__client_id},
        )

    def __subscribe(self):
        """
        Creates a connection and subscription: durable by default
        https://stomp.github.io/stomp-specification-1.2.html#SUBSCRIBE
        https://activemq.apache.org/stomp
        For durable connections:
            - parameter 'ack' = 'client-individual' for the connection
            - header 'activemq.subcriptionName' of subscription = header 'client-id'
            for the connection in ActiveMQ versions prior 5.7.0
            (note: 'subcriptionName' not 'subscriptionName')
            - header 'activemq.subscriptionName' of subscription = header 'client-id'
            for the connection in ActiveMQ versions after 5.6.0
            (note: 'subscriptionName' not 'subcriptionName')
        """
        acknowledgement_mode = "client-individual" if self.__durable else "auto"
        headers = {
            "activemq.subcriptionName": self.__client_id,
            "activemq.subscriptionName": self.__client_id,
        }

        if len(self.__message_types) > 0:
            headers["selector"] = self.__generate_jms_type_selector_string()

        self.__connection.subscribe(
            destination="/topic/bmrsTopic",
            ack=acknowledgement_mode,
            id=self.__client_id,
            headers=headers,
        )

    def start(self):
        """
        Initializes the STOMP client and connects to BMRS and listens
        """
        self.__connection.set_listener(
            "",
            StompListener(
                self.__process_bmrs_message,
                disconnection_handler=self.__diconnection_handler,
                xml_to_json=self.__xml_to_json,
            ),
        )
        self.__connection.start()
        self.__connect()
        self.__subscribe()

        while self.__connection.is_connected():
            try:
                time.sleep(self.__poll_interval)
            except KeyboardInterrupt as exp:
                print(exp)
                exit(0)
