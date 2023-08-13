# Signed_Graph_Clustering_for_Social_Media_Analysis

To connect MySql Database Remotely, I have provided basic arguments that the connect() method needs, it should be fine when building the connection in Python. If you have any questions, please contact me. 

In the main branch of the GitHub link, ACL_Algorithm, LocBipartDC_Algorithm, and LocSigned2L_Algorithm are the basic versions of these three algorithms. Given a seed user ID, they return one or two clusters of users and the corresponding fitness measure for this result. Pre-processing_Dataset.py illustrates the process of analysing and storing our Twitter dataset in the Database. And Graph_builder.py shows the process of building graphs and how to store their edge information with the STAG library in Python. All resulting edge results are stored in the Graphs folder.  

Other folders in the main branch correspond to all of the evaluations in our experiments, respectively. And running the main.py in each folder can directly implement this evaluation. 
