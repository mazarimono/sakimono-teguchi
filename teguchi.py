from requests_html import HTMLSession
import urllib.request
import re
import os
import time

def get_monthly_urls():
    folder_dates = []
    urls = []
    session = HTMLSession()
    r = session.get('https://www.jpx.co.jp/markets/derivatives/perticipant-volume/index.html')
    r.html.render(sleep=5)
    address = r.html.find('option')

    for i in address:
        date = i.text.replace('年', '-')
        date = date.replace('月', '')
        if len(date) == 6:
            date = date[:5] + '0' + date[5]
            folder_dates.append(date)
        else:
            folder_dates.append(date)
        urls.append('https://www.jpx.co.jp' + i.html.split('"')[1])

    return folder_dates, urls

def make_folder(folder_dates):
    for date in folder_dates:
        os.mkdir('{}'.format(date))

def get_daily_urls(monthly_urls='https://www.jpx.co.jp/markets/derivatives/perticipant-volume/index.html'):
    day_csv = []
    night_csv = []
    dd = []

    session = HTMLSession()
    r = session.get(monthly_urls) 
    r.html.render()
    csvs = r.html.find('.component-normal-table')
    csvs2 = csvs[0].find('a')
    dates = csvs[0].find('.a-center.w-space')

# absolute_linksがsetに入っているので、ややこしい処理を！

    csv3 = list()
    for i in csvs2:
        for i2 in i.absolute_links:
            csv3.append(i2)

    for url in csv3:
        if url.endswith('NET.csv'):
            pass
        elif url.endswith('day.csv'):
            day_csv.append(url)
        elif url.endswith('night.csv'):
            night_csv.append(url)

    for d in dates:
        dd.append(d.text)
        
    return dd, day_csv, night_csv

def download(date, day_data, night_data):
    for d, d_csv, n_csv in zip(date, day_data, night_data):
        folder_name = d.split('/')[0] + '-' + d.split('/')[1]
        file_name = d.replace('/', '')
        urllib.request.urlretrieve(d_csv, '{}/day_{}.csv'.format(folder_name, file_name))
        urllib.request.urlretrieve(n_csv, '{}/night_{}.csv'.format(folder_name, file_name))

        time.sleep(3)

if __name__ == '__main__':
    f_name, monthly_urls = get_monthly_urls()
    make_folder(f_name)
    for url in monthly_urls:
        date, day_data, night_data = get_daily_urls(url)

        download(date, day_data, night_data)
        