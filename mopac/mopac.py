#!/usr/bin/env python3

import argparse
import datetime
import json
import random
import sys
import time

import pytz
import requests


USER_AGENTS = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
               'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4147.71 Mobile/15E148 Safari/604.1',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40']

def printd(data):
    '''Print a dictionary in a nice human-readable way.'''
    print(json.dumps(data, separators=(',', ': '), sort_keys=True, indent=4))

def print_mopac(data):
    '''Print a dictionary of mopac price data'''
    print('{date}-{time} {day_of_week}'.format(**data))
    data.pop('date', None)
    data.pop('day_of_week', None)
    data.pop('time', None)
    for k in sorted(data):
        print("%21s: %s" % (k, data[k]))

def get_mopac_data(when):
    '''Get raw data from Mopac website. Should be in JSON format.'''
    url = 'https://mopac-fare.mroms.us/HistoricalFare/ViewHistoricalFare'
    headers = {
        'Origin': 'https://www.mobilityauthority.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': random.choice(USER_AGENTS),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.mobilityauthority.com/pay-your-toll/current-mopac-rates',
        'Connection': 'keep-alive'
        }
    payload = when.strftime('starttime=%m%%2F%d%%2F%Y+%H%%3A%M')
    r = requests.post(url, headers=headers, data=payload)
    try:
        return r.json()
    except:
        print(r.status_code)
        print(r.headers)
        print(r.text)
        return {}

def parse_mopac_data(data):
    '''Grab just the data we care about.'''
    result = {}
    for e in data:
        name = e.get('tollingPointName').replace('LP1X ','')
        result[name] = e.get('tripRate')
    return result

def append_csv(data, name='result.csv'):
    if not name:
        return None
    keys = ['date','time','day_of_week',
            'NB: 2222 to Parmer','NB: CVZ to 183','NB: CVZ to Parmer',
            'SB: 2222 to 5th/CVZ','SB: Parmer to 2222','SB: Parmer to 5th/CVZ']
    with open(name, "a") as f:
        line = []
        for k in keys:
            line.append(str(data[k]))
        f.write(",".join(line) + "\n")
    print("Wrote to %s" % name)
    return None

def main():
    parser = argparse.ArgumentParser(description='Get current Mopac express lane prices')
    parser.add_argument("-o", "--out", help="Append data to csv file", type=str, default="")
    args = parser.parse_args()
    # Get current Central Time
    now = datetime.datetime.now(pytz.timezone('America/Chicago'))
    raw_data = get_mopac_data(now)
    if not raw_data:
        print("Didn't get json data, quitting...")
        sys.exit(1)
    nice_data= parse_mopac_data(raw_data)
    # Add useful information
    nice_data['date'] = now.strftime("%Y-%m-%d")
    nice_data['time'] = now.strftime("%H:%M")
    nice_data['day_of_week'] = now.strftime("%a")
    append_csv(nice_data, args.out)
    #printd(nice_data)
    print_mopac(nice_data)

if __name__ == '__main__':
    main()
