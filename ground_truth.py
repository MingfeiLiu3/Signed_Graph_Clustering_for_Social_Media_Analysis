
import stag.graphio
import stag.graph
import stag.cluster

import pymysql
import scipy.sparse
from random import sample



def load_G_vertex_dictionaries():
    # Construct and return the dictionaries of user ids to node index.
    vertex_to_user = {}
    user_to_vertex = {}

    sql_list = "SELECT * FROM USER_LIST_G"
    try:
        cursor.execute(sql_list)
        results_list = cursor.fetchall()
        for row_list in results_list:
            User_Id = row_list[0]
            User_Index = row_list[1]
            vertex_to_user[User_Index] = User_Id
            user_to_vertex[User_Id] = User_Index
    except:
        raise Exception("Error: unable to fetch data")
    return user_to_vertex, vertex_to_user


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


def signed_2_lift_clustering(seed_user):

    h = stag.graphio.load_edgelist('./Graphs/H_graph.edgelist')
    g = stag.graphio.load_edgelist('./Graphs/G_graph.edgelist')

    # Load dictionaries mapping between graph nodes and user ids
    user_to_vertex, vertex_to_user = load_G_vertex_dictionaries()


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
    size_factor = 0.7       #A number from 0 to 1 indicating how 'local' the cluster should be
    epsilon = 6.989e-4
    seed_vector = scipy.sparse.lil_matrix((h.number_of_vertices(), 1))    #construct an empty matrix with shape (M, N)
    seed_vector[starting_vertex, 0] = 1
    p, r = stag.cluster.approximate_pagerank(h, seed_vector.tocsc(), alpha, epsilon)

    # Compute the simplified pagerank vector
    p_simplified = simplify(g.number_of_vertices(), p)

    # Compute the sweep set in the double cover
    sweep_set = stag.cluster.sweep_set_conductance(h, p_simplified)

    # Split the returned vertices into those in the same cluster as the seed, and others.
    this_cluster = [vertex_to_user.get(i) for i in sweep_set if i < g.number_of_vertices()]
    that_cluster = [vertex_to_user.get(i - g.number_of_vertices()) for i in sweep_set if i >= g.number_of_vertices()]
    #print(this_cluster, that_cluster)

    #computing the conductance of the resulting cluster
    #print('The conductance of the signed 2-lift clustering algorithm: '+ str(stag.cluster.conductance(h, sweep_set)))
    return this_cluster, that_cluster


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()

ran_user_list = []
sql_list = "SELECT * FROM USER_LIST_G"
try:
    cursor.execute(sql_list)
    results_list = cursor.fetchall()
    for row_list in results_list:
        user_id = row_list[0]
        ran_user_list.append(user_id)
except:
    raise Exception("Error: unable to fetch data")

sample = sample(ran_user_list, 2000)


for s in sample:
    this_cluster, that_cluster = signed_2_lift_clustering(s)

    cluster_label = []
    ground_cluser_label = []

    for this_user in this_cluster:
        sql_user_label = "SELECT Label FROM USER_LIST_G \
                        WHERE User_Id = %s" % (this_user)
        cursor.execute(sql_user_label)
        results_label = cursor.fetchall()
        if results_label[0][0] != '':
            print(this_user, results_label[0][0])
            this_label = results_label[0][0]
            ground_cluser_label.append(0)
            if this_label == 'Remain':
                cluster_label.append(1)
            else:
                cluster_label.append(0)
        
        
    for that_user in that_cluster:
        sql_user_label = "SELECT Label FROM USER_LIST_G \
                        WHERE User_Id = %s" % (that_user)
        cursor.execute(sql_user_label)
        results_label = cursor.fetchall()
        if results_label[0][0] != '':
            print(that_user, results_label[0][0])
            that_label = results_label[0][0]
            ground_cluser_label.append(1)
            if that_label == 'Remain':
                cluster_label.append(1)
            else:
                cluster_label.append(0)
            
    #print(len(this_cluster), len(that_cluster))
    #print(cluster_label)
    #print(ground_cluser_label)
    print(stag.cluster.adjusted_rand_index(ground_cluser_label, cluster_label))

        

