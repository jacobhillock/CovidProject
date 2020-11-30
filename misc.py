from requests import get as req_get
from json import loads, dumps


def download_states_codes():
    url = "https://raw.githubusercontent.com/michaelficarra/us-states/master/index.json"
    with open("state_list.txt", "w+") as file:
        r = req_get(url)
        data = loads(r.text)
        codes = list(data.keys())
        military_keys = ['AA', 'AE', 'AP']
        territory_keys = ['AS', 'DC', 'FM', 'GU', 'MH', 'MP', 'PR', 'PW', 'VI']
        state_keys = [ key for key in codes if key not in military_keys+territory_keys ]
        organized_data = {
            "military_keys": military_keys,
            "territory_keys": territory_keys,
            "state_keys": state_keys
        }
        file.write(dumps(organized_data, indent='\t'))

def load_state_codes():
    with open('state_list.txt') as file:
        data = loads(file.read())
    return data['state_keys']