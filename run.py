
import itertools
import random

import numpy
import PIL
import wordcloud
import matplotlib.pyplot as plt

import govtweets.read
import govtweets.visual


def compute_frequencies(column):
    return {
        key: len(list(grp))
        for (key, grp) in itertools.groupby(sorted(column.to_list()[0]))
    }


def recolor_red(word, font_size, position, orientation, random_state=None, **kwargs):
    return "rgb(%d%%, 0%%, 0%%)" % random.randint(60, 100)


def recolor_blue(word, font_size, position, orientation, random_state=None, **kwargs):
    return "rgb(0%%, 0%%, %d%%)" % random.randint(60, 100)


def _main():

    (legislators, tweets) = govtweets.read.read_all()

    tweets_persons = tweets.merge(
        legislators, left_on='user_id', right_on='twitter_id')

    # Groups hashtags by party:
    ht_by_party = tweets_persons.groupby('party').agg({'hashtags': 'sum'})
    
    ht_rep = compute_frequencies(ht_by_party.hashtags[ht_by_party.index == 'Republican'])
    ht_dem = compute_frequencies(ht_by_party.hashtags[ht_by_party.index == 'Democrat'])

    img_rep = numpy.array(PIL.Image.open("./data/images/elephant.png"))[:1600,:,:]
    img_dem = numpy.array(PIL.Image.open("./data/images/donkey.png"))[:1600,:,:]

    wc_rep = wordcloud.WordCloud(
        background_color='white',
        mask=255 - img_rep[:,:,3],
        width=1600, height=1024
        ).generate_from_frequencies(ht_rep)

    wc_dem = wordcloud.WordCloud(
        background_color='white',
        mask=255 - img_dem[:,:,3],
        width=1600, height=1024
        ).generate_from_frequencies(ht_dem)

    plt.subplot(2, 1, 1)
    plt.imshow(wc_rep.recolor(color_func=recolor_red), interpolation="bilinear")
    plt.axis("off")

    plt.subplot(2, 1, 2)
    plt.imshow(wc_dem.recolor(color_func=recolor_blue), interpolation="bilinear")
    plt.axis("off")

    fig = plt.gcf()
    fig.set_size_inches(10.5, 18.5)
    fig.savefig('./wc.png', dpi=200)

    # plt.show()


if __name__ == "__main__":
    _main()
