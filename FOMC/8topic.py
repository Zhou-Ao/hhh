# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:55:45 2017

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

fileNames = []

folder = 'fomctopicmodeling\\Minutes'
#folder = 'Minutes'
#folder = 'FOMC_clean'

for fileName in os.listdir(os.path.join(os.getcwd(), folder)):
    if fileName.endswith('.txt'):
        fileNames.append(os.path.join(os.getcwd(), folder, fileName))
        
def readFile(path):
    with open(path, 'r') as f:
        return f.read()
        
def readFileToPara(path):
    print(path)
    with open(path, 'r') as f:
        return [line.decode('utf-8') for line in f.readlines() if len(line)>1]
        
#docs = map(readFile, fileNames)
docs = map(readFileToPara, fileNames)
docs = [para for doc in docs for para in doc]


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
    
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens 
        if ((i not in en_stop)
#        and (i not in myStopWords)
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

    for doc in clean_docs:
        tdm.add_doc(' '.join(doc))
        
    tdm_row_generator = tdm.rows(cutoff = 1)
    vocab = np.array(tdm_row_generator.next())
    return np.array([row for row in tdm_row_generator]), vocab

tdm, vocab = generateTDM(clean_docs)

model = lda.LDA(n_topics=6, random_state=1991)

model.fit(tdm)

topic_word = model.topic_word_
n_top_words = 11
for i, topic_dist in enumerate(topic_word):
     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
     
doc_topic = model.doc_topic_
topic_df = pd.DataFrame(doc_topic)
topic_df.to_csv(folder + "_6 topic prob.csv")

mintues_docs = map(readFile, fileNames)
