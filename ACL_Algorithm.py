import stag.graphio
import stag.graph
import stag.cluster

import pymysql

import scipy.sparse

import Graph_builder

# 打开数据库连接
db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

def load_pos_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_pos = {}
    user_to_vertex_pos = {}

    # SQL 查询语句
    sql_list = "SELECT * FROM USER_LIST_G_pos"
    try:
        # 执行SQL语句
        cursor.execute(sql_list)
        # 获取所有记录列表
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_pos[User_Index] = User_Id
            user_to_vertex_pos[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_pos, vertex_to_user_pos


# Load the positive edges information 
g_pos = stag.graphio.load_edgelist('G_pos_graph.edgelist')

# Load dictionaries mapping between graph nodes and user ids
user_to_vertex_pos, vertex_to_user_pos = load_pos_vertex_dictionaries()


# Get the starting vertex of the algorithm
seed_user = 34247411   # For example

# Check whether this seed user is a vertex in graph G_pos
sql_starting = "SELECT User_Index FROM USER_LIST_G_pos \
                WHERE User_Id = %s" % (seed_user)
try:
    cursor.execute(sql_starting)
    results_starting = cursor.fetchall()
    if results_starting == ():
        print("Seed Twitter user not found in dataset.")
    else:
        starting_vertex = results_starting[0][0]
        print('seed_user: '+ str(seed_user), 'starting_vertex: '+ str(starting_vertex))
except:
    raise Exception("Error: unable to fetch data")

    
# Run the approximate pagerank on the graph G_pos
alpha = 0.01
epsilon = 9.4798e-4   # For example
size_factor = 0.7
seed_vector = scipy.sparse.lil_matrix((g_pos.number_of_vertices(), 1))
seed_vector[starting_vertex, 0] = 1
p, r = stag.cluster.approximate_pagerank(g_pos, seed_vector.tocsc(), alpha, epsilon)

# Compute the sweep set in the graph G_pos
sweep_set = stag.cluster.sweep_set_conductance(g_pos, p)

cluster = [vertex_to_user_pos[i] for i in sweep_set if i < g_pos.number_of_vertices()]
print(cluster)

#computing the conductance of the resulting cluster
stag.cluster.conductance(g_pos, sweep_set)
