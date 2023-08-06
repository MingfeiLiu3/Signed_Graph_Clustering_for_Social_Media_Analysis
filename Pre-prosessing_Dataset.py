import json
import os
from numba.typed import Dict

from textblob import TextBlob

import pymysql

import py3langid as langid
import stag.graphio
import stag.graph
import stag.cluster


tweets = []
for date_file in os.listdir('./2020-06'):
    print(date_file)
    if date_file != ".DS_Store":
        path = './2020-06/' + date_file
        for file_name in os.listdir(path):
            json_file = open(path +'/'+ file_name,'r', encoding='utf-8')
            for line in json_file .readlines():
                dic = json.loads(line)
                tweets.append(dic)

#  -----------------------------------------------------------------------------------------------------------------
#     Tweet Type  ||        How to identify       ||  (Original)User 1 field  ||  User 2 field  ||   Text field
#  -----------------------------------------------------------------------------------------------------------------
#        Reply        in_reply_to_user_id != None        in_reply_to_user_id       user/id          text 
#       Retweet         retweeted_status != None    retweeted_status/user/id       user/id 
#   Quoted Tweet       quoted_status != None & 
#                   retweeted_status == None        quoted_status/user/id        user/id   or extended_tweet/full_text


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS REPLY_STATUS")

sql_creat = """CREATE TABLE REPLY_STATUS (
         Original_User CHAR(20),
         Ind_Original_User int,
         Reply_User CHAR(20),
         Ind_Reply_User int,
         Polarity FLOAT,
         Text VARCHAR(1000))"""
cursor.execute(sql_creat)


user_list = []

for tweet in tweets:
    if tweet.get('in_reply_to_user_id_str') != None:
        #If the represented Tweet is a reply, in_reply_to_user_id_str = original Tweet’s author ID
        original_reply_user = tweet.get('in_reply_to_user_id_str')
        #user = The user who posted this Tweet
        reply_user = tweet.get('user').get('id_str')
            
        if tweet.get('truncated') == False:
            reply_tweet = tweet.get('text')
        else:
            reply_tweet = tweet.get('extended_tweet').get('full_text')

        # unpack the result tuple in variables & identified language and probability
        lang, prob = langid.classify(reply_tweet)
        split_text = reply_tweet.split('https://')
        split_text_parts = split_text[0].split(' ')
            
        del_list = []
        for part in split_text_parts:
            if part != '' and part[0] == '@':
                del_list.append(part)
        for p in del_list:
            split_text_parts.remove(p)
        final_reply_text = ' '.join(split_text_parts)
        reply_pol = TextBlob(final_reply_text).sentiment.polarity
            
        #remove the zero weights
        if lang == 'en' and abs(prob) > 100 and reply_pol != 0.0:
            #remove the self reply
            if reply_user != original_reply_user:
                
                #store all users
                if original_reply_user not in user_list:
                    user_list.append(original_reply_user)
                if reply_user not in user_list:
                    user_list.append(reply_user)
                        
                        
                sql_insert = """INSERT INTO REPLY_STATUS(Original_User, Ind_Original_User, Reply_User, Ind_Reply_User, Polarity, Text)
                            VALUES (%s,%s,%s,%s,%s,%s)""" 
                par = (original_reply_user, user_list.index(original_reply_user), reply_user, user_list.index(reply_user), reply_pol, final_reply_text)
                    
                try:
                    cursor.execute(sql_insert,par)
                    db.commit()
                except:
                    print('Insert REPLY_STATUS rollback')
                    db.rollback()
                    

cursor.execute("DROP TABLE IF EXISTS RETWEET_STATUS")
cursor.execute("DROP TABLE IF EXISTS QUOTED_STATUS")

sql_creat_re = """CREATE TABLE RETWEET_STATUS (
         Original_User CHAR(20),
         Ind_Original_User int,
         Retweet_User CHAR(20),
         Ind_Retweet_User int,
         Polarity FLOAT)"""
cursor.execute(sql_creat_re)


sql_creat_qu = """CREATE TABLE QUOTED_STATUS (
         Original_User CHAR(20),
         Ind_Original_User int,
         Quoted_User CHAR(20),
         Ind_Quoted_User int,
         Polarity FLOAT,
         Text VARCHAR(1000))"""
cursor.execute(sql_creat_qu)


for tweet_a in tweets:
    # Users can amplify the broadcast of Tweets authored by other users by retweeting.
    # Retweets can be distinguished from typical Tweets by the existence of a retweeted_status attribute. 
    # This attribute contains a representation of the original Tweet that was retweeted.
    retweeted_status = tweet_a.get('retweeted_status')
    quoted_status = tweet_a.get('quoted_status')
    if retweeted_status != None:
        original_retweet_user = retweeted_status.get('user').get('id_str')
        #user = The user who posted this Tweet
        retweet_user = tweet_a.get('user').get('id_str')
        
        #any retweet is regarded as postive 
        retweet_pol = 0.5
        
        #store all users
        if original_retweet_user not in user_list:
            user_list.append(original_retweet_user)
        if retweet_user not in user_list:
            user_list.append(retweet_user)
            
        if original_retweet_user != retweet_user: 
            sql_insert_re = """INSERT INTO RETWEET_STATUS(Original_User, Ind_Original_User, Retweet_User, Ind_Retweet_User, Polarity)
                            VALUES (%s,%s,%s,%s,%s)""" 
            par_re = (original_retweet_user, user_list.index(original_retweet_user), retweet_user, user_list.index(retweet_user), retweet_pol)
                    
            try:
                cursor.execute(sql_insert_re,par_re)
                db.commit()
            except:
                print('Insert RETWEET_STATUS rollback')
                db.rollback()
    
    #This field only surfaces when the Tweet is a quote Tweet.
    #This attribute contains the Tweet object of the original Tweet that was quoted.
    elif quoted_status != None:
        original_quoted_user = quoted_status.get('user').get('id_str')
        #user = The user who posted this Tweet
        quoted_user = tweet_a.get('user').get('id_str')
        
        if quoted_status.get('truncated') == True:
            quoted_tweet = quoted_status.get('extended_tweet').get('full_text')
        else:
            quoted_tweet = quoted_status.get('text')
            
        # unpack the result tuple in variables & identified language and probability
        lang, prob = langid.classify(quoted_tweet)
        split_text = quoted_tweet.split('https://')
        split_text_parts = split_text[0].split(' ')
            
        del_list = []
        for part in split_text_parts:
            if part != '' and part[0] == '@':
                del_list.append(part)
        for p in del_list:
            split_text_parts.remove(p)
        final_quoted_text = ' '.join(split_text_parts)
        quoted_pol = TextBlob(final_quoted_text).sentiment.polarity
            
        #remove the zero weights
        if lang == 'en' and abs(prob) > 100 and quoted_pol != 0.0:
            #remove the self reply
            if quoted_user != original_quoted_user:
                
                #store all users
                if original_quoted_user not in user_list:
                    user_list.append(original_quoted_user)
                if quoted_user not in user_list:
                    user_list.append(quoted_user)
                
                sql_insert_qu = """INSERT INTO QUOTED_STATUS(Original_User, Ind_Original_User, Quoted_User, Ind_Quoted_User, Polarity, Text)
                            VALUES (%s,%s,%s,%s,%s,%s)""" 
                par_qu = (original_quoted_user, user_list.index(original_quoted_user), quoted_user, user_list.index(quoted_user), quoted_pol, final_quoted_text)
                    
                try:
                    cursor.execute(sql_insert_qu,par_qu)
                    db.commit()
                except:
                    print('Insert QUOTED_STATUS rollback')
                    db.rollback()
    
db.close()

