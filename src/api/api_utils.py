from datetime import date, datetime
from random import random
from time import sleep
import typing
if typing.TYPE_CHECKING:
    from src.api.tinder_api import TinderAPI


'''
This file collects important data on your matches,
allows you to sort them by last_activity_date, age,
gender, message count, and their average successRate.
'''


def get_match_info(api: "TinderAPI"):
    matches = api.get_updates()['matches']
    match_info = {}
    for match in matches[:len(matches)]:
        try:
            person = match['person']
            person_id = person['_id']  # This ID for looking up person
            match_info[person_id] = {
                "name": person['name'],
                "match_id": match['id'],  # This ID for messaging
                "message_count": match['message_count'],
                "photos": get_photos(person),
                "bio": person['bio'],
                "gender": person['gender'],
                "avg_successRate": get_avg_successRate(person),
                "messages": match['messages'],
                "age": calculate_age(match['person']['birth_date']),
                "distance": api.get_person(person_id)['results']['distance_mi'],
                "last_activity_date": match['last_activity_date'],
            }
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            # continue
    print("All data stored in variable: match_info")
    return match_info


def get_match_id_by_name(match_info, name):
    '''
    Returns a list_of_ids that have the same name as your input
    '''
    list_of_ids = []
    for match in match_info:
        if match_info[match]['name'] == name:
            list_of_ids.append(match_info[match]['match_id'])
    if len(list_of_ids) > 0:
        return list_of_ids
    return {"error": "No matches by name of %s" % name}


def get_photos(person):
    '''
    Returns a list of photo urls
    '''
    photos = person['photos']
    photo_urls = []
    for photo in photos:
        photo_urls.append(photo['url'])
    return photo_urls


def calculate_age(birthday_string):
    '''
    Converts from '1997-03-25T22:49:41.151Z' to an integer (age)
    '''
    birthyear = int(birthday_string[:4])
    birthmonth = int(birthday_string[5:7])
    birthday = int(birthday_string[8:10])
    today = date.today()
    return today.year - birthyear - ((today.month, today.day) < (birthmonth, birthday))


def get_avg_successRate(person):
    '''
    SuccessRate is determined by Tinder for their 'Smart Photos' feature
    '''
    photos = person['photos']
    curr_avg = 0
    for photo in photos:
        try:
            photo_successRate = photo['successRate']
            curr_avg += photo_successRate
        except:
            return -1
    return curr_avg / len(photos)


def sort_by_value(match_info, sortType):
    '''
    Sort options are:
        'age', 'message_count', 'gender'
    '''
    return sorted(match_info.items(), key=lambda x: x[1][sortType], reverse=True)


def convert_from_datetime(difference):
    secs = difference.seconds
    days = difference.days
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    return ("%d days, %d hrs %02d min %02d sec" % (days, h, m, s))


def get_last_activity_date(now, ping_time):
    ping_time = ping_time[:len(ping_time) - 5]
    datetime_ping = datetime.strptime(ping_time, '%Y-%m-%dT%H:%M:%S')
    difference = now - datetime_ping
    since = convert_from_datetime(difference)
    return since


def how_long_has_it_been(match_info):
    now = datetime.utcnow()
    times = {}
    for person in match_info:
        name = match_info[person]['name']
        ping_time = match_info[person]['last_activity_date']
        since = get_last_activity_date(now, ping_time)
        times[name] = since
        print(name, "----->", since)
    return times


def pause():
    '''
    In order to appear as a real Tinder user using the app...
    When making many API calls, it is important to pause a...
    realistic amount of time between actions to not make Tinder...
    suspicious!
    '''
    nap_length = 3 * random()
    print('Napping for %f seconds...' % nap_length)
    sleep(nap_length)
