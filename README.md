# bmrs-json-api

[![PyPI version](https://badge.fury.io/py/bmrs.svg)](https://badge.fury.io/py/bmrs)
[![Downloads](https://pepy.tech/badge/bmrs)](https://pepy.tech/project/bmrs)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


For returning BMRS API data in json format, it fetches data and auto converts it to a dictionary object, easier for data processing.

## Dependecies

1. [stomp.py](https://github.com/jasonrbriggs/stomp.py)
2. [xmltodict](https://pypi.org/project/xmltodict/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bmrs-json-api.

```bash
pip install bmrs
```

## Example Usage

```python
'''This could be your example consumer file from which you will receive and process the API responses'''
from bmrs import connect_to_api


def on_message(json_response):
    '''Receive a JSON response and do stuff with it'''
    print(list(json_response.keys()))
    # print(json_response)


# If client_id is not specified, the computer hostname is automatically picked
# but that means only one connection per computer (name)
bmrs.connect_to_api(
    api_key = 'YOUR API KEY HERE',
    client_id = 'YOUR_CLIENT_ID_HERE',
    listener=on_message # mention the name of your main data receiving function as a parameter
)     
```

## Known bugs
[Dealing with disconnects doesn't recyle threads](https://github.com/jasonrbriggs/stomp.py/issues/151)


## Getting API key

- Register on the [ELEXON Portal](https://www.elexonportal.co.uk/).
- The API Key is the `Scripting Key` under `Basics` on your profile.

## Imposter syndrome disclaimer: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not ready to be an open source contributor; that your skills aren't nearly good enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at all, you can contribute code to open source. Contributing to open source projects is a fantastic way to advance one's coding skills. Writing perfect code isn't the measure of a good developer (that would disqualify all of us!); it's trying to create something, making mistakes, and learning from those mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can help out by writing documentation, tests, or even giving feedback about the project (and yes - that includes giving feedback about the contribution process). Some of these contributions may be the most valuable to the project as a whole, because you're coming to the project with fresh eyes, so you can see the errors and assumptions that seasoned contributors have glossed over.

## Contributing

For major changes, please open an issue first to discuss what you would like to contribute.
Please make sure to update tests as appropriate.
Also, add your name to the readme in the Contributors section (below).

## Contributors and acknowledgment

1. Edison Abahurire [simicode](https://github.com/SimiCode) - BDFL
2. Elijah Rwothoromo [rwothoromo](https://github.com/Rwothoromo) - For big updates to documentation
3. Martin Ahindura [Tinitto](https://github.com/Tinitto) - For adding the durable connection method

## License

[MIT](https://choosealicense.com/licenses/mit/)

Packaged with: [Flit](https://buildmedia.readthedocs.org/media/pdf/flit/latest/flit.pdf)
