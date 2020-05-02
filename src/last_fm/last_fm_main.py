# Application name law-school-copyright
# API key a791ebdea3b7ba81ff4bd70cff591244
# Shared secret b3efda8cad1b0041281caffe3430a0c9
# Registered to law-school-copy

# To use this, please supply a csv file and then run it
# please pip install xlrd, pandas, requests-cache
import requests
import json
import pandas as pd
import xlsxwriter


def load_data_from_excel(csv_input):
    request_query = []
    req = {}
    data = pd.read_excel(r''+csv_input)
    if 'Title' in data and 'Artist' in data:
        df = pd.DataFrame(data, columns=['Title', 'Artist'])
    else:
        df = pd.DataFrame(data, columns=['title', 'artist'])
    # print(df)
    for index, row in df.iterrows():
        req['method'] = 'track.getInfo'
        req['autocorrect'] = 1
        req['track'] = row['Title'][1:-1]
        req['artist'] = row['Artist']
        request_query.append(req)
        req = {}
    return request_query


def convert(millis):
    # millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    # hours = (millis / (1000 * 60 * 60)) % 24
    return ("%02d:%02d" % (minutes, seconds))
    # seconds = seconds % (24 * 3600)
    # hour = seconds // 3600
    # seconds %= 3600
    # minutes = seconds // 60
    # seconds %= 60
    # return "%d:%02d:%02d" % (hour, minutes, seconds)


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
        # print('count is', count, "listener is", listener, 'duration is', duration)
        out_p['playcount'] = int(count)
        out_p['listeners'] = int(listener)
        out_p['duration'] = duration
    else:
        # print("not found")
        out_p['playcount'] = -1
        out_p['listeners'] = -1
        out_p['duration'] = -1
    return out_p

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
    # print(payload['artist'], payload['track'])
    text = response.json()
    out_dict = count_listeners(text)
    return out_dict


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text


def perform_last_fm(data,progress_callback):
    df = pd.DataFrame(data, columns=['title', 'artist'])
    print(df)
    request_query = []
    req = {}
    for index, row in df.iterrows():
        req['method'] = 'track.getInfo'
        req['autocorrect'] = 1
        print('track,', row['title'])
        req['track'] = row['title'][1:-1]
        req['artist'] = row['artist']
        request_query.append(req)
        req = {}
    out_query = []
    out_dict = {}
    i=0
    for each in request_query:
        progress_callback.emit(100*int(i/df.shape[0]))
        out_dict['artist'] = each['artist']
        out_dict['track'] = each['track']
        # print(each)
        out_dict.update(lastfm_get(each))
        out_query.append(out_dict)
        out_dict = {}
        i+=1

    print(out_query)
    out_df = pd.DataFrame(out_query)
    print(out_df)
    print(out_df.dtypes)
    return out_df


def perform_last_fm_s(data, progress_callback):
    out_put = {}
    writer = pd.ExcelWriter('last_fm_output.xlsx', engine='xlsxwriter')
    for each in data:
        print(data[each])
        out_df = (perform_last_fm(data[each],progress_callback))
        out_df.to_excel(writer, sheet_name=each)
    progress_callback.emit(100)
    writer.save()

#
# asd = {
#     # 'method': 'artist.getTopTags',
#     # 'artist':  'The Beach Boys'
#     'method': 'track.getInfo',
#     'autocorrect': 1,
#     'track':  "The End of the World",
#     'artist': 'Skeeter Davis'}
# dsa = {
#     # 'method': 'artist.getTopTags',
#     # 'artist':  'The Beach Boys'
#     'method': 'track.getInfo',
#     'autocorrect': 1,
#     'track':  "Surfin\' U.S.A.",
#     'artist': 'The Beach Boys'}
# # intake is a dict
#
# aasd = [asd, dsa]
# for each in aasd:
#     print(each)
#     r = lastfm_get(each)
if __name__ == "__main__":
    data = pd.read_excel(r'Year-end Hot 100 1963-1964.xlsx', sheet_name=None)
    # for each in data:
    #     print(data[each])
    perform_last_fm_s(data, 'aaa')
    # perform_last_fm(data)
# request_query = load_data_from_excel()
# for each in request_query:
#     print(each)
#     r = lastfm_get(each)

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




