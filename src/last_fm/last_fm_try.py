# Application name law-school-copyright
# API key a791ebdea3b7ba81ff4bd70cff591244
# Shared secret b3efda8cad1b0041281caffe3430a0c9
# Registered to law-school-copy
import requests
import json
import csv


def load_data(csv_input):
    with


def count_listeners(data_json):
    count = 0
    for each in data_json['results']['trackmatches']['track']:
        count = count + int(each['listeners'])
        # print(each['listeners'], each['name'])
    print('count is', count)


def lastfm_get(payload):
    API_KEY = 'a791ebdea3b7ba81ff4bd70cff591244'
    USER_AGENT = 'law-school-copyright'
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    print(payload['artist'])
    text = response.json()
    count_listeners(text)
    return response


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text


asd = {
    # 'method': 'artist.getTopTags',
    # 'artist':  'The Beach Boys'
    'method': 'track.search',
    'track':  "The End of the World",
    'artist': 'Skeeter Davis'}
dsa = {
    # 'method': 'artist.getTopTags',
    # 'artist':  'The Beach Boys'
    'method': 'track.search',
    'track':  "Surfin' U.S.A.",
    'artist': 'The Beach Boys'}
# intake is a dict
aasd = [asd, dsa]
for each in aasd:
    r = lastfm_get(each)
    # for e, v in each.items():
    #     # print(e, v)

# print(jprint(r.json()))

#
# name = text['results']['trackmatches']
# # print(name)
# count = 0
# for each in name['track']:
#     count = count + int(each['listeners'])
#     print(each['listeners'], each['name'])


# name = text['toptags']['@attr']['artist']
# print(name)
# count = 0
# for each in text['toptags']['tag']:
#     print(each)
#     count += each['count']
#

