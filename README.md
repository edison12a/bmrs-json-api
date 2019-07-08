# bmrs-json-api

For returning BMRS API data in json format, it fetches data and auto converts it to a dictionary object, easier for data processing.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bmrs-json-api.

```bash
pip install bmrs
```

## Exmaple Usage

```python
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
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
