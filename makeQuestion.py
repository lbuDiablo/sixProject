#!/usr/bin/env python
# coding: utf-8

# In[14]:


import sys
import pymysql
import random
import json
import os
from textrankr import TextRank
from konlpy.tag import Okt
import nltk
    
DB_HOST = 'sixproject.cica4dx4uu4o.ap-northeast-2.rds.amazonaws.com'
DB_NAME = 'QnA'
DB_USER = 'sixth'
DB_PASSWORD = 'password'

if len(sys.argv) == 3 and isinstance(sys.argv[1], str) and isinstance(sys.argv[2], str) :
    category = sys.argv[1]
    keyword = sys.argv[2]
else :
    print('Test Mode. format : python collect.py [category] [keyword]')
    category = '인물'
    keyword = '이순신'


# In[4]:


# 카테고리,키워드로 select문을 통해 문장들을 불러오기
def select_sentence():
    text = ''
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8')
    try :
        with conn.cursor() as curs:
            sql = "SELECT sentence FROM CATEGORY WHERE keyword_name = '" + keyword + "' AND category_name ='" + category + "';"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                #print(row)
                text = text+row[0]+ '.'
    finally:
        conn.close()
        return text


# In[5]:


# 카테고리에 해당하는 문장들을 select문을 통해 불러오기
def select_sentence_by_keyword() :
    text = []
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8')
    try :
        with conn.cursor() as curs:
            sql = "SELECT sentence, keyword_name FROM CATEGORY WHERE category_name='" + category + "';"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                text.append(row)
    finally :
        conn.close()
        return text;


# In[6]:


def tokenize(doc):
    return [''.join(t) for t in pos_tagger2.phrases(doc)]


# In[7]:


def term_exists(doc):
    return {'{}'.format(word): (word in set(doc)) for word in tokens}


# In[15]:


text = select_sentence()
textrank = TextRank(text)
main_sentences = textrank.summarize(5).split('\n')
random.shuffle(main_sentences)
main_sentence = main_sentences.pop()
main_sentence2 = main_sentences.pop()
main_sentence3 = main_sentences.pop()


# In[20]:


pos_tagger2 = Okt()

trainSet = select_sentence_by_keyword()
train_docs = [(tokenize(row[0]), row[1]) for row in trainSet]
tokens = [t for d in train_docs for t in d[0]]
train_xy = [(term_exists(d), c) for d,c in train_docs]

classifier = nltk.NaiveBayesClassifier.train(train_xy)
classifier.show_most_informative_features(200)


# In[12]:


def makeMC4(sentence) :
    test_docs = tokenize(sentence)
    test_sentence_features = {word: (word in tokens) for word in test_docs}
    keys = list(classifier.prob_classify(test_sentence_features)._prob_dict.keys())
    probs = []
    for key in keys :
        probs.append((classifier.prob_classify(test_sentence_features).prob(key),key))
    probs.sort()
    print(probs)
    answer = probs[len(probs)-1]
    options = []
    for i in range(4) :
        options.append(probs.pop())
        if(len(probs) == 0) :
            break;
    random.shuffle(options)
    print(options)
    print(answer)
    QnA = '{'
    if keyword in sentence:
        QnA = QnA + '"question" : "빈칸에 들어갈 알맞은 인물을 고르시오.",'
        QnA = QnA + '"sentence" : "'+sentence.replace(keyword, '＿＿＿')+'",'
    else :
        QnA = QnA + '"question" : "다음은 어떤 인물에 관한 설명인가?",'
        QnA = QnA + '"sentence" : "'+sentence+'",'
    QnA = QnA + '"option1" : "'+options[0][1]+'",'
    QnA = QnA + '"option2" : "'+options[1][1]+'",'
    QnA = QnA + '"option3" : "'+options[2][1]+'",'
    QnA = QnA + '"option4" : "'+options[3][1]+'",'
    for i in range(len(options)) :
        if(answer == options[i]) :
            QnA = QnA + '"answer" : "'+str(i+1)+'"}'
    return QnA


# In[13]:


if 'Desktop' not in os.getcwd() :
    os.chdir(os.getcwd()+'\Desktop')
    print(os.getcwd())
#QnA = json.loads(makeMC4(main_sentence))
QnA = '['
QnA = QnA + makeMC4(main_sentence) + ','
QnA = QnA + makeMC4(main_sentence2) + ','
QnA = QnA + makeMC4(main_sentence3) + ']'
f = open("test.json", 'w')
f.write(QnA)
f.close()

