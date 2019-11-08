#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import pymysql

if len(sys.argv) == 3 and isinstance(sys.argv[1], str) and isinstance(sys.argv[2], str) :
    category = sys.argv[1]
    keyword = sys.argv[2]
else :
    print('format : python collect.py [category] [keyword]')
    exit()
    
DB_HOST = 'sixproject.cica4dx4uu4o.ap-northeast-2.rds.amazonaws.com'
DB_NAME = 'QnA'
DB_USER = 'sixth'
DB_PASSWORD = 'password'


# In[26]:


f = open('C:/Users/user/Desktop/paragraph.txt', 'r', encoding='utf8')
text = f.read()
str = text.split('.')
testSet1 = []
for i in range(len(str)-1) :
    testSet1.append(str[i])
    print(testSet1)


# In[44]:


def select_all():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8')
    try :
        with conn.cursor() as curs:
            sql = 'select * from CATEGORY'
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)
    finally:
        conn.close()


# In[43]:


def insert():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8')
    try :
        with conn.cursor() as curs:
            for i in testSet1 : 
                sql = "insert into CATEGORY values(0, '" + category + "','" + keyword + "','" + i + "');"
                curs.execute(sql)
                rs = curs.fetchall()
            conn.commit()
            for row in rs:
                print(row)
    finally:
        conn.close()

insert();


# In[ ]:




