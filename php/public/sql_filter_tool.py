#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import tensorflow as tf
import random
import sys


####################################################
# cut words function                               #
####################################################
def cut(contents, cut=1):
    results = []
    for content in contents:
        words = content.split()
        result = []
        for word in words:
            result.append(word[:cut])
        results.append(' '.join([token for token in result]))
    return results

####################################################
# divide train/test set function                   #
####################################################
'''
def divide(x, y, train_prop):
    random.seed(1234)
    x = np.array(x)
    y = np.array(y)
    tmp = np.random.permutation(np.arange(len(x)))
    x_tr = x[tmp][0:0]
    y_tr = y[tmp][0:0]
    x_te = x[-1:]
    y_te = y[-1:]
    return x_tr, x_te, y_tr, y_te

'''
def divide(x, y):

    x = np.array(x)
    y = np.array(y)

    x_te = x[-1:]
    y_te = y[-1:]
    return x_te, y_te

####################################################
# making input function                            #
####################################################
def make_input(documents, max_document_length):  # 문장 , 200
    # tensorflow.contrib.learn.preprocessing 내에 VocabularyProcessor라는 클래스를 이용
    # 모든 문서에 등장하는 단어들에 인덱스를 할당
    # 길이가 다른 문서를 max_document_length로 맞춰주는 역할
    vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(max_document_length)  # 객체 선언
    x = np.array(list(vocab_processor.fit_transform(documents)))
    ### 텐서플로우 vocabulary processor
    # Extract word:id mapping from the object.
    # word to ix 와 유사
    vocab_dict = vocab_processor.vocabulary_._mapping
    # Sort the vocabulary dictionary on the basis of values(id).
    sorted_vocab = sorted(vocab_dict.items(), key=lambda x: x[1])
    # Treat the id's as index into list and create a list of words in the ascending order of id's
    # word with id i goes at index i of the list.
    vocabulary = list(list(zip(*sorted_vocab))[0])
    return x, vocabulary, len(vocab_processor.vocabulary_)

####################################################
# make output function                             #
####################################################
def make_output(points, threshold):
    results = np.zeros((len(points),2))
    for idx, point in enumerate(points):
        if point > threshold:
            results[idx,0] = 1
        else:
            results[idx,1] = 1
    return results

####################################################
# check maxlength function                         #
####################################################
def check_maxlength(contents):
    max_document_length = 0
    for document in contents:
        document_length = len(document.split())
        if document_length > max_document_length:
            max_document_length = document_length
    return max_document_length

####################################################
# loading function                                 #
####################################################
def loading_rdata(data_path):
    # R에서 title과 contents만 csv로 저장한걸 불러와서 제목과 컨텐츠로 분리
    # write.csv(corpus, data_path, fileEncoding='utf-8', row.names=F)
    corpus = pd.read_table(data_path, sep=",", encoding="utf-8")
    corpus = np.array(corpus)  # shape (20000, 2)
    contents = []
    points = []

    # --------
    #contents = sys.argv[1]
    #points = sys.argv[2]
    # --------

    for idx,doc in enumerate(corpus):
        if isNumber(doc[0]) is False:
            #content = normalize(doc[0], english=eng, number=num, punctuation=punc)
            #contents.append(content)
            contents.append(doc[0])
            points.append(doc[1])

    contents.append(sys.argv[1])
    #print(sys.argv[1])
    #contents.append('좋아에요!!')
    points.append(1.0)    # 하나 해서  acc 이 1이나오면  긍정   acc이 0이나오면 부정.

    return contents, points

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

