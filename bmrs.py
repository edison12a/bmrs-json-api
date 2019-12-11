"""This package enables you receive BMRS data as json instead of the default XML"""
__version__ = '1.2.6'


from durable_stomp_connection import DurableStompConnection, get_hostname
from utils.custom_logger import CustomLogger


def connect_to_api(api_key='', client_id=get_hostname(), listener='', port=61613, message_types=[], logger=CustomLogger()):
    ''' Connect to the BMRS API. This function will get the XML data and convert it to JSON instantaneously!

    `api_key`: is your API key that can be got by following [Guide](https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/).
    `client_id`: is your Client ID that can be got together with the APIkey from the above step.
    `listener`: is your custom function that receives & handles messages returned from the API. See a sample of this in our sample file sample_client.py on github.
    '''
    bmrs_message_listener = DurableStompConnection(
        api_key=api_key,
        client_id=client_id,
        bmrs_message_processor=listener,
        message_types=message_types,
        xml_to_json=True,
        logger=logger,
    )
    bmrs_message_listener.start()
