import requests
import pytz
import datetime


def get_pages_count():
    raw_response = requests.get('http://devman.org/api/challenges/solution_attempts')
    json_response = raw_response.json()
    return json_response['number_of_pages']


def load_attempts():
    offset = 1
    pages = get_pages_count() + offset
    for page in range(1, pages):
        raw_result = requests.get('http://devman.org/api/challenges/solution_attempts/?page={}'.format(page))
        records = raw_result.json()['records']
        for user_attempt in records:
            yield user_attempt


def get_midnighters():
    pass

if __name__ == '__main__':
    start_datetime = datetime.time(hour=0, minute=0, microsecond=0)
    end_datetime = datetime.time(hour=6, minute=0, microsecond=0)
    for user in load_attempts():
        timezone = pytz.timezone(user['timezone'])
        time = timezone.localize(datetime.datetime.fromtimestamp(user['timestamp']))
        if (time.time() > start_datetime) and (time.time() < end_datetime):
            print(time.strftime('%H:%M'))
