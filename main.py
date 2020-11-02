from os.path import isfile, join
from json import loads, dumps
import requests


base_url_states = "https://data.covidactnow.org/latest/us/{STATE_CODE}.OBSERVED_INTERVENTION.timeseries.json"
base_url_countries = "https://data.covidactnow.org/latest/us/counties/{COUNTRY_CODE}.OBSERVED_INTERVENTION.timeseries.json"



def main():
    if isfile('state_list.txt'):
        url = "https://raw.githubusercontent.com/michaelficarra/us-states/master/index.json"
        with open("state_list.txt", "w+") as file:
            r = requests.get(url)
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


if __name__ == '__main__':
    main()