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
import time
import os

def load_data_from_excel(csv_input):
    request_query = []
    req = {}
    data = pd.read_excel(r''+csv_input)
    if 'Title' in data and 'Artist' in data:
        data = data.rename(columns={'Title': 'title', 'Artist': 'artist'})
    df = pd.DataFrame(data, columns=['title', 'artist'])
    # print(df)
    for index, row in df.iterrows():
        req['method'] = 'track.getInfo'
        req['autocorrect'] = 1
        req['track'] = row['title'][1:-1]
        req['artist'] = row['artist']
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
    ys = 'ca791ebdea3b7ba81ff4bd70cff59124423'
    ys=ys[1:-2]
    USER_AGENT = 'law-school-copyright'
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = ys
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


def perform_last_fm(data, current_finished_count,total_records,progress_callback):
    if 'Title' in data and 'Artist' in data:
        data = data.rename(columns={'Title': 'title', 'Artist': 'artist'})
    df = pd.DataFrame(data, columns=['title', 'artist'])
    print(df)
    request_query = []
    req = {}
    for index, row in df.iterrows():
        req['method'] = 'track.getInfo'
        req['autocorrect'] = 1
        # print('track,', row['title'])
        req['track'] = row['title'][1:-1]
        req['artist'] = row['artist']
        request_query.append(req)
        req = {}
    out_query = []
    out_dict = {}
    i = 0
    for each in request_query:
        if __name__ != "__main__":
            progress_callback.emit(int(100 * (i+current_finished_count) / total_records))
        out_dict['artist'] = each['artist']
        out_dict['track'] = each['track']
        # print(each)
        max_retry=10
        current_retry=0
        is_api_success=False
        while not is_api_success and current_retry<max_retry:
            is_api_success=True
            try:
                api_result=lastfm_get(each)
            except Exception as e:
                print(e)
                is_api_success=False
                time.sleep(1)
            current_retry+=1
        out_dict.update(api_result)
        out_query.append(out_dict)
        out_dict = {}
        i += 1

    print(out_query)
    out_df = pd.DataFrame(out_query)
    print(out_df)
    print(out_df.dtypes)
    return out_df

def perform_last_fm_s(data, output_path, progress_callback):
    #1/0
    out_put = {}
    total_records=0
    for sheet_name in data:
        total_records+=data[sheet_name].shape[0]

    writer = pd.ExcelWriter(os.path.join(output_path,'last_fm_output.xlsx'), engine='xlsxwriter')

    current_finished_count=0
    for each in data:
        print(data[each])
        out_df = (perform_last_fm(data[each],current_finished_count,total_records,progress_callback))
        out_df.to_excel(writer, sheet_name=each)
        current_finished_count+=data[each].shape[0]
    if __name__ != "__main__":
        progress_callback.emit(100)
    writer.save()
    return 'Finished'

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
    perform_last_fm_s(data, 'progress_callback')
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




