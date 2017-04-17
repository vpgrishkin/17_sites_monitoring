import sys
import os
import datetime

import whois
from termcolor import colored
import requests
from requests.exceptions import ConnectionError, Timeout


DAYS_BEFORE_EXPIRATION_DATE = 30


def get_file_name_or_exit():
    if len(sys.argv) == 1:
        print('No params')
        work_file = input('Input file name:')
    else:
        work_file = sys.argv[1]
        if os.path.isfile(work_file):
            print('Work file: {}'.format(work_file))
    if not os.path.exists(work_file):
        print('{} doesn\'t exist'.format(work_file))
        sys.exit(1)
    return work_file


def get_urls_list_from_file(file_name):
    with open(file_name) as file:
        return file.read().split()


def is_server_respond_with_200(url):
    try:
        response = requests.get(url)
    except ConnectionError:
        return False, 'ConnectionError'
    except Timeout:
        return False, 'Timeout'
    if response is None:
        return False, None
    status = response.status_code
    if status == 200:
        return True, status
    return False, status


def get_domain_expiration_date(url):
    expiration_site_date = whois.whois(url).expiration_date
    if isinstance(expiration_site_date, list):
        return expiration_site_date[0]
    else:
        return expiration_site_date


def is_expiration_date_soon(expiration_date):
    today = datetime.datetime.today()
    if expiration_date:
        return (expiration_date - today).days >= DAYS_BEFORE_EXPIRATION_DATE


if __name__ == '__main__':
    file_name = get_file_name_or_exit()
    urls = get_urls_list_from_file(file_name)
    for url in urls:
        is_200, staus = is_server_respond_with_200(url)
        print_color = 'green' if is_200 else 'red'
        print(colored('URL:{} staus:{}'.format(url, staus), print_color))
        expiration_date = get_domain_expiration_date(url)
        print_color = 'red' if is_expiration_date_soon(expiration_date) else 'green'
