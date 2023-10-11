import networkx as nx
from dwave.system import LeapHybridSampler
import matplotlib.pyplot as plt
import neal
import dwave_networkx as dnx

# Create a graph
G = nx.Graph()

# Read the TSP data from the file
with open("example/berlin52.tsp", "r") as tsp_file:
    lines = tsp_file.readlines()

node_coord_section = False
for line in lines:
    if "NODE_COORD_SECTION" in line:
        node_coord_section = True
    elif node_coord_section:
        if "EOF" in line:
            break
        parts = line.split()
        node = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        G.add_node(node, pos=(x, y))

# Calculate distances (Euclidean distance) and add edges
for node1 in G.nodes():
    for node2 in G.nodes():
        if node1 != node2:
            distance = ((G.nodes[node1]["pos"][0] - G.nodes[node2]["pos"][0]) ** 2 +
                        (G.nodes[node1]["pos"][1] - G.nodes[node2]["pos"][1]) ** 2) ** 0.5
            G.add_edge(node1, node2, weight=distance)

# Solve the TSP using Simulated Annealing
sampler = neal.SimulatedAnnealingSampler()
tsp_solution = dnx.traveling_salesperson(G, sampler, num_reads=10)

# Extract the optimal TSP tour
optimal_tour = list(tsp_solution)

# Create a plot to visualize the tour
pos = nx.get_node_attributes(G, "pos")
tour_edges = [(optimal_tour[i], optimal_tour[i + 1]) for i in range(len(optimal_tour) - 1)]
tour_edges.append((optimal_tour[-1], optimal_tour[0]))

plt.figure(figsize=(8, 6))
# nx.draw(G, pos, node_size=20)
nx.draw_networkx_edges(G, pos, edgelist=tour_edges, edge_color='b', width=2)
plt.title("Optimal TSP Tour")
plt.show()

