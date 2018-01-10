#!/usr/bin/env python3

import datetime
import json
import sys

import requests


def printd(data):
    print(json.dumps(data, separators=(',', ': '), sort_keys=True, indent=4))

def get_mopac_data(when):
    url = 'https://mopac-fare.mroms.us/HistoricalFare/ViewHistoricalFare'
    headers = {
        'Origin': 'https://www.mobilityauthority.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.mobilityauthority.com/pay-your-toll/current-mopac-rates',
        'Connection': 'keep-alive'
        }
    payload = when.strftime('starttime=%m%%2F%d%%2F%Y+%H%%3A%M')
    r = requests.post(url, headers=headers, data=payload)
    print(r.status_code)
    print(r.headers)
    if (r.status_code != 200):
        print(r.headers)
        sys.exit(1)
    print(r.text)
    return r.json()

def parse_mopac_data(data):
    result = {}
    for e in data:
        result[e.get('tollingPointName')] = e.get('tripRate')
    return result

now = datetime.datetime.now()
raw_data = get_mopac_data(now)
nice_data= parse_mopac_data(raw_data)
nice_data['date'] = now.strftime("%Y-%m-%d")
nice_data['time'] = now.strftime("%H:%M")
nice_data['day_of_week'] = now.strftime("%a")
printd(nice_data)
