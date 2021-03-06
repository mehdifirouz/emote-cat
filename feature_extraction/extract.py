from collections import Counter
import nltk
import random
import string
import sys
sys.path.append('..')
import scripts.twokenize as twokenize
import scripts.emoticons as emoticons
import scripts
from scripts import crossval

romney_file = '../Tweet-Data/Romney-Labeled.csv'
tunisia_file = '../Tweet-Data/Tunisia-Labeled.csv'

def ok_word(word):
    word_cleaned = ''.join([c for c in word if c not in set(string.punctuation)])
    if word_cleaned == "":
        if emoticons.analyze_tweet(word) != "SAD":
            if emoticons.analyze_tweet(word) != "HAPPY": 
                return False
    return True
        

def train(file):
    """ Dictionary of word counts for each label """
    features_list = []
    
    f = open(romney_file)
    
    for line in f.readlines():
        line = line.rstrip().lower()
        [HITID, tweet, W1, A1, W2, A2, Agmt, label, date] = line.split(',')
        tokens = twokenize.tokenize(tweet)
        if "no_agreement" in label: continue
        print label
        for token in tokens:
            if not ok_word(token): continue
        features_list.append(({'token': token}, label))

        """ Feature Extraction """
        random.shuffle(features_list)
        classifier = nltk.NaiveBayesClassifier.train(features_list)

        classifier.show_most_informative_features(100)
        print nltk.classify.accuracy(classifier, features_list)

def test(file):
    f = open(romney_file)

    total_guesses = 0.0
    total_correct = 0.0

    for line in f.readlines():
        line = line.rstrip()
        [HITID, tweet, W1, A1, W2, A2, Agmt, label, date] = line.split(',')
        tokens = twokenize.tokenize(tweet)
        if "no_agreement" in label: continue
        votes = Counter()
        for token in tokens:
            if not ok_word(token): continue
            feature = {'token': token}
            guess = classifier.classify(feature)
            votes[guess] += 1
        [(pred_label, count)] = votes.most_common(1)
        if pred_label == label: total_correct += 1.0
        total_guesses += 1.0

    print total_guesses, total_correct
    print total_correct / total_guesses


test = crossval.KFoldData(romney_file)
print test.train()


if __name__ == "__main__":
    classifier = train(romney_file)
    test(romney_file)
