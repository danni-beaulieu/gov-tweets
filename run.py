
import govtweets.read
import govtweets.visual


def _main():

    (legislators, tweets) = govtweets.read.read_all()

    tweets_persons = tweets.merge(
        legislators, left_on='user_id', right_on='twitter_id')

    # Groups hashtags by party:
    ht_by_party = tweets_persons.groupby('party').agg({'hashtags': 'sum'})
    
    ht_rep = ht_by_party.hashtags[ht_by_party.index == 'Republican'].to_list()[0]
    ht_dem = ht_by_party.hashtags[ht_by_party.index == 'Democrat'].to_list()[0]

    govtweets.visual.save_wordcloud(ht_rep, "./wc_rep.png")
    govtweets.visual.save_wordcloud(ht_dem, "./wc_dem.png")


if __name__ == "__main__":
    _main()
