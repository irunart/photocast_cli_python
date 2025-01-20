'''CLI for PhotoCast system.

Usage:
    photocast_cli.py upload <token> <folder>
    photocast_cli.py upload_from_drive <token>
    photocast_cli.py test <token> <input_file>
    photocast_cli.py build photographer <token>
    photocast_cli.py build index <token>

Options:
    -h Help doc.
'''

import requests
import os
import docopt
import logging
from multiprocessing.pool import Pool

ALLOWED_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.JPG',
    '.heic',
    '.HEIC',
]

logging.basicConfig(level=logging.INFO)


if os.environ.get('DEBUG', None) == 'True':
    # Dev server. Change to your flask settings.
    API_PREFIX = 'http://localhost:8080'
    logging.info(f'Use dev API: {API_PREFIX}')
else:
    API_PREFIX = 'https://photo.runart.net/'
    logging.info(f'Use prod API: {API_PREFIX}')


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

def upload_photo_from_drive(token):
    r = api_request('post', '/upload/drive/', token)
    return r

def post_photo_test(token, photo_path):
    '''
    A token is binded to a photographer, aka label, i.e. race-name-location.
    '''
    files = {'file': open(photo_path, 'rb')}
    r = api_request('post', 'upload', token, files=files, params={'test': 'true'})
    return r

def upload_arg_func(arg):
    upload_file(*arg)

def upload_file(token, pf, len_files, i):
    logging.info(f'Upload photo ID: {i} / {len_files}')
    logging.info(f'post photo: {pf}')
    if any(pf.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        try:
            r = post_photo(token, pf)
            logging.info(f'Upload result: {r}')
            return True
        except Exception as e:
            logging.warning(f'Exception: {e}')
            return pf
    else:
        logging.info(f'Not supported extension. Skip.')
        return True
    
def post_folder(token, photo_folder):
    files = os.listdir(photo_folder)
    len_files = len(files)

    task_queue = [(token, os.path.join(photo_folder, f), len_files, i+1) for i, f in enumerate(files)]
    pool = Pool(16)
    jobs = pool.map(upload_arg_func, task_queue)
    jobs = [j for j in jobs if isinstance(j, str)]
    logging.info(f'processing failed jobs: {jobs}')
    for i, j in enumerate(jobs):
        loop_count = 0
        while upload_file(token, j, len(jobs), i)!=True and loop_count<3:
            loop_count += 1
            logging.info(f'Upload failed job: {j}, retrying...{loop_count+1}') 
    pool.close()


def build_photographer(token):
    r = api_request('get', 'build/photographer/', token)
    logging.info(f'build_photographer: {r}')
    return r


def build_index(token):
    r = api_request('get', 'build/index/', token)
    logging.info(f'build_index: {r}')
    return r


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    print(arguments)
    if arguments['upload']:
        print('Uploading a folder.')
        token = arguments['<token>']
        folder = arguments['<folder>']
        post_folder(token, folder)
    elif arguments['upload_from_drive']:
        print('Uploading from Google Drive')
        token = arguments['<token>']
        r = upload_photo_from_drive(token)
        print(r)
        print('Number of results:', len(r['result']['results']))
    elif arguments['build']:
        if arguments['photographer']:
            token = arguments['<token>']
            build_photographer(token)
        elif arguments['index']:
            token = arguments['<token>']
            build_index(token)
    elif arguments['test']:
        print('Test photo upload.')
        token = arguments['<token>']
        input_file = arguments['<input_file>']
        ret = post_photo_test(token, input_file)
        print(ret)
        url = f'https://storage.googleapis.com/photocast/{ret["filename"]}'
        print(f'Visit the uploaded image at following URL: {url}')
