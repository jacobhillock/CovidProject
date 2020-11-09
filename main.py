from api_requests import counties_specific
from os.path import isfile, join
from json import loads, dumps
from time import sleep
from requests import get as req_get
import pandas as pd


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

def proc_ts (data):
    frame = pd.DataFrame(
        columns=["date", "fips", "cases", "deaths", "positiveTests", "negativeTests", "newCases"]
    )
    for loc in data:
        fips = loc.get("fips")
        for point in loc["actualsTimeseries"]:
            frame = frame.append({
                "date"          : point.get("date",          None),
                "fips"          : fips,
                "cases"         : point.get("cases",         None),
                "deaths"        : point.get("deaths",        None),
                "positiveTests" : point.get("positiveTests", None),
                "negativeTests" : point.get("negativeTests", None),
                "newCases"      : point.get("newCases",      None)
                },
                ignore_index=True
            )
    frame = frame.fillna(0)
    # print(frame)
    return frame
    

def write_ts (data, file_name):
    frame = proc_ts(data)
    
    open(file_name, 'w+').write(frame.to_csv())

def write (data, file_name):
    # states = {}
    # for point in data:
    #     hash_val = f"{point['state']}_{point['lastUpdatedDate']}"
    #     states[hash_val] = {
    #         "population": point.get("population", None),
    #         "metrics":    point.get("metrics", None),
    #         "riskLevels": point.get("riskLevels", None),
    #         "actuals":    point.get("actuals", None)
    #     }
    open(file_name, 'w+').write(dumps(data, indent='\t'))



def main():
    if not isfile('state_list.txt'):
        download_states_codes()
    # data = us_states()
    data = counties_specific(use_ts=True)
    # print(data)
    write(data, 'temp.json')
    write_ts(data, 'wash.csv')


if __name__ == '__main__':
    main()