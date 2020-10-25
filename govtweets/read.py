"helper functions to read and preprocess the JSON data"

import json
import glob
import datetime

import pandas
import nltk


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


def extract_term_data(person, date=None):
    if date is None:
        date = datetime.date.today()
    for term in person['terms']:
        start = datetime.date.fromisoformat(term['start'])
        end = datetime.date.fromisoformat(term['end'])
        if date >= start and date <= end:
            return (start, end, term)
    return None


def parse_personal_data(data):
    """
    Convert legislators info from a dictionary into pandas DataFrame
    and compute extra columns for the personal data.
    """
    records = []
    for (twitter_id, person) in data.items():
        term_data = extract_term_data(person)
        if term_data is not None:
            (start, end, term) = term_data
            records.append({
                'twitter_id': twitter_id,
                'name': person['name']['official_full'],
                'birthday': person['bio']['birthday'],
                'gender': person['bio']['gender'],
                'start': start,
                'end': end,
                'party': term['party'],
                'type': term['type'],
                'state': term['state'],
                'district': term.get('district')
            })
    df = pandas.DataFrame.from_records(records)
    # Compute the age of each legislator:
    df['age'] = df.birthday.apply(lambda d: 2020 - int(d[:4]))
    return df


def read_tweets(data_dir='./data/tweets/', files='*.json'):
    "Read tweets JSON data into a single pandas DataFrame"
    data = pandas.DataFrame()
    for fname in glob.glob(data_dir + '/' + files, recursive=False):
        tweets = json.load(open(fname, encoding='utf-8'))
        data = data.append(tweets)
    return data


def parse_tweets(data):
    "Tokenize and extract hashtags and @names"
    tokenizer = nltk.tokenize.TweetTokenizer()
    data['tokenized'] = data.text.apply(tokenizer.tokenize)
    data['hashtags'] = data.tokenized.apply(
        lambda words: [w[1:] for w in words if w[0] == '#'])
    data['references'] = data.tokenized.apply(
        lambda words: [w[1:] for w in words if w[0] == '@'])
    return data


def read_all(data_dir='./data/'):
    "return two data frames: (legislators, tweets)"
    legislators = read_personal_data(data_dir)
    tweets = read_tweets(data_dir + "/tweets/")
    legislators = parse_personal_data(legislators)
    tweets = parse_tweets(tweets)
    return (legislators, tweets)
