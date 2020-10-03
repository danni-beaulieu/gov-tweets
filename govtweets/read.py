"helper functions to read and preprocess the JSON data"

import json


def read_personal_data(data_dir='./data'):
    """
    Read the congressmen personal data and merge it with their
    social network IDs. Each entry is keyed by the twitter ID
    so it can be connected with the tweets later.
    """
    with open(data_dir + '/legislators-current.json') as jfile:
        # Load the senators and key them by their Bioguide ID
        legislators = {
            person['id']['bioguide']: person
            for person in json.load(jfile)
        }
    with open(data_dir + '/legislators-social-media.json') as jfile:
        for person in json.load(jfile):
            # Link each senator to their social media accounts
            person_id = person['id']['bioguide']
            legislators[person_id]['social'] = person['social']
    # Reads the senators' data and key each entry by twitter ID
    legislators = {
        person['social']['twitter_id']: person
        for person in legislators.values()
        if 'twitter_id' in person.get('social', {})
    }
    return legislators
