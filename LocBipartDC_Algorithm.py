import stag.graphio
import stag.graph
import stag.cluster

import pymysql

import scipy.sparse

#import Graph_builder


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()


def load_neg_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user_neg = {}
    user_to_vertex_neg = {}

    sql_list = "SELECT * FROM USER_LIST_G_neg"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user_neg[User_Index] = User_Id
            user_to_vertex_neg[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex_neg, vertex_to_user_neg


def simplify(num_g_vertices: int, sparse_vector):
    # Initialise the new sparse vector
    new_vector = scipy.sparse.lil_matrix((2 * num_g_vertices, 1))

    # Iterate through the entries in the matrix
    for i in range(min(num_g_vertices, sparse_vector.shape[0] - num_g_vertices)):
        if sparse_vector[i, 0] > sparse_vector[i + num_g_vertices, 0]:
            new_vector[i, 0] = sparse_vector[i, 0] - sparse_vector[i + num_g_vertices, 0]
        elif sparse_vector[i + num_g_vertices, 0] > sparse_vector[i, 0]:
            new_vector[i + num_g_vertices, 0] = sparse_vector[i + num_g_vertices, 0] - sparse_vector[i, 0]

    return new_vector.tocsc()



# Load the edges information of the graph G_neg the its double cover
g_neg = stag.graphio.load_edgelist('G_neg_graph.edgelist')
h_neg = stag.graphio.load_edgelist('H_neg_graph.edgelist')


# Load dictionaries mapping between graph nodes and user ids
user_to_vertex_neg, vertex_to_user_neg = load_neg_vertex_dictionaries()


# Get the starting vertex of the algorithm
seed_user = 1232386376244572161    # For example 

sql_starting = "SELECT User_Index FROM USER_LIST_G_neg \
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
        
    
# Run the approximate pagerank on the double cover graph
alpha = 0.01
epsilon = 9.4798e-4   # For example
size_factor = 0.7
seed_vector = scipy.sparse.lil_matrix((h_neg.number_of_vertices(), 1))
seed_vector[starting_vertex, 0] = 1
p, r = stag.cluster.approximate_pagerank(h_neg, seed_vector.tocsc(), alpha, epsilon)

# Compute the simplified pagerank vector
p_simplified = simplify(g_neg.number_of_vertices(), p)

# Compute the sweep set in the double cover
sweep_set = stag.cluster.sweep_set_conductance(h_neg, p_simplified)

# Split the returned vertices into those in the same cluster as the seed, and others.
this_cluster = [vertex_to_user_neg.get(i) for i in sweep_set if i < g_neg.number_of_vertices()]
that_cluster = [vertex_to_user_neg.get(i - g_neg.number_of_vertices()) for i in sweep_set if i >= g_neg.number_of_vertices()]
print(this_cluster, that_cluster)

#computing the conductance of the resulting cluster
stag.cluster.conductance(h_neg, sweep_set)