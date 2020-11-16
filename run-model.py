
import nltk

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

import govtweets.read
import govtweets.model


_TRAIN_TEST_SEED = 42


def _main():

    (legislators, tweets) = govtweets.read.read_all(tweet_files='*.json')

    tweets_persons = tweets.merge(
        legislators, left_on='user_id', right_on='twitter_id')

    # Keep only two major parties and assign a numeric label to each
    parties = {'Democrat': 0, 'Republican': 1}  # , 'Independent': 2}
    parties_inv = {0: 'Democrat', 1: 'Republican'}
    tweets_persons = tweets_persons[tweets_persons.party.apply(parties.__contains__)]

    tweets_persons['party_id'] = tweets_persons.party.apply(parties.get)

    tokenizer = nltk.tokenize.TweetTokenizer()
    count_vect = CountVectorizer(
        ngram_range=(1, 1),
        tokenizer=tokenizer.tokenize,
        stop_words=nltk.corpus.stopwords.words('english'))

    pipeline = Pipeline([
        ('vectorizer', count_vect),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB()),
        # ('classifier', SGDClassifier(
        #     loss='hinge', penalty='l2', alpha=1e-3,
        #     random_state=_TRAIN_TEST_SEED, max_iter=10,
        #     tol=None))
    ])

    (tweets_train, tweets_test,
     labels_train, labels_test) = train_test_split(
         tweets_persons.text, tweets_persons.party_id,
         test_size=0.2, random_state=_TRAIN_TEST_SEED)

    pipeline.fit(tweets_train, labels_train)

    print("TRAIN Accuracy:", pipeline.score(tweets_train, labels_train))
    print("TEST Accuracy:", pipeline.score(tweets_test, labels_test))

    test_tweets = [

        """
        Thankfully, @SpeakerPelosis power to move a radical, far-left agenda
        through the House was weakened with Republican gains.
        """,

        """
        Millions of Americans stood up against Donald Trump and elected decency
        back to the White House.
        """
    ]

    test_predict = pipeline.predict(test_tweets)

    for (text, label) in zip(test_tweets, test_predict):
        print("\nTEXT:%s\nPARTY prediction: %s" % (text, parties_inv.get(label)))


if __name__ == "__main__":
    _main()
