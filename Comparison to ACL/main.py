
import stag.graphio
import stag.graph
import stag.cluster

import pymysql

import scipy.sparse
from random import sample

#import Graph_builder
import ACL
import LocSigned2L

db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()

def load_G_pos_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_G_pos = {}
    user_to_vertex_G_pos = {}

    sql_list = "SELECT * FROM USER_LIST_G_pos"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_G_pos[User_Index] = User_Id
            user_to_vertex_G_pos[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_G_pos, vertex_to_user_G_pos

pos_user_list = []
sql_list = "SELECT * FROM USER_LIST_G_pos"
try:
    cursor.execute(sql_list)
    results_list = cursor.fetchall()
    for row_list in results_list:
        user_id = row_list[0]
        pos_user_list.append(user_id)
except:
    raise Exception("Error: unable to fetch data")


g_pos = stag.graphio.load_edgelist('./Graphs/G_pos_graph.edgelist')
epsilon = 9.4798e-4

# Load dictionaries mapping between graph nodes and user ids
user_to_vertex_G_pos, vertex_to_user_G_pos = load_G_pos_vertex_dictionaries()


sample = sample(pos_user_list, 20)
for s in sample:

    cond_ACL = ACL.ACL_clusering(s,epsilon)
    print('The conductance in G_pos: '+str(cond_ACL))

    result_cluster = LocSigned2L.LocSigned2L_clustering(s,epsilon)
    
    if result_cluster != None:
        sweep_list_G_pos = []
        for user in result_cluster:
            if user_to_vertex_G_pos.get(user) != None:
                sweep_list_G_pos.append(user_to_vertex_G_pos.get(user))

        sweep_set_G_pos = tuple(sweep_list_G_pos)
        cond_2L = stag.cluster.conductance(g_pos, sweep_set_G_pos)
        print('The conductance of L/R in G_pos: '+str(cond_2L))
        print('\n')