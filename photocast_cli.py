'''CLI for PhotoCast system.

Usage:
    photocast_cli.py upload <token> <folder>
    photocast_cli.py build photographer <token>
    photocast_cli.py build index <token>

Options:
    -h Help doc.
'''

import requests
import os
import docopt
import logging

#API_PREFIX = 'http://localhost:8080' # test
API_PREFIX = 'https://photo.hupili.net/'

def api_request(method, api_path, token, *args, **kwargs):
    api_url = f'{API_PREFIX}/{api_path}'
    cookies = {'token': token, 'type': 'cli'}
    if method == 'post':
        r = requests.post(api_url, *args, cookies=cookies, **kwargs)
    elif method == 'get':
        r = requests.get(api_url, *args, cookies=cookies, **kwargs)
    return r.json()


def post_photo(token, photo_path):
    '''
    A token is binded to a photographer, aka label, i.e. race-name-location.
    '''
    files = {'file': open(photo_path, 'rb')}
    r = api_request('post', 'upload', token, files=files)
    return r


def post_folder(token, photo_folder):
    count = 0
    for fn in os.listdir(photo_folder):
        count += 1
        print(f'Upload photo {count}')
        photo_path = f'{photo_folder}/{fn}'
        print('post photo:', photo_path)
        try:
            r = post_photo(token, photo_path)
            print('result:')
            print(r)
        except Exception as e:
            logging.warning(f'Exception: {e}')


def build_photographer(token):
    r = api_request('get', 'build/photographer/', token)
    print(r)
    return r


def build_index(token):
    r = api_request('get', 'build/index/', token)
    print(r)
    return r


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    print(arguments)
    if arguments['upload']:
        print('Uploading a folder.')
        token = arguments['<token>']
        folder = arguments['<folder>']
        post_folder(token, folder)
    elif arguments['build']:
        if arguments['photographer']:
            token = arguments['<token>']
            build_photographer(token)
        elif arguments['index']:
            token = arguments['<token>']
            build_index(token)
