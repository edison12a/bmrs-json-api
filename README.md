# bmrs-json-api

For returning BMRS API data in json format, it fetches data and auto converts it to a dictionary object, easier for data processing.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bmrs-json-api.

```bash
pip install bmrs
```


## Example Usage

```python
'''This could be your example consumer file from which you will receive and process the API responses'''
import bmrs


def on_message(json_response):
    '''Receive a JSON reponse and do stuff with it'''
    print(list(json_response.keys()))
    # print(json_response)

# connect to the bmrs API using your credentials
bmrs.connect_to_api(
        api_key = 'YOUR API KEY HERE',
        client_id = YOUR_CLIENT_ID_HERE,
        listener=on_message # mention the name of your main data recieving function s a parameter
    )
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to contribute.
Please make sure to update tests as appropriate.
Also, add your name to the readme in the Contributors section (below).


## Contributors and acknowledgment
1. Edison Abahurire [simicode](https://github.com/SimiCode)
2.


## License
[MIT](https://choosealicense.com/licenses/mit/)


Packaged with: [Flit](https://buildmedia.readthedocs.org/media/pdf/flit/latest/flit.pdf)
