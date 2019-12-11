"""
Script to test out the durability of the durable stomp connection
This is how to test:
    - Run the script with `python test_run.py`
    - Stop the script for at least 30 minutes. To do this, hit CTRL-C
    - Run the script again with `python test_run.py`
    - Look closely at the dates in the messages. You will find that
      those missed in the last 30 minutes were immediately sent on reconnecting
"""

from bmrs import connect_to_api

if __name__ == "__main__":
    # You could specify the message types to listen to. By default, all are received
    # message_types = ['BOALF', 'FUELINST', 'B1510', 'B1520', 'B1530', 'B1540']

    # You could create your own logger
    #custom_logger = CustomLogger()

    def bmrs_json_message_processor(message):
        print(message)

    print('Starting!')
    # If client_id is not specified, the computer hostname is automatically picked
    # but that means only one connection per computer (name)
    connect_to_api(api_key='YOUR API KEY HERE', client_id='YOUR_CLIENT_ID_HERE_CREATED_BY_YOU',
                   listener=bmrs_json_message_processor)
