from time import sleep, time
import stomp
import xmltodict


class MyListener(stomp.ConnectionListener):
    def __init__(self, listener):
        self.listener = listener

    def on_error(self, headers, message):
        print(f'ERROR "{message}" ' * 5)

    def on_message(self, headers, message):
        message = xmltodict(message)
        for key,value in headers.iteritems():
            message[key]=value
            print('header: key %s , value %s' %(key, value))
        listener(message)


def connect_to_api(api_key='', client_id='', listener='', port=61613):
    conn = stomp.Connection12(
        host_and_ports=[
            ('api.bmreports.com', port)], use_ssl=True)
    conn.start()
    conn.connect(api_key, api_key, True)
    conn.subscribe(
        destination='/topic/bmrsTopic',
        ack='auto',
        id=client_id)
    conn.set_listener('', MyListener())
    while conn.is_connected():
        sleep(1)

