import subprocess
import sys

import requests

HEADERS = {'Host': 'allplay.uz',
           'Accept': 'application/json',
           'x-allplay-brand': 'Apple',
           'x-allplay-version': '3.25',
           'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
           'x-allplay-device-id': 'hj32hj42hgh3gh2g3h1g4h21',
           'Accept-Language': 'ru',
           'x-allplay-app': 'ios',
           'User-Agent': 'Allplay/3.25 (uz.allplay.app; build:1; iOS 14.0.0) Alamofire/4.9.1',
           'x-allplay-model': 'iPhone 12 Pro Max'
           }

FFMPEG_COMMAND = 'ffmpeg -i {0} -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {1}.mp4'

EMAIL = ''
PASSWORD = ''


def main(movie_link):
    api_token = auth(EMAIL, PASSWORD)
    movie_id = get_movie_id(movie_link)
    movie_name = get_movie_info(movie_id)
    m3u8_url = get_m3u8_url(movie_id, api_token)
    print(f'Начинаю скачивание фильма: {movie_name}')
    download_movie(m3u8_url, movie_name)


def auth(email, password):
    data = {'email': email, 'password': password, 'device_id': 'hj32hj42hgh3gh2g3h1g4h21'}
    request_url = 'https://allplay.uz/api/v1/login'
    get_request = requests.post(request_url, headers=HEADERS, data=data)
    response = get_request.json()

    if 'errors' in response.keys():
        print(response['errors']['email'][0])
        sys.exit(1)

    api_token = response['api_token']
    return api_token


def get_movie_id(movie_link):
    movie_id = str(movie_link).split('movie/')[1].split('/')[0]
    return movie_id


def get_movie_info(movie_id):
    request_url = f'https://allplay.uz/api/v1/movie/1/{movie_id}'
    get_request = requests.get(request_url, headers=HEADERS)
    response = get_request.json()

    movie_name = response['data']['title']
    return movie_name


def get_m3u8_url(movie_id, api_token):
    HEADERS['Authorization'] = 'Bearer {}'.format(api_token)
    request_url = f'https://allplay.uz/api/v1/file/play/1/{movie_id}?support_trial=1&type=hls'
    get_request = requests.get(request_url, headers=HEADERS)
    response = get_request.json()

    if 'errors' in response.keys():
        print(response['errors']['default'][0])
        sys.exit(1)

    m3u8_url = response['data']['url']
    return m3u8_url


def download_movie(m3u8_url, file_name):
    command = FFMPEG_COMMAND.format(m3u8_url, file_name).split(' ')
    subprocess.call(command)


if __name__ == '__main__':
    main('https://allmovies.uz/movie/36836/greenland')
