# Signed_Graph_Clustering_for_Social_Media_Analysis

To connect MySql Database Remotely, I have provided basic arguments that the pymysql.connect() method needs, it should be fine when building the connection in Python. If you have any questions, please contact me. 

In the main branch of this GitHub link, ACL_Algorithm, LocBipartDC_Algorithm, and LocSigned2L_Algorithm are the basic versions of these three algorithms. Given a seed user ID, they return one or two clusters of users and the corresponding fitness measure for this result. 

Pre-processing_Dataset.py illustrates the process of analysing and storing our Twitter dataset in the Database. Notice that the dataset we used in our experiments is not included in this link considering the privacy of our dataset.

Graph_builder.py shows the process of building graphs and how to store their edge information with the STAG library in Python. All resulting edge results are stored in the folder Graphs.

Other folders and ground_truth.py in the main branch correspond to all of the evaluations in our experiments, respectively. And running main.py in each folder can directly implement this evaluation. Notice that all the edge information of the involved graphs in each evaluation is summarised in the corresponding Graphs folders. This means that in all evaluations, we do not need to implement the graph construction again, and the edge information of the graphs is loaded by the STAG library. 
