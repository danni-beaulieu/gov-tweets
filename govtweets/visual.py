
import wordcloud


def save_wordcloud(words, fname):
    wc = wordcloud.WordCloud(
        background_color='white',
        width=1600,
        height=1024).generate(' '.join(words))
    wc.to_file(fname)
