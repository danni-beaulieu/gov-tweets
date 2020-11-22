
import itertools
import operator

import govtweets.read
import govtweets.visual


def compute_frequencies(column):
    return {
        key: len(list(grp))
        for (key, grp) in itertools.groupby(sorted(column.to_list()[0]))
    }


def get_top_k(words_freq, k=20):
    total = float(sum(words_freq.values()))
    top_k = sorted(words_freq.items(), key=operator.itemgetter(1), reverse=True)[:k]
    return [(word, freq / total) for (word, freq) in top_k]


def _main():

    (legislators, tweets) = govtweets.read.read_all(tweet_files='2020-10-*.json')

    tweets_persons = tweets.merge(
        legislators, left_on='user_id', right_on='twitter_id')

    # Groups hashtags by party:
    ht_by_party = tweets_persons.groupby('party').agg({'hashtags': 'sum'})
    
    ht_rep = compute_frequencies(ht_by_party.hashtags[ht_by_party.index == 'Republican'])
    ht_dem = compute_frequencies(ht_by_party.hashtags[ht_by_party.index == 'Democrat'])

    govtweets.visual.wordcloud_dem_rep(ht_dem, ht_rep, "./wc.png", show=False)

    ht_freq_rep = get_top_k(ht_rep)
    ht_freq_dem = get_top_k(ht_dem)

    govtweets.visual.words_hist(ht_freq_rep, '#AA2222', 'Republican', './ht-rep.png', show=False)
    govtweets.visual.words_hist(ht_freq_dem, '#224499', 'Democrat', './ht-dem.png', show=False)


if __name__ == "__main__":
    _main()
