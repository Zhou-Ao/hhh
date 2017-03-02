# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 10:57:14 2017

@author: strategy.intern.2
"""


import os
#import string
import re

import numpy as np
import pandas as pd

from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
import textmining

import lda

os.chdir('U:\\Python Project\\FOMC\\fomctopicmodeling')

folder = 'Speech'

#names = ["Yellen", "Brainard", "Lacker", "Dudley", "Fischer", "Powell", "Tarullo"]
names = ["Yellen", "Brainard", "Lacker"]

fileNames = []

for name in names:
    for fileName in os.listdir(os.path.join(os.getcwd(), folder, name)):
        if fileName.endswith('.txt'):
            fileNames.append(os.path.join(os.getcwd(), folder, name, fileName))
            
def readFile(path):
    with open(path, 'r') as f:
        return f.read().decode('utf-8')
        
docs = map(readFile, fileNames)

def cleanDoc(doc):
    # tokenization
#    print('Cleaning ' + doc + '...')
    tokenizer = RegexpTokenizer(r'\w+')
    raw = doc.lower()
    raw = re.sub('[0-9]', '', raw)
#    raw.translate(None, string.digits)
    tokens = tokenizer.tokenize(raw)
    
    # create English stop words list
    en_stop = get_stop_words('en')
    
#    myStopWords = ["monday", "tuesday", "wednesday", "thursday", "firday", "saturday", "sunday",
#                "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
#                "year", "quarter", "month", "day",
#                "first", "second", "third", "fourth",
#                "federal", "reserve", "session", "percent",
#                "recent", "fomc", "cre"]

    myStopWords = [
#                    "monday", "tuesday", "wednesday", "thursday", "firday", "saturday", "sunday",
#                    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
#                    "year", "quarter", "month", "day",
#                    "first", "second", "third", "fourth",
#                    "federal", "reserve", "session", "percent",
#                    "recent", "fomc", "cre",
                 "a", "about", "above", "across", "after", "again", "against", "all", "almost", 
                 "alone", "along", "already", "also", "although", "always", "am", "among", "an", "and", "another", 
                 "any", "anybody", "anyone", "anything", "anywhere", "are", "area", "areas", "aren\'t", "around", 
                 "as", "ask", "asked", "asking", "asks", "at", "away", "b", "back", "backed", "backing", "backs", 
                 "be", "became", "because", "become", "becomes", "been", "before", "began", "behind", "being", 
                 "beings", "below", "best", "better", "between", "big", "both", "but", "by", "c", "came", "can", 
                 "cannot", "can\'t", "case", "cases", "certain", "certainly", "clear", "clearly", "come", "could", 
                 "couldn\'t", "d", "did", "didn\'t", "differ", "different", "differently", "do", "does", "doesn\'t", 
                 "doing", "done", "don\'t", "down", "downed", "downing", "downs", "during", "e", "each", "early", 
                 "either", "end", "ended", "ending", "ends", "enough", "even", "evenly", "ever", "every", "everybody", 
                 "everyone", "everything", "everywhere", "f", "face", "faces", "fact", "facts", "far", "felt", "few", 
                 "find", "finds", "first", "for", "four", "from", "full", "fully", "further", "furthered", "furthering", 
                 "furthers", "g", "gave", "general", "generally", "get", "gets", "give", "given", "gives", "go", "going", 
                 "good", "goods", "got", "great", "greater", "greatest", "group", "grouped", "grouping", "groups", "h", 
                 "had", "hadn\'t", "has", "hasn\'t", "have", "haven\'t", "having", "he", "he\'d", "he\'ll", "her", "here", 
                 "here\'s", "hers", "herself", "he\'s", "high", "higher", "highest", "him", "himself", "his", "how", 
                 "however", "how\'s", "i", "i\'d", "if", "i\'ll", "i\'m", "important", "in", "interest", "interested", 
                 "interesting", "interests", "into", "is", "isn\'t", "it", "its", "it\'s", "itself", "i\'ve", "j", "just", 
                 "k", "keep", "keeps", "kind", "knew", "know", "known", "knows", "l", "large", "largely", "last", "later", 
                 "latest", "least", "less", "let", "lets", "let\'s", "like", "likely", "long", "longer", "longest", "m", 
                 "made", "make", "making", "man", "many", "may", "me", "member", "members", "men", "might", "more", "most", 
                 "mostly", "mr", "mrs", "much", "must", "mustn\'t", "my", "myself", "n", "necessary", "need", "needed", 
                 "needing", "needs", "never", "new", "newer", "newest", "next", "no", "nobody", "non", "noone", "nor", "not", 
                 "nothing", "now", "nowhere", "number", "numbers", "o", "of", "off", "often", "old", "older", "oldest", "on", 
                 "once", "one", "only", "open", "opened", "opening", "opens", "or", "order", "ordered", "ordering", "orders", 
                 "other", "others", "ought", "our", "ours", "ourselves", "out", "over", "own", "p", "part", "parted", "parting", 
                 "parts", "per", "perhaps", "place", "places", "point", "pointed", "pointing", "points", "possible", "present", 
                 "presented", "presenting", "presents", "problem", "problems", "put", "puts", "q", "quite", "r", "rather", 
                 "really", "right", "room", "rooms", "s", "said", "same", "saw", "say", "says", "second", "seconds", "see", 
                 "seem", "seemed", "seeming", "seems", "sees", "several", "shall", "shan\'t", "she", "she\'d", "she\'ll", "she\'s", 
                 "should", "shouldn\'t", "show", "showed", "showing", "shows", "side", "sides", "since", "small", "smaller", 
                 "smallest", "so", "some", "somebody", "someone", "something", "somewhere", "state", "states", "still", "such", 
                 "sure", "t", "take", "taken", "than", "that", "that\'s", "the", "their", "theirs", "them", "themselves", "then", 
                 "there", "therefore", "there\'s", "these", "they", "they\'d", "they\'ll", "they\'re", "they\'ve", "thing", "things", 
                 "think", "thinks", "this", "those", "though", "thought", "thoughts", "three", "through", "thus", "to", "today", 
                 "together", "too", "took", "toward", "turn", "turned", "turning", "turns", "two", "u", "under", "until", "up", 
                 "upon", "us", "use", "used", "uses", "v", "very", "w", "want", "wanted", "wanting", "wants", "was", "wasn\'t", 
                 "way", "ways", "we", "we\'d", "well", "we\'ll", "wells", "went", "were", "we\'re", "weren\'t", "we\'ve", "what", 
                 "what\'s", "when", "when\'s", "where", "where\'s", "whether", "which", "while", "who", "whole", "whom", "who\'s", 
                 "whose", "why", "why\'s", "will", "with", "within", "without", "won\'t", "work", "worked", "working", "works", 
                 "would", "wouldn\'t", "x", "y", "year", "years", "yes", "yet", "you", "you\'d", "you\'ll", "young", "younger", 
                 "youngest", "your", "you\'re", "yours", "yourself", "yourselves", "you\'ve", "z"]
    
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens 
        if ((i not in en_stop)
        and (i not in myStopWords)
        and re.match('[a-z]+', i)
        and len(i) > 1)]
    
#    print(stopped_tokens)
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    texts = [p_stemmer.stem(i) for i in stopped_tokens]
    
    return texts
    
clean_docs = map(cleanDoc, docs)


# document-term matrix
def generateTDM(docs):
    tdm = textmining.TermDocumentMatrix()

    for doc in docs:
        tdm.add_doc(' '.join(doc))
        
    tdm_row_generator = tdm.rows(cutoff = 1)
    vocab = np.array(tdm_row_generator.next())
    return np.array([row for row in tdm_row_generator]), vocab

tdm, vocab = generateTDM(clean_docs)

model = lda.LDA(n_topics=8, n_iter=1000, random_state=1991)

model.fit(tdm)


topic_word = model.topic_word_
n_top_words = 11
for i, topic_dist in enumerate(topic_word):
     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
     
doc_topic = model.doc_topic_
topic_df = pd.DataFrame(doc_topic)
topic_df.to_csv(folder + "_speech topic prob.csv")


#estimate fed minutes
fileNames_minutes = []

folder_minutes = 'FOMC_raw'
for fileName in os.listdir(os.path.join(os.getcwd(), folder_minutes)):
    if fileName.endswith('.txt'):
        fileNames_minutes.append(os.path.join(os.getcwd(), folder_minutes, fileName))

minutes_docs = map(readFile, fileNames_minutes)
clean_minutes_docs = map(cleanDoc, minutes_docs)

clean_minutes_docs_vocab = []
for doc in clean_minutes_docs:
    clean_minutes_docs_vocab.append([word for word in doc if word in vocab])

tdm_minutes, vocab_minutes = generateTDM(clean_minutes_docs_vocab)
doc_topic_test = model.transform(tdm_minutes)

for fileName, topics in zip(fileNames_minutes, doc_topic_test):
    print("{} (top topic: {})".format(fileName, topics.argmax()))
    
doc_topic_test_pf = pd.DataFrame(doc_topic_test)
doc_topic_test_pf.to_csv(folder + '_minutes_topic prob.csv')
