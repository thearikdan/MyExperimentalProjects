#binary sentiment analysis
import nltk
import random
from nltk.corpus import movie_reviews
import pickle

#documents = [(list(movie_reviews.words(fileid)), category)
#             for category in movie_reviews.categories()
#             for fileid in movie_reviews.fileids(category)]

documents = []
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
#        print (list(movie_reviews.words(fileid)))
#        print(category)
        documents.append((list(movie_reviews.words(fileid)), category))

random.shuffle(documents)
#print(documents[1])

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

all_words_freq_dist = nltk.FreqDist(all_words)
#print(all_words_freq_dist.most_common(15))

#print (all_words_freq_dist["stupid"])

word_features = list(all_words_freq_dist.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


#print ((find_features((movie_reviews.words('neg/cv000_29416.txt')))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

training_set = featuresets[:1900]
testing_set = featuresets[1900:]


classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Naive Bayes acuracy :", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)


save_classifier = open("naivebayes.pickle", "wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()
