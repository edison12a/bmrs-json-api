"""This package enables you receive BMRS data as json instead of the default XML"""
__version__ = '1.2.6'


from time import sleep, time
import stomp
import xmltodict
import json


def connect_and_subscribe(conn, api_key, client_id):
    conn.start()
    conn.connect(api_key, api_key, wait=True, headers={'client-id': client_id})
    conn.subscribe(
        destination='/topic/bmrsTopic',
        ack='auto',
        id=client_id,
        headers={'subscription-type': 'MULTICAST',
                 'durable-subscription-name': 'someRandomValue'}
    )


class MyListener(stomp.ConnectionListener):
    '''This is a listener class that listens for new messages using the STOMP protocol'''

    def __init__(self, conn, listener, api_key, client_id):
        self.listener = listener
        self.conn = conn
        self.api_key = api_key
        self.client_id = client_id

    def on_error(self, headers, message):
        print(f'ERROR! : "{message}"')
        connect_and_subscribe(self.conn, self.api_key, self.client_id)

    def on_message(self, headers, message):
        message = xmltodict.parse(message)
        for key, value in headers.items():
            message[key] = value
            # print('header: key %s , value %s' %(key, value))
        message = json.loads(json.dumps(message))
        self.listener(message)

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn, self.api_key, self.client_id)

    def on_heartbeat_timeout(self):
        print("Oh damn - the heartbeats have timed out.... Lets try re-connecting 30 times")
        for n in range(1, 31):
            try:
                print("Reconnecting: Attempt: ", n)
                connect_and_subscribe(self.conn, self.api_key, self.client_id)
                break
            except stomp.exception.ConnectFailedException:
                # Oh, still can't reconnect
                print("Reconnect attempt failed")
                time.sleep(1)

    def on_heartbeat_timeout(self):
        """
        Called by the STOMP connection when a heartbeat message has not been
        received beyond the specified period.
        """
        print('heartbeat timed out')
        connect_and_subscribe(self.conn, self.api_key, self.client_id)


def connect_to_api(api_key='', client_id='', listener='', port=61613):
    ''' Connect to the BMRS API. This function will get the XML data and convert it to JSON instantaneously!

    `api_key`: is your API key that can be got by following [Guide](https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/).
    `client_id`: is your Client ID that can be got together with the APIkey from the above step.
    `listener`: is your custom function that receives & handles messages returned from the API. See a sample of this in our sample file sample_client.py on github.
    '''
    # connect to API using stomp
    conn = stomp.Connection12(
        host_and_ports=[
            ('api.bmreports.com', port)], use_ssl=True)
    conn.set_listener('', MyListener(conn, listener, api_key, client_id))
    connect_and_subscribe(conn, api_key, client_id)
    # check for new messages after every x seconds
    while conn.is_connected():
        sleep(1)
