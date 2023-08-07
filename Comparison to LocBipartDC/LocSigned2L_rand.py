import networkx as nx

import stag.graphio
import stag.graph
import stag.cluster

import pymysql

import scipy.sparse

import Graph_builder


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()


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


def LocSigned2L_clustering(seed_user):

    h = stag.graphio.load_edgelist('./Graphs/H_graph.edgelist')
    g = stag.graphio.load_edgelist('./Graphs/G_graph.edgelist')


    # Get the starting vertex of the algorithm
    sql_starting = "SELECT User_Index FROM USER_LIST_G \
                WHERE User_Id = %s" % (seed_user)
    try:
        cursor.execute(sql_starting)
        results_starting = cursor.fetchall()
        if results_starting == ():
            print("Seed Twitter user not found in G dataset.")
        else:
            starting_vertex = results_starting[0][0]
            print('seed_user: '+str(seed_user)+ ', ' + 'starting vertex: '+ str(starting_vertex))
    except:
        raise Exception("Error: unable to fetch data")


    # Run the approximate pagerank on the double cover graph
    alpha = 0.01
    size_factor = 0.7
    epsilon = 9.4798e-3   # For example       
    seed_vector = scipy.sparse.lil_matrix((h.number_of_vertices(), 1))    #construct an empty matrix with shape (M, N)
    seed_vector[starting_vertex, 0] = 1
    p, r = stag.cluster.approximate_pagerank(h, seed_vector.tocsc(), alpha, epsilon)

    # Compute the simplified pagerank vector
    p_simplified = simplify(g.number_of_vertices(), p)

    # Compute the sweep set in the double cover
    sweep_set = stag.cluster.sweep_set_conductance(h, p_simplified)

    # Split the returned vertices into those in the same cluster as the seed, and others.
    #this_cluster = [vertex_to_user.get(i) for i in sweep_set if i < g.number_of_vertices()]
    #that_cluster = [vertex_to_user.get(i - g.number_of_vertices()) for i in sweep_set if i >= g.number_of_vertices()]
    #print(this_cluster, that_cluster)
    
    return sweep_set, stag.cluster.conductance(h, sweep_set)