"""This package that enables you fetch BMRS data as json instead of XML"""
__version__ = '1.2.1'


from time import sleep, time
import stomp
import xmltodict
import json


class MyListener(stomp.ConnectionListener):
    '''This is a listener class that listens for new messages using the STOMP protocol'''
    def __init__(self, listener):
        self.listener = listener

    def on_error(self, headers, message):
        print(f'ERROR! : "{message}"')

    def on_message(self, headers, message):
        message = xmltodict.parse(message)
        for key,value in headers.items():
            message[key]=value
            # print('header: key %s , value %s' %(key, value))
        message = json.loads(json.dumps(message))
        self.listener(message)


def connect_to_api(api_key='', client_id='', listener='', port=61613):
    ''' Connect to the BMRS API. This function will get the XML data and convert it to JSON instantaneoudly!

    `api_key`: is your API key that can be got by following [Guide](https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/).
    `client_id`: is your Client ID that can be got together with the APIkey from the above step.
    `listener`: is your custom function that recieves & handles messages returned from the API. See a sample of this in our sample file sample_client.py on github.
    '''
    # connect to API using stomp
    conn = stomp.Connection12(
        host_and_ports=[
            ('api.bmreports.com', port)], use_ssl=True)
    conn.start()
    conn.connect(api_key, api_key, True)
    conn.subscribe(
        destination='/topic/bmrsTopic',
        ack='auto',
        id=client_id)
    # add a listener instance and initialize it with the user's supplied custom listener
    conn.set_listener('', MyListener(listener))

    # check for new meessages after every x seconds
    while conn.is_connected():
        sleep(1)
