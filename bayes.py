import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle

def word_feats(words):
    return dict([(word, True) for word in words])
 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
 
negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
 
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

f = open('my_classifier.pickle', 'rb')
cl = pickle.load(f)
f.close()

cl= NaiveBayesClassifier.train(trainfeats)
f = open('my_classifier.pickle', 'wb')
pickle.dump(cl, f)
f.close()

print 'accuracy:', nltk.classify.util.accuracy(cl, testfeats)
cl.show_most_informative_features()
Compute accuracy



print(cl.classify(word_feats("I am happy")))