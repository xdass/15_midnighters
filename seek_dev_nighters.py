import requests
import pytz
import datetime


def get_pages_count():
    raw_response = requests.get('http://devman.org/api/challenges/solution_attempts')
    json_response = raw_response.json()
    return json_response['number_of_pages']


def load_attempts():
    offset = 1
    records = []
    response = requests.get('http://devman.org/api/challenges/solution_attempts', params={'page': 1})
    pages = response.json()['number_of_pages'] + offset
    records.extend(response.json()['records'])
    for page in range(2, pages):
        payload = {'page': page}
        raw_result = requests.get('http://devman.org/api/challenges/solution_attempts/', params=payload)
        records.extend(raw_result.json()['records'])
    yield from records


def get_midnighters():
    start_time = datetime.time(hour=0, minute=0, microsecond=0)
    end_time = datetime.time(hour=6, minute=0, microsecond=0)
    midnighters_attempts = []
    for user_attempt in load_attempts():
        timezone = pytz.timezone(user_attempt['timezone'])
        _datetime = timezone.localize(datetime.datetime.fromtimestamp(user_attempt['timestamp']))
        if (_datetime.time() > start_time) and _datetime.time() < end_time:
            midnighters_attempts.append(user_attempt)
    return midnighters_attempts


def print_midnighters(midnighters_attempts):
    unique_midnighters = {attempt_info['username'] for attempt_info in midnighters_attempts}
    print('Список сов Devman\'a:')
    for midnighter_name in unique_midnighters:
        print(midnighter_name)

if __name__ == '__main__':
    all_midnighters = get_midnighters()
    print_midnighters(all_midnighters)

