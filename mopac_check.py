#!/usr/bin/env python3

import argparse
import datetime
import json
import random
import sys
import time

import pytz
import requests


def printd(data):
    '''Print a dictionary in a nice human-readable way.'''
    print(json.dumps(data, separators=(',', ': '), sort_keys=True, indent=4))

def get_mopac_data(when):
    '''Get raw data from Mopac website. Should be in JSON format.'''
    url = 'https://mopac-fare.mroms.us/HistoricalFare/ViewHistoricalFare'
    USER_AGENTS = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
                   'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C202 Safari/604.1',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko']
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

def randsleep(seconds=0):
    '''Use this optionally to "fuzzy" when this runs.'''
    time.sleep(random.randint(0,seconds))
    return None

def append_csv(data, name='result.csv'):
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sec", help="Randomly sleep between 0 and this many seconds", type=int, default=0)
    parser.add_argument("-o", "--out", help="Append data to this csv file", type=str, default="result.csv")
    args = parser.parse_args()
    randsleep(args.sec)
    now = datetime.datetime.now(pytz.timezone('America/Chicago'))
    raw_data = get_mopac_data(now)
    if not raw_data:
        print("Didn't get json data, quitting...")
        sys.exit(1)
    nice_data= parse_mopac_data(raw_data)
    # Add information
    nice_data['date'] = now.strftime("%Y-%m-%d")
    nice_data['time'] = now.strftime("%H:%M")
    nice_data['day_of_week'] = now.strftime("%a")
    append_csv(nice_data, args.out)
    printd(nice_data)
