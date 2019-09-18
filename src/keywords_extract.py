import re
import nltk
import spacy
import gensim, pprint
import gensim.corpora as corpora
import numpy as np 
import pandas as pd 
from nltk.corpus import stopwords
from pprint import pprint

def readFile(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()
       
def stopWordList():
    stop_words = stopwords.words('english')
    more_stop_words = [line.rstrip('\n') for line in readFile('/Users/friedahuang/Desktop/XProject/doc/stopwords.txt')]
    stop_words.extend(more_stop_words)
    return stop_words

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(sentence, deacc=True))  # deacc=True removes punctuations

data = list(sent_to_words(readFile('/Users/friedahuang/Desktop/XProject/doc/articles.txt')))
id2word = corpora.Dictionary(list(data))
corpus = [id2word.doc2bow(text) for text in data]

i = [[(id2word[id], freq) for id, freq in cp] for cp in corpus[:100000]]

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)


pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]    