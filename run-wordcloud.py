
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


def words_frequencies(data, colname):
    "Group words from a column `colname` by party"
    words_by_party = data.groupby('party').agg({colname: 'sum'})
    words_rep = compute_frequencies(words_by_party[colname][words_by_party.index == 'Republican'])
    words_dem = compute_frequencies(words_by_party[colname][words_by_party.index == 'Democrat'])
    return (words_rep, words_dem)


def _main():

    (legislators, tweets) = govtweets.read.read_all(tweet_files='2020-11-*.json')
    tweets_persons = tweets.merge(legislators, left_on='user_id', right_on='twitter_id')

    # Get the most popular hashtags for each party and plot them

    (ht_rep, ht_dem) = words_frequencies(tweets_persons, 'hashtags')

    ht_freq_rep = get_top_k(ht_rep)
    ht_freq_dem = get_top_k(ht_dem)

    govtweets.visual.words_hist(
        ht_freq_rep, '#AA2222', 'Most frequent hashtags', 'Republicans',
        './ht-rep.png', show=False)

    govtweets.visual.words_hist(
        ht_freq_dem, '#224499', 'Most frequent hashtags', 'Democrats',
        './ht-dem.png', show=False)

    govtweets.visual.wordcloud_dem_rep(ht_dem, ht_rep, "./wc.png", show=False)

    # Same as above, but for words

    (words_rep, words_dem) = words_frequencies(tweets_persons, 'clean_tokens')

    words_freq_rep = get_top_k(words_rep)
    words_freq_dem = get_top_k(words_dem)

    govtweets.visual.words_hist(
        words_freq_rep, '#AA2222', 'Most frequent words', 'Republicans',
        './words-rep.png', show=False)

    govtweets.visual.words_hist(
        words_freq_dem, '#224499', 'Most frequent words', 'Democrats',
        './words-dem.png', show=False)

    # Wordcloud for references

    (ref_rep, ref_dem) = words_frequencies(tweets_persons, 'references')
    govtweets.visual.wordcloud_dem_rep(ref_dem, ref_rep, "./wc-refs.png", show=False)


if __name__ == "__main__":
    _main()
