from requests import get as req_get
from json import loads as json_loads

base_url_states          = "https://api.covidactnow.org/v2/states{use_ts}.json?apiKey={apiKey}"
base_url_counties        = "https://api.covidactnow.org/v2/counties{use_ts}.json?apiKey={apiKey}"
base_url_specific_state  = "https://api.covidactnow.org/v2/state/{state}{use_ts}.json?apiKey={apiKey}"
base_url_specific_county = "https://api.covidactnow.org/v2/county/{fips}{use_ts}.json?apiKey={apiKey}"

def load_key():
    key = ""
    with open('.secrets/api_key') as file:
        key = file.read()
    return key

def request_data (url, use_ts, ret_str):
    url = url.replace("{apiKey}", load_key())
    url = url.replace("{use_ts}", ".timeseries" if use_ts else "")
    r = req_get(url)
    print(url)
    data = json_loads(r.text) if not ret_str else r.text
    return data

def us_states(use_ts=False, ret_str=False):
    return request_data(base_url_states, use_ts, ret_str)

def all_counties(use_ts=False, ret_str=False):
    return request_data(base_url_counties, use_ts, ret_str)

def us_state_specific(use_ts=False, state_code='MI', ret_str=False):
    url = base_url_specific_state.replace("{state}", state_code)
    return request_data(url, use_ts, ret_str)

def counties_specific(use_ts=False, fips="26161", ret_str=False):
    url = base_url_specific_county.replace("{fips}", fips)
    return request_data(url, use_ts, ret_str)