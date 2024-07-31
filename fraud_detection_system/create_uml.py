import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes for data sources
G.add_node('User Input Data')
G.add_node('System-Generated Data')
G.add_node('Internal Databases')
G.add_node('Third-Party Data')

# Add node for data processing
G.add_node('Data Processing')

# Add nodes for output
G.add_node('Processed Data')
G.add_node('End Users')

# Add edges representing the flow of data
G.add_edge('User Input Data', 'Data Processing')
G.add_edge('System-Generated Data', 'Data Processing')
G.add_edge('Internal Databases', 'Data Processing')
G.add_edge('Third-Party Data', 'Data Processing')
G.add_edge('Data Processing', 'Processed Data')
G.add_edge('Processed Data', 'End Users')

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')

# Show the plot
plt.show()
