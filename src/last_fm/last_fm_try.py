# Application name law-school-copyright
# API key a791ebdea3b7ba81ff4bd70cff591244
# Shared secret b3efda8cad1b0041281caffe3430a0c9
# Registered to law-school-copy
import requests
import json
import pandas as pd


def load_data_from_excel(csv_input):
    request_query = []
    req = {}
    data = pd.read_excel(r''+csv_input)
    df = pd.DataFrame(data, columns=['Title', 'Artist'])
    # print(df)
    for index, row in df.iterrows():
        req['method'] = 'track.getInfo'
        req['autocorrect'] = 1
        req['track'] = row['Title'][1:-1]
        req['artist'] = row['Artist']
        request_query.append(req)
        req = {}
    return request_query


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def count_listeners(data_json):
    # print(jprint(data_json))
    out_p = {}
    if 'track' in data_json:
        count = data_json['track']['playcount']
        listener = data_json['track']['listeners']
        duration = convert(int(data_json['track']['duration']))
        # for each in data_json['track']['playcount']['track']:
        #     count = count + int(each['listeners'])
        #     # print(each['listeners'], each['name'])
        print('count is', count, "listener is", listener, 'duration is', duration)
    else:
        print("not found")


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
    print(payload['artist'], payload['track'])
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
    'method': 'track.getInfo',
    'autocorrect': 1,
    'track':  "The End of the World",
    'artist': 'Skeeter Davis'}
dsa = {
    # 'method': 'artist.getTopTags',
    # 'artist':  'The Beach Boys'
    'method': 'track.getInfo',
    'autocorrect': 1,
    'track':  "Surfin\' U.S.A.",
    'artist': 'The Beach Boys'}
# intake is a dict

aasd = [asd, dsa]
for each in aasd:
    print(each)
    r = lastfm_get(each)

request_query = load_data_from_excel('Year-end Hot 100 1963-1964.xlsx')
for each in request_query:
    print(each)
    r = lastfm_get(each)

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

