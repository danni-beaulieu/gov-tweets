
import random

import numpy
import PIL
import matplotlib.pyplot as plt

import wordcloud


def recolor_red(word, font_size, position, orientation, random_state=None, **kwargs):
    return "rgb(%d%%, %d%%, %d%%)" % (
        random.randint(60, 100),
        random.randint(0, 15),
        random.randint(0, 15))


def recolor_blue(word, font_size, position, orientation, random_state=None, **kwargs):
    return "rgb(%d%%, %d%%, %d%%)" % (
        random.randint(0, 15),
        random.randint(0, 30),
        random.randint(60, 100))


def wordcloud_dem_rep(freq_dem, freq_rep, fname=None, show=True):
    """
    Build wordclouds for democrats and republicans
    using word frequency dictionaries.
    """
    img_rep = numpy.array(PIL.Image.open("./data/images/elephant.png"))
    img_dem = numpy.array(PIL.Image.open("./data/images/donkey.png"))

    wc_rep = wordcloud.WordCloud(
        background_color='white',
        mask=255 - img_rep[:,:,3],
        width=1600, height=1024
        ).generate_from_frequencies(freq_rep)

    wc_dem = wordcloud.WordCloud(
        background_color='white',
        mask=255 - img_dem[:,:,3],
        width=1600, height=1024
        ).generate_from_frequencies(freq_dem)

    fig, (plot0, plot1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 6]})

    plot0.imshow(wc_rep.recolor(color_func=recolor_red), interpolation="bilinear")
    plot0.axis("off")

    plot1.imshow(wc_dem.recolor(color_func=recolor_blue), interpolation="bilinear")
    plot1.axis("off")

    fig.tight_layout()
    fig.set_size_inches(8, 12)

    if fname is not None:
        fig.savefig(fname, dpi=300)

    if show:
        plt.show()


def words_hist(words_freq, color, ylabel, title=None, fname=None, show=True):

    labels = [word for (word, freq) in words_freq]
    data = [freq for (word, freq) in words_freq]

    plt.figure()

    plt.yticks(range(len(labels)), labels)
    plt.barh(range(len(data)), numpy.array(data) * 100, color=color, alpha=0.9)

    plt.xlabel('Frequency, %')
    plt.ylabel(ylabel)
    plt.title(title)

    plt.tight_layout()

    if fname is not None:
        plt.savefig(fname, dpi=300)

    if show:
        plt.show()
