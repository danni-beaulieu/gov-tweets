"helper functions to read and preprocess the JSON data"

import json
import glob
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

# Compute the age of each legislator:
# data['age'] = data.birthday.apply(lambda d: 2020 - int(d[:4]))

# Average age of the party members
# data.groupby(by='party').aggregate(np.mean).age


def read_tweets(data_dir='./data/tweets/', files='*.json'):
    "Read tweets JSON data into a single pandas DataFrame"
    data = pandas.DataFrame()
    for fname in glob.glob(data_dir + '/' + files, recursive=False):
        tweets = json.load(open(fname, encoding='utf-8'))
        data = data.append(tweets)
    return data


def tokenize_tweets(data):
    tokenizer = nltk.tokenize.TweetTokenizer()
    return data.text.apply(tokenizer.tokenize)

# data['hashtags'] = data.tokenized.apply(
#     lambda words: [w[1:] for w in words if w[0] == '#'])
# ht = []
# data.hashtags.aggregate(ht.extend)
# ...use ht to generate the wordcloud
