import matplotlib.pyplot as plt
import networkx as nx
import H_Pos as hp

G=nx.Graph()
G.add_edges_from([(1,2),(1,3),(1,4),(2,5),(2,6)])
pos = hp.hierarchy_pos(G,1)
nx.draw(G, pos, with_labels=False)
plt.show()