from matplotlib import pyplot as plt
import numpy as np

import LocBipartDC_line
import LocSigned2L_line
import pymysql


db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'Vision33',
    db = 'mysql')
 
cursor = db.cursor()

fig = plt.figure()
axes = fig.add_axes([0.1,0.1,0.8,0.8])

seed_user = 623199094
# conductance_1: 623199094
# conductnace_2: 1103393913988096000
x = np.linspace(6.989e-4, 6.989e-2,500)

y_2L = []
y_DC = []
for e in x:
    a_2L = LocSigned2L_line.LocSigned2L_clustering(seed_user,e)
    a_DC = LocBipartDC_line.LocBipartDC_clustering(seed_user,e)
    y_2L.append(a_2L)
    y_DC.append(a_DC)
    

plt.plot(x,y_2L,c='green',label='conductance of LocSigned2L')
plt.plot(x,y_DC,c='blue',label='conductance of LocBipartDC')
plt.title('Conductance of Two Algorithms')
plt.xlabel('epsilon')
plt.ylabel('conductance')

plt.legend()
plt.show()