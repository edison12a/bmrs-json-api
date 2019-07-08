'''This could be your example consumer file from which you will receive and process the API responses'''
import bmrs


def on_message(json_response):
    '''Receive a JSON reponse and do stuff with it'''
    print(list(json_response.keys()))
    # print(json_response)

# connect to the bmrs API using your credentials
bmrs.connect_to_api(
        api_key = 'kslch6aa8p97wyn',
        client_id = 89898989,
        listener=on_message
    )
