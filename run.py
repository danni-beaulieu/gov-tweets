
import itertools

import govtweets.read
import govtweets.visual


def compute_frequencies(column):
    return {
        key: len(list(grp))
        for (key, grp) in itertools.groupby(sorted(column.to_list()[0]))
    }


def _main():

    (legislators, tweets) = govtweets.read.read_all(tweet_files='2020-10-*.json')

    tweets_persons = tweets.merge(
        legislators, left_on='user_id', right_on='twitter_id')

    # Groups hashtags by party:
    ht_by_party = tweets_persons.groupby('party').agg({'hashtags': 'sum'})
    
    ht_rep = compute_frequencies(ht_by_party.hashtags[ht_by_party.index == 'Republican'])
    ht_dem = compute_frequencies(ht_by_party.hashtags[ht_by_party.index == 'Democrat'])

    govtweets.visual.wordcloud_dem_rep(ht_dem, ht_rep, "./wc.png", False)


if __name__ == "__main__":
    _main()
