import bmrs


def on_message(json_response):
    print(list(json_response.keys()))
    # print(json_response)

bmrs.connect_to_api(
        api_key = 'kslch6aa8p97wyn',
        client_id = 89898989,
        listener=on_message
    )
