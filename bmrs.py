"""This package enables you receive BMRS data as json instead of the default XML"""
__version__ = "2021.07.01"
# this new verison sleeps for 30 seconds in case of any error/exception and kees retrying infinitely

from time import sleep, time
import stomp
import xmltodict
import json
import socket


def connect_and_subscribe(conn, api_key, client_id):
    acknowledgement_mode = "client-individual"
    headers = {
        "activemq.subcriptionName": client_id,
        "activemq.subscriptionName": client_id,
    }
    conn.connect(api_key, api_key, wait=True, headers={"client-id": client_id})
    conn.subscribe(
        destination="/topic/bmrsTopic",
        ack=acknowledgement_mode,
        id=client_id,
        headers=headers,
    )


def get_hostname():
    """Returns hostname of  to be used as client id for connection"""
    return socket.getfqdn()


class MyListener(stomp.ConnectionListener):
    """This is a listener class that listens for new messages using the STOMP protocol"""

    def __init__(self, conn, listener, api_key, client_id):
        self.listener = listener
        self.conn = conn
        self.api_key = api_key
        self.client_id = client_id
        self.acknowledgement_mode = "client-individual"

    def on_error(self, headers, message):
        print(f'on_error! : "{headers}"')
        self.reconnect()

    def on_message(self, headers, message):
        message = xmltodict.parse(message)
        for key, value in headers.items():
            message[key] = value
            # print('header: key %s , value %s' %(key, value))
        message = json.loads(json.dumps(message))
        self.listener(message)
        # acknowledge message
        ack = headers["ack"]
        self.conn.ack(ack)

    def on_disconnected(self):
        print("disconnected")
        self.conn.disconnect()
        self.reconnect()

    def on_heartbeat_timeout(self):
        print("heartbeat_timeout")
        self.reconnect()

    def reconnect(self):
        print("attemptig reconnect")
        connect_and_subscribe(self.conn, self.api_key, self.client_id)


def connect_to_api(api_key, listener, client_id="", port=61613):
    """ Connect to the BMRS API. This function will get the XML data and convert it to JSON instantaneously!
    `api_key`:str is your API key that can be got by following [Guide](https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/).
    `client_id`:str is your Client ID that can be got together with the APIkey from the above step.
    `listener`:func is your custom function that receives & handles messages returned from the API. See a sample of this in our sample file sample_client.py on github.
    """
    # generate client id if not supplied
    if not client_id:
        client_id = get_hostname()
    print('client_id', client_id)
    # connect to API using stomp
    conn = stomp.Connection12(
        host_and_ports=[("api.bmreports.com", port)], use_ssl=True
    )
    conn.set_listener("", MyListener(conn, listener, api_key, client_id))

    while True:
        ## parts that can be moved to inside the loop
        connect_and_subscribe(conn, api_key, client_id)
        # check for new messages after every x seconds
        while conn.is_connected():
            sleep(1)
        conn.disconnect()
