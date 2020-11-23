
import nltk
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import learning_curve

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

    (train_sizes, train_scores, test_scores) = learning_curve(
        pipeline, tweets_persons.text, tweets_persons.party_id,
        cv=5, scoring='accuracy', train_sizes=np.linspace(0.05, 1.0, 20))

    # Create means and standard deviations of training set scores
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)

    # Create means and standard deviations of test set scores
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # Draw lines
    plt.plot(train_sizes, train_mean, '--', color="#111111",  label="Training score")
    plt.plot(train_sizes, test_mean, color="#111111", label="Cross-validation score")

    # Draw bands
    plt.fill_between(train_sizes, train_mean - train_std,
                     train_mean + train_std, color="#DDDDDD")

    plt.fill_between(train_sizes, test_mean - test_std,
                     test_mean + test_std, color="#DDDDDD")

    # Create plot
    plt.title("Learning Curve")
    plt.xlabel("Training Set Size")
    plt.ylabel("Accuracy Score")
    plt.legend(loc="best")
    
    plt.tight_layout()
    plt.savefig('./learning-curve.png', dpi=300)


if __name__ == "__main__":
    _main()
