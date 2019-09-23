import os
import argparse
import json
import time
import random
import logging
import sys
import requests
from src.api.connection import Connection
from src.api.tinder_api import TinderAPI
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('log.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
log.addHandler(stdout_handler)
log.addHandler(file_handler)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--token', dest='api_token')
    parser.add_argument('-o', '--output', default='all_recs.json', dest='output_filename')
    parser.add_argument('mode', choices=['scrape', 'build'])
    args = parser.parse_args()
    if args.mode == 'scrape':
        cxn = Connection(args.api_token)
        api = TinderAPI(cxn)
        scrape(args, api)
    elif args.mode == 'build':
        build(args)


def build(args):
    with open(args.output_filename, 'r') as fd:
        all_recs = json.load(fd)
    for _id in all_recs:
        fldr = os.path.join('Your Recommendations', _id)
        os.makedirs(fldr, exist_ok=True)
        with open(os.path.join(fldr, 'data.json'), 'w') as fd:
            json.dump(all_recs[_id], fd)
            for photo in all_recs[_id]['photos']:
                with open(os.path.join(fldr, photo['id'])+'.jpeg', 'wb') as photo_fd:
                    r = requests.get(photo['url'])
                    photo_fd.write(r.content)


def scrape(args, api: TinderAPI):
    if os.path.exists(args.output_filename):
        with open(args.output_filename, 'r') as fd:
            all_results = json.load(fd)
    else:
        all_results = {}
    try:
        for i in range(0, 1):
            recs = api.get_recommendations()
            if recs['status'] == 200:
                log.info('Successfully retrieved recommendations')
                for rec in recs['results']:
                    _id = rec['_id']
                    if _id in all_results:
                        log.info('Duplicate recommendation: %s', _id)
                        all_results.update(rec)
                    else:
                        all_results[_id] = rec
                    log.info('Done processing %s, disliking now', _id)
                    api.dislike(_id)
                    time.sleep(random.random() * 2)
            else:
                log.error('ERROR')
                log.error(recs)
                break
    finally:
        with open(args.output_filename, 'w+') as fd:
            json.dump(all_results, fd, indent=2)


if __name__ == '__main__':
    main()
