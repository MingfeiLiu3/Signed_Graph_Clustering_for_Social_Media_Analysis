
import stag.graphio
import stag.graph

import networkx as nx

import stag.graphio
import stag.graph
import stag.cluster

import pymysql

db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')

cursor = db.cursor()

def build_graph_G():
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_G")

    sql_creating_G = """CREATE TABLE USER_LIST_G (
            User_Id CHAR(20),
            User_Index int)"""
    cursor.execute(sql_creating_G)

    print('finish CREATE TABLE USER_LIST_G')

    #buid a undirected graph G
    G = nx.Graph()

    #store the order of adding nodes
    G_node_list = []

    sql_rep = "SELECT * FROM REPLY_STATUS"
    try:
        cursor.execute(sql_rep)
        results_rep = cursor.fetchall()
        for row_rep in results_rep:
            original_reply_user_id = row_rep[0]
            reply_user_id = row_rep[2]
            polarity_rep = row_rep[4]
        
            if original_reply_user_id != reply_user_id:
            
                if original_reply_user_id not in G_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_node_list.append(original_reply_user_id)
                    index_original_reply_user = G_node_list.index(original_reply_user_id)
                    G.add_node(index_original_reply_user)
            
                else: 
                    index_original_reply_user = G_node_list.index(original_reply_user_id)
            
            
                if reply_user_id not in G_node_list:
                    G_node_list.append(reply_user_id)
                    index_reply_user = G_node_list.index(reply_user_id)
                    G.add_node(index_reply_user)
            
                else:
                    index_reply_user = G_node_list.index(reply_user_id)
            
            
                G.add_edge(index_original_reply_user, index_reply_user, weight=polarity_rep)
                
    except:
        print ("Error: unable to fetch data")

    print('finish SELECT * FROM REPLY_STATUS')


    sql_ret = "SELECT * FROM RETWEET_STATUS"
    try:
        cursor.execute(sql_ret)
        results_ret = cursor.fetchall()
        for row_ret in results_ret:
            original_retweet_user_id = row_ret[0]
            retweet_user_id = row_ret[2]
            polarity_ret = row_ret[4]
        
            if original_retweet_user_id != retweet_user_id:
            
                if original_retweet_user_id not in G_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_node_list.append(original_retweet_user_id)
                    index_original_retweet_user = G_node_list.index(original_retweet_user_id)
                    G.add_node(index_original_retweet_user)
            
                else:
                    index_original_retweet_user = G_node_list.index(original_retweet_user_id)
            
            
                if retweet_user_id not in G_node_list:
                    G_node_list.append(retweet_user_id)
                    index_retweet_user = G_node_list.index(retweet_user_id)
                    G.add_node(index_retweet_user)
            
                else:
                    index_retweet_user = G_node_list.index(retweet_user_id)
                
                G.add_edge(index_original_retweet_user, index_retweet_user, weight=polarity_ret)
                
    except:
        print ("Error: unable to fetch data")
    
    print('finish SELECT * FROM RETWEET_STATUS')


    sql_qu = "SELECT * FROM QUOTED_STATUS"
    try:
        cursor.execute(sql_qu)
        results_qu = cursor.fetchall()
        for row_qu in results_qu:
            original_quoted_user_id = row_qu[0]
            quoted_user_id = row_qu[2]
            polarity_qu = row_qu[4]
        
            if original_quoted_user_id != quoted_user_id:
            
                if original_quoted_user_id not in G_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_node_list.append(original_quoted_user_id)
                    index_original_quoted_user = G_node_list.index(original_quoted_user_id)
                    G.add_node(index_original_quoted_user)
            
                else: 
                    index_original_quoted_user = G_node_list.index(original_quoted_user_id)
            
            
                if quoted_user_id not in G_node_list:
                    G_node_list.append(quoted_user_id)
                    index_quoted_user = G_node_list.index(quoted_user_id)
                    G.add_node(index_quoted_user)
            
                else:
                    index_quoted_user = G_node_list.index(quoted_user_id)
                
                G.add_edge(index_original_quoted_user, index_quoted_user, weight=polarity_qu)
                
    except:
        print ("Error: unable to fetch data")

    print("finish SELECT * FROM QUOTED_STATUS")

    #store the user index in G to database
    for node in G_node_list:
        sql_add = """INSERT INTO USER_LIST_G(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add = (node, G_node_list.index(node))
        try:
            cursor.execute(sql_add, par_add)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_G rollback')
            db.rollback()
        
    print('finish INSERT INTO USER_LIST_G')

    # Type stag.graph.Graph
    g = stag.graph.from_networkx(G)

    filename = "G_graph.edgelist"
    stag.graphio.save_edgelist(g, filename)
    return G


def build_graph_G_neg():
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_G_neg")

    sql_creating_G_neg = """CREATE TABLE USER_LIST_G_neg (
            User_Id CHAR(20),
            User_Index int)"""
    cursor.execute(sql_creating_G_neg)

    print('finish CREATE TABLE USER_LIST_G_neg')

    #buid a undirected graph G
    G_neg = nx.Graph()

    #store the order of adding nodes
    G_neg_node_list = []

    sql_rep = "SELECT * FROM REPLY_STATUS"
    try:
        cursor.execute(sql_rep)
        results_rep = cursor.fetchall()
        for row_rep in results_rep:
            original_reply_user_id = row_rep[0]
            reply_user_id = row_rep[2]
            polarity_rep = row_rep[4]
        
            if polarity_rep < 0 and original_reply_user_id != reply_user_id:
                
                if original_reply_user_id not in G_neg_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_neg_node_list.append(original_reply_user_id)
                    index_original_reply_user = G_neg_node_list.index(original_reply_user_id)
                    G_neg.add_node(index_original_reply_user)
            
                else: 
                    index_original_reply_user = G_neg_node_list.index(original_reply_user_id)
            
            
                if reply_user_id not in G_neg_node_list:
                    G_neg_node_list.append(reply_user_id)
                    index_reply_user = G_neg_node_list.index(reply_user_id)
                    G_neg.add_node(index_reply_user)
            
                else:
                    index_reply_user = G_neg_node_list.index(reply_user_id)
            
                G_neg.add_edge(index_original_reply_user, index_reply_user, weight=abs(polarity_rep))
                
    except:
        print ("Error: unable to fetch data")

    print('finish SELECT * FROM REPLY_STATUS')


    sql_qu = "SELECT * FROM QUOTED_STATUS"
    try:
        cursor.execute(sql_qu)
        results_qu = cursor.fetchall()
        for row_qu in results_qu:
            original_quoted_user_id = row_qu[0]
            quoted_user_id = row_qu[2]
            polarity_qu = row_qu[4]
        
            if polarity_qu < 0 and original_quoted_user_id != quoted_user_id:
            
                if original_quoted_user_id not in G_neg_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_neg_node_list.append(original_quoted_user_id)
                    index_original_quoted_user = G_neg_node_list.index(original_quoted_user_id)
                    G_neg.add_node(index_original_quoted_user)
            
                else: 
                    index_original_quoted_user = G_neg_node_list.index(original_quoted_user_id)
            
            
                if quoted_user_id not in G_neg_node_list:
                    G_neg_node_list.append(quoted_user_id)
                    index_quoted_user = G_neg_node_list.index(quoted_user_id)
                    G_neg.add_node(index_quoted_user)
            
                else:
                    index_quoted_user = G_neg_node_list.index(quoted_user_id)
                
                G_neg.add_edge(index_original_quoted_user, index_quoted_user, weight=abs(polarity_qu))
                
    except:
        print ("Error: unable to fetch data")

    print("finish SELECT * FROM QUOTED_STATUS")

    #store the user index in G to database
    for neg_node in G_neg_node_list:
        sql_add_neg = """INSERT INTO USER_LIST_G_neg(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add_neg = (neg_node, G_neg_node_list.index(neg_node))
        try:
            cursor.execute(sql_add_neg, par_add_neg)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_G_neg rollback')
            db.rollback()
        
    print('finish INSERT INTO USER_LIST_G_neg')

    # Type stag.graph.Graph
    g_neg = stag.graph.from_networkx(G_neg)

    filename = "G_neg_graph.edgelist"
    stag.graphio.save_edgelist(g_neg, filename)
    return G_neg


def build_graph_G_pos():
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_G_pos")

    sql_creating_G_pos = """CREATE TABLE USER_LIST_G_pos (
            User_Id CHAR(20),
            User_Index int)"""
    cursor.execute(sql_creating_G_pos)

    print('finish CREATE TABLE USER_LIST_G_pos')

    #buid a undirected graph G
    G_pos = nx.Graph()

    #store the order of adding nodes
    G_pos_node_list = []

    sql_rep = "SELECT * FROM REPLY_STATUS"
    try:
        cursor.execute(sql_rep)
        results_rep = cursor.fetchall()
        for row_rep in results_rep:
            original_reply_user_id = row_rep[0]
            reply_user_id = row_rep[2]
            polarity_rep = row_rep[4]
        
            if polarity_rep > 0 and original_reply_user_id != reply_user_id:
                
                if original_reply_user_id not in G_pos_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_pos_node_list.append(original_reply_user_id)
                    index_original_reply_user = G_pos_node_list.index(original_reply_user_id)
                    G_pos.add_node(index_original_reply_user)
            
                else: 
                    index_original_reply_user = G_pos_node_list.index(original_reply_user_id)
            
            
                if reply_user_id not in G_pos_node_list:
                    G_pos_node_list.append(reply_user_id)
                    index_reply_user = G_pos_node_list.index(reply_user_id)
                    G_pos.add_node(index_reply_user)
            
                else:
                    index_reply_user = G_pos_node_list.index(reply_user_id)
            
            
                G_pos.add_edge(index_original_reply_user, index_reply_user, weight=polarity_rep)
                
    except:
        print ("Error: unable to fetch data")

    print('finish SELECT * FROM REPLY_STATUS')
    

    sql_ret = "SELECT * FROM RETWEET_STATUS"
    try:
        cursor.execute(sql_ret)
        results_ret = cursor.fetchall()
        for row_ret in results_ret:
            original_retweet_user_id = row_ret[0]
            retweet_user_id = row_ret[2]
            polarity_ret = row_ret[4]
        
            if original_retweet_user_id != retweet_user_id:
            
                if original_retweet_user_id not in G_pos_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_pos_node_list.append(original_retweet_user_id)
                    index_original_retweet_user = G_pos_node_list.index(original_retweet_user_id)
                    G_pos.add_node(index_original_retweet_user)
            
                else:
                    index_original_retweet_user = G_pos_node_list.index(original_retweet_user_id)
            
            
                if retweet_user_id not in G_pos_node_list:
                    G_pos_node_list.append(retweet_user_id)
                    index_retweet_user = G_pos_node_list.index(retweet_user_id)
                    G_pos.add_node(index_retweet_user)
            
                else:
                    index_retweet_user = G_pos_node_list.index(retweet_user_id)
                
                G_pos.add_edge(index_original_retweet_user, index_retweet_user, weight=polarity_ret)
                
    except:
        print ("Error: unable to fetch data")
    
    print('finish SELECT * FROM RETWEET_STATUS')


    sql_qu = "SELECT * FROM QUOTED_STATUS"
    try:
        cursor.execute(sql_qu)
        results_qu = cursor.fetchall()
        for row_qu in results_qu:
            original_quoted_user_id = row_qu[0]
            quoted_user_id = row_qu[2]
            polarity_qu = row_qu[4]
        
            if polarity_qu > 0 and original_quoted_user_id != quoted_user_id:
            
                if original_quoted_user_id not in G_pos_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_pos_node_list.append(original_quoted_user_id)
                    index_original_quoted_user = G_pos_node_list.index(original_quoted_user_id)
                    G_pos.add_node(index_original_quoted_user)
            
                else: 
                    index_original_quoted_user = G_pos_node_list.index(original_quoted_user_id)
            
            
                if quoted_user_id not in G_pos_node_list:
                    G_pos_node_list.append(quoted_user_id)
                    index_quoted_user = G_pos_node_list.index(quoted_user_id)
                    G_pos.add_node(index_quoted_user)
            
                else:
                    index_quoted_user = G_pos_node_list.index(quoted_user_id)
                
                G_pos.add_edge(index_original_quoted_user, index_quoted_user, weight=polarity_qu)
                
    except:
        print ("Error: unable to fetch data")

    print("finish SELECT * FROM QUOTED_STATUS")

    #store the user index in G to database
    for pos_node in G_pos_node_list:
        sql_add_pos = """INSERT INTO USER_LIST_G_pos(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add_pos = (pos_node, G_pos_node_list.index(pos_node))
        try:
            cursor.execute(sql_add_pos, par_add_pos)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_G_pos rollback')
            db.rollback()
        
    print('finish INSERT INTO USER_LIST_G_pos')

    # Type stag.graph.Graph
    g_pos = stag.graph.from_networkx(G_pos)

    filename = "G_pos_graph.edgelist"
    stag.graphio.save_edgelist(g_pos, filename)
    return G_pos


def build_graph_G_SA():
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_G_SA")

    sql_creating_G = """CREATE TABLE USER_LIST_G_SA (
            User_Id CHAR(20),
            User_Index int)"""
    cursor.execute(sql_creating_G)

    print('finish CREATE TABLE USER_LIST_G_SA')

    #buid a undirected graph G
    G_SA = nx.Graph()

    #store the order of adding nodes
    G_SA_node_list = []

    sql_rep = "SELECT * FROM REPLY_STATUS"
    try:
        cursor.execute(sql_rep)
        results_rep = cursor.fetchall()
        for row_rep in results_rep:
            original_reply_user_id = row_rep[0]
            reply_user_id = row_rep[2]
            polarity_rep = row_rep[4]
        
            if original_reply_user_id != reply_user_id:
            
                if original_reply_user_id not in G_SA_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_SA_node_list.append(original_reply_user_id)
                    index_original_reply_user = G_SA_node_list.index(original_reply_user_id)
                    G_SA.add_node(index_original_reply_user)
            
                else: 
                    index_original_reply_user = G_SA_node_list.index(original_reply_user_id)
            
            
                if reply_user_id not in G_SA_node_list:
                    G_SA_node_list.append(reply_user_id)
                    index_reply_user = G_SA_node_list.index(reply_user_id)
                    G_SA.add_node(index_reply_user)
            
                else:
                    index_reply_user = G_SA_node_list.index(reply_user_id)
            
            
                G_SA.add_edge(index_original_reply_user, index_reply_user, weight=polarity_rep)
                
    except:
        print ("Error: unable to fetch data")

    print('finish SELECT * FROM REPLY_STATUS')


    sql_qu = "SELECT * FROM QUOTED_STATUS"
    try:
        cursor.execute(sql_qu)
        results_qu = cursor.fetchall()
        for row_qu in results_qu:
            original_quoted_user_id = row_qu[0]
            quoted_user_id = row_qu[2]
            polarity_qu = row_qu[4]
        
            if original_quoted_user_id != quoted_user_id:
            
                if original_quoted_user_id not in G_SA_node_list:
                    #use the index of users_list as the node name (shorter and safer)
                    G_SA_node_list.append(original_quoted_user_id)
                    index_original_quoted_user = G_SA_node_list.index(original_quoted_user_id)
                    G_SA.add_node(index_original_quoted_user)
            
                else: 
                    index_original_quoted_user = G_SA_node_list.index(original_quoted_user_id)
            
            
                if quoted_user_id not in G_SA_node_list:
                    G_SA_node_list.append(quoted_user_id)
                    index_quoted_user = G_SA_node_list.index(quoted_user_id)
                    G_SA.add_node(index_quoted_user)
            
                else:
                    index_quoted_user = G_SA_node_list.index(quoted_user_id)
                
                G_SA.add_edge(index_original_quoted_user, index_quoted_user, weight=polarity_qu)
                
    except:
        print ("Error: unable to fetch data")

    print("finish SELECT * FROM QUOTED_STATUS")

    #store the user index in G to database
    for node_SA in G_SA_node_list:
        sql_add_SA = """INSERT INTO USER_LIST_G_SA(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add_SA = (node_SA, G_SA_node_list.index(node_SA))
        try:
            cursor.execute(sql_add_SA, par_add_SA)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_G_SA rollback')
            db.rollback()
        
    print('finish INSERT INTO USER_LIST_G_SA')

    # Type stag.graph.Graph
    g_SA = stag.graph.from_networkx(G_SA)

    filename = "G_SA_graph.edgelist"
    stag.graphio.save_edgelist(g_SA, filename)
    return G_SA


def build_graph_H(G):
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_H")

    sql_creating_H = """CREATE TABLE USER_LIST_H (
                     User_Id CHAR(20),
                     User_Index int)"""
    cursor.execute(sql_creating_H)
    print('finish CREATE TABLE USER_LIST_H')
    
    H_node_list = []
    #buid a undirected graph H
    H = nx.Graph()

    for node in list(G.nodes):
        H.add_node('a'+str(node))
        H_node_list.append('a'+str(node))
        H.add_node('b'+str(node))
        H_node_list.append('b'+str(node))
    
    for n,nbrs in G.adjacency(): 
        for nbr,attr in nbrs.items():
            if nbr not in list(H.adj['a'+str(n)]):
                weight = attr.get('weight')
                if n != nbr:
                    if weight > 0:
                        H.add_edge('a'+str(n), 'a'+str(nbr), weight=weight)
                        H.add_edge('b'+str(n), 'b'+str(nbr), weight=weight)
                    else:
                        H.add_edge('a'+str(n), 'b'+str(nbr), weight=abs(weight))
                        H.add_edge('a'+str(nbr), 'b'+str(n), weight=abs(weight))
                        
    #store the user index in G to database
    for node in H_node_list:
        sql_add = """INSERT INTO USER_LIST_H(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add = (node, H_node_list.index(node))
        try:
            cursor.execute(sql_add, par_add)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_H rollback')
            db.rollback()
    print('finish INSERT INTO USER_LIST_H')
    
    # Type stag.graph.Graph
    h = stag.graph.from_networkx(H)

    filename = "H_graph.edgelist"
    stag.graphio.save_edgelist(h, filename)
    return H


def build_graph_H_neg(G_neg):
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_H_neg")

    sql_creating_H = """CREATE TABLE USER_LIST_H_neg (
                     User_Id CHAR(20),
                     User_Index int)"""
    cursor.execute(sql_creating_H)
    print('finish CREATE TABLE USER_LIST_H_neg')
    
    H_neg_node_list = []
    #buid a undirected graph H
    H_neg = nx.Graph()

    for node in list(G_neg.nodes):
        H_neg.add_node('a'+str(node))
        H_neg_node_list.append('a'+str(node))
        H_neg.add_node('b'+str(node))
        H_neg_node_list.append('b'+str(node))
    
    for n,nbrs in G_neg.adjacency(): 
        for nbr,attr in nbrs.items():
            if nbr not in list(H_neg.adj['a'+str(n)]):
                weight = attr.get('weight')
                if n != nbr:
                    H_neg.add_edge('a'+str(n), 'b'+str(nbr), weight=weight)
                    H_neg.add_edge('a'+str(nbr), 'b'+str(n), weight=weight)
                        
    #store the user index in G to database
    for node in H_neg_node_list:
        sql_add = """INSERT INTO USER_LIST_H_neg(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add = (node, H_neg_node_list.index(node))
        try:
            cursor.execute(sql_add, par_add)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_H_neg rollback')
            db.rollback()
    print('finish INSERT INTO USER_LIST_H_neg')
    
    # Type stag.graph.Graph
    h_neg = stag.graph.from_networkx(H_neg)

    filename = "H_neg_graph.edgelist"
    stag.graphio.save_edgelist(h_neg, filename)
    return H_neg


def build_graph_H_SA(G_SA):
    cursor.execute("DROP TABLE IF EXISTS USER_LIST_H_SA")
    
    print("DROP TABLE IF EXISTS USER_LIST_H_SA")

    sql_creating_H = """CREATE TABLE USER_LIST_H_SA (
                     User_Id CHAR(20),
                     User_Index int)"""
    cursor.execute(sql_creating_H)
    print('finish CREATE TABLE USER_LIST_H_SA')
    
    H_SA_node_list = []
    #buid a undirected graph H
    H_SA = nx.Graph()

    for node in list(G_SA.nodes):
        H_SA.add_node('a'+str(node))
        H_SA_node_list.append('a'+str(node))
        H_SA.add_node('b'+str(node))
        H_SA_node_list.append('b'+str(node))
    
    for n,nbrs in G_SA.adjacency(): 
        for nbr,attr in nbrs.items():
            if nbr not in list(H_SA.adj['a'+str(n)]):
                weight = attr.get('weight')
                if n != nbr:
                    if weight > 0:
                        H_SA.add_edge('a'+str(n), 'a'+str(nbr), weight=weight)
                        H_SA.add_edge('b'+str(n), 'b'+str(nbr), weight=weight)
                    else:
                        H_SA.add_edge('a'+str(n), 'b'+str(nbr), weight=abs(weight))
                        H_SA.add_edge('a'+str(nbr), 'b'+str(n), weight=abs(weight))
                        
    #store the user index in G to database
    for node in H_SA_node_list:
        sql_add = """INSERT INTO USER_LIST_H_SA(User_Id, User_Index)
                   VALUES (%s,%s)""" 
        par_add = (node, H_SA_node_list.index(node))
        try:
            cursor.execute(sql_add, par_add)
            db.commit()
        except:
            print('INSERT INTO USER_LIST_H_SA rollback')
            db.rollback()
    print('finish INSERT INTO USER_LIST_H_SA')
    
    # Type stag.graph.Graph
    h_SA = stag.graph.from_networkx(H_SA)

    filename = "H_SA_graph.edgelist"
    stag.graphio.save_edgelist(h_SA, filename)
    return H_SA
