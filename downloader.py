import subprocess
import requests

HEADERS = {'Host': 'allplay.uz',
           'x-allplay-brand': 'Apple',
           'x-allplay-version': '3.25',
           'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
           'Accept-Language': 'ru',
           'x-allplay-app': 'ios',
           'Connection': 'keep-alive',
           'Accept': 'application/json'
           }

FFMPEG_COMMAND = 'ffmpeg -i {0} -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {1}.mp4'


def main(movie_link):
    movie_id = get_movie_id(movie_link)
    movie_name = get_movie_info(movie_id)
    m3u8_url = get_m3u8_url(movie_id)
    download_movie(m3u8_url, movie_name)


def get_m3u8_url(movie_id):
    request_url = f'https://allplay.uz/api/v1/file/play/1/{movie_id}?support_trial=1&type=hls'
    get_request = requests.get(request_url, headers=HEADERS)
    response = get_request.json()

    m3u8_url = response['data']['url']
    return m3u8_url


def get_movie_info(movie_id):
    request_url = f'https://allplay.uz/api/v1/movie/1/{movie_id}'
    get_request = requests.get(request_url, headers=HEADERS)
    response = get_request.json()

    movie_name = response['data']['title']
    return movie_name


def download_movie(m3u8_url, file_name):
    command = FFMPEG_COMMAND.format(m3u8_url, file_name).split(' ')
    print(command)
    subprocess.call(command)


def get_movie_id(movie_link):
    movie_id = str(movie_link).split('movie/')[1].split('/')[0]
    return movie_id


if __name__ == '__main__':
    main('https://allmovies.uz/movie/36836/greenland')
