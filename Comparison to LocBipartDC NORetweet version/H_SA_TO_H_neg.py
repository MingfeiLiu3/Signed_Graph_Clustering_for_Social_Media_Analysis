import stag.graphio
import stag.graph
import stag.cluster

import pymysql

import scipy.sparse


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()


def load_G_neg_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_G_neg = {}
    user_to_vertex_G_neg = {}

    sql_list = "SELECT * FROM USER_LIST_G_neg"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_G_neg[User_Index] = User_Id
            user_to_vertex_G_neg[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_G_neg, vertex_to_user_G_neg

def load_H_neg_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_H_neg = {}
    user_to_vertex_H_neg = {}

    sql_list = "SELECT * FROM USER_LIST_H_neg"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_H_neg[User_Index] = User_Id
            user_to_vertex_H_neg[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_H_neg, vertex_to_user_H_neg


def load_G_SA_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_G_SA = {}
    user_to_vertex_G_SA = {}

    sql_list = "SELECT * FROM USER_LIST_G_SA"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_G_SA[User_Index] = User_Id
            user_to_vertex_G_SA[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_G_SA, vertex_to_user_G_SA

def load_H_SA_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_H_SA = {}
    user_to_vertex_H_SA = {}

    sql_list = "SELECT * FROM USER_LIST_H_SA"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_H_SA[User_Index] = User_Id
            user_to_vertex_H_SA[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_H_SA, vertex_to_user_H_SA


def convert_H_SA_TO_H_neg(sweep_set):

    h_neg = stag.graphio.load_edgelist("./Graphs/H_neg_graph.edgelist")


    # Load dictionaries mapping between graph nodes and user ids
    user_to_vertex_G_neg, vertex_to_user_G_neg = load_G_neg_vertex_dictionaries()

    # Load dictionaries mapping between graph nodes and user ids
    user_to_vertex_H_neg, vertex_to_user_H_neg = load_H_neg_vertex_dictionaries()


    # Load dictionaries mapping between graph nodes and user ids
    user_to_vertex_G_SA, vertex_to_user_G_SA = load_G_SA_vertex_dictionaries()

    # Load dictionaries mapping between graph nodes and user ids
    user_to_vertex_H_SA, vertex_to_user_H_SA = load_H_SA_vertex_dictionaries()


    G_SA_id = []
    for sweep in sweep_set:
        sweep_ID = vertex_to_user_H_SA.get(sweep)

        if sweep_ID[0] == 'a':
            G_SA_user_ID = vertex_to_user_G_SA.get(int(sweep_ID[1:]))
            G_SA_id.append('a'+G_SA_user_ID)
        else:
            G_SA_user_ID = vertex_to_user_G_SA.get(int(sweep_ID[1:]))
            G_SA_id.append('b'+G_SA_user_ID)

    H_neg_ID = []
    H_neg_index = []
    for G_SA_node in G_SA_id:
        if G_SA_node[0] == 'a':
            if user_to_vertex_G_neg.get(G_SA_node[1:]) != None:
                H_neg_node_ID = 'a'+str(user_to_vertex_G_neg.get(G_SA_node[1:]))
                H_neg_ID.append(H_neg_node_ID)
                H_neg_node_index = user_to_vertex_H_neg.get(H_neg_node_ID)
                H_neg_index.append(H_neg_node_index)
        else:
            if user_to_vertex_G_neg.get(G_SA_node[1:]) != None:
                H_neg_node_ID = 'b'+str(user_to_vertex_G_neg.get(G_SA_node[1:]))
                H_neg_ID.append(H_neg_node_ID)
                H_neg_node_index = user_to_vertex_H_neg.get(H_neg_node_ID)
                H_neg_index.append(H_neg_node_index)

    sweep_set_H_neg = tuple(H_neg_index)

    #computing the conductance of the resulting cluster
    return stag.cluster.conductance(h_neg, sweep_set_H_neg)