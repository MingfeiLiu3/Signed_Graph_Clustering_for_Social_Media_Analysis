import networkx as nx

import stag.graphio
import stag.graph
import stag.cluster

import pymysql
from random import sample

import Graph_builder
import Signed_2_Lift_Clustering
import Signed_Bipartite_Clustering
import comparison_H_neg_TO_H
import comparison_H_TO_H_neg


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS Random_USER_LIST_G_neg")

sql_random_G_neg = """CREATE TABLE Random_USER_LIST_G_neg (
            User_Id CHAR(20),
            cond_H_neg float,
            cond_H_from_H_neg float,
            cond_H float,
            cond_H_neg_from_H float)"""
cursor.execute(sql_random_G_neg)

print('finish CREATE TABLE Random_USER_LIST_G_neg')

neg_user_list = []
sql_list = "SELECT * FROM USER_LIST_G_neg"
try:
    cursor.execute(sql_list)
    results_list = cursor.fetchall()
    for row_list in results_list:
        user_id = row_list[0]
        neg_user_list.append(user_id)
except:
    raise Exception("Error: unable to fetch data")



sample = sample(neg_user_list, 2000)
for s in sample:
    
    sweep_set_H, cond_H = Signed_2_Lift_Clustering.signed_2_lift_clustering(s)
    print('The conductnace from signed 2-lift clustering algorithm: '+ str(cond_H))
    cond_H_neg_from_H = comparison_H_TO_H_neg.convert_H_TO_H_neg(sweep_set_H)
    print('Based on the same vertices, convert the H to the H_neg. The conductance of H_neg: '+ str(cond_H_neg_from_H))
    
    sweep_set_H_neg, cond_H_neg = Signed_Bipartite_Clustering.signed_bipartite_clustering(s)
    print('The conductnace from signed bipartiteness clustering algorithm: '+ str(cond_H_neg))
    cond_H_from_H_neg = comparison_H_neg_TO_H.convert_H_neg_TO_H(sweep_set_H_neg)
    print('Based on the same vertices, convert the H_neg to the H. The conductance of H: '+ str(cond_H_from_H_neg))
    print('\n')
    
    sql_add = """INSERT INTO Random_USER_LIST_G_neg(User_Id, cond_H_neg, cond_H_from_H_neg, cond_H, cond_H_neg_from_H)
                VALUES (%s,%s,%s,%s,%s)""" 
    par_add = (s, cond_H_neg, cond_H_from_H_neg, cond_H, cond_H_neg_from_H)
    try:
        cursor.execute(sql_add, par_add)
        db.commit()
    except:
        print('rollback')
        db.rollback()
    