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
        payload = {'page': page}
        raw_result = requests.get('http://devman.org/api/challenges/solution_attempts/', params=payload)
        records = raw_result.json()['records']
        for user_attempt in records:
            yield user_attempt


def get_midnighters():
    start_time = datetime.time(hour=0, minute=0, microsecond=0)
    end_time = datetime.time(hour=6, minute=0, microsecond=0)
    midnighters = []
    for user_attempt in load_attempts():
        timezone = pytz.timezone(user_attempt['timezone'])
        time = timezone.localize(datetime.datetime.fromtimestamp(user_attempt['timestamp']))
        if (time.time() > start_time) and (time.time() < end_time):
            midnighters.append(user_attempt)
    return midnighters


def print_midnighters(midnighters_list):
    unique_midnighters = {item['username'] for item in midnighters_list}
    print('Список сов Devman\'a:')
    for midnighter_name in unique_midnighters:
        print(midnighter_name)

if __name__ == '__main__':
    all_midnighters = get_midnighters()
    print_midnighters(all_midnighters)

