import networkx as nx

import stag.graphio
import stag.graph
import stag.cluster

import pymysql
from random import sample

#import Graph_builder
import LocBipartDC_rand
import LocSigned2L_rand_NORetweet
import H_neg_TO_H_SA
import H_SA_TO_H_neg


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS Random_USER_LIST_G_neg_NORetweet")

sql_random_G_neg = """CREATE TABLE Random_USER_LIST_G_neg_NORetweet (
            User_Id CHAR(20),
            cond_H_neg float,
            cond_H_SA_from_H_neg float,
            cond_H_SA float,
            cond_H_neg_from_H_SA float)"""
cursor.execute(sql_random_G_neg)

print('finish CREATE TABLE Random_USER_LIST_G_neg_NORetweet')

# Using the same random user sets in the previous comparison
neg_user_list = []
sql_list = "SELECT * FROM Random_USER_LIST_G_neg"
try:
    cursor.execute(sql_list)
    results_list = cursor.fetchall()
    for row_list in results_list:
        user_id = row_list[0]
        neg_user_list.append(user_id)
except:
    raise Exception("Error: unable to fetch data")


#sample = sample(neg_user_list, 10)
for s in neg_user_list:
    
    sweep_set_H_SA, cond_H_SA = LocSigned2L_rand_NORetweet.LocSigned2L_clustering(s)
    print('The conductnace from signed 2-lift clustering algorithm: '+ str(cond_H_SA))
    cond_H_neg_from_H_SA = H_SA_TO_H_neg.convert_H_SA_TO_H_neg(sweep_set_H_SA)
    print('Based on the same vertices, convert the H_SA to the H_neg. The conductance of H_neg: '+ str(cond_H_neg_from_H_SA))
    
    sweep_set_H_neg, cond_H_neg = LocBipartDC_rand.LocBipartDC_clustering(s)
    print('The conductnace from signed bipartiteness clustering algorithm: '+ str(cond_H_neg))
    cond_H_SA_from_H_neg = H_neg_TO_H_SA.convert_H_neg_TO_H_SA(sweep_set_H_neg)
    print('Based on the same vertices, convert the H_neg to the H_SA. The conductance of H: '+ str(cond_H_SA_from_H_neg))
    print('\n')
    
    # Store the selected sample to the Database
    sql_add = """INSERT INTO Random_USER_LIST_G_neg_NORetweet(User_Id, cond_H_neg, cond_H_SA_from_H_neg, cond_H_SA, cond_H_neg_from_H_SA)
                VALUES (%s,%s,%s,%s,%s)""" 
    par_add = (s, cond_H_neg, cond_H_SA_from_H_neg, cond_H_SA, cond_H_neg_from_H_SA)
    try:
        cursor.execute(sql_add, par_add)
        db.commit()
    except:
        print('rollback')
        db.rollback()
    