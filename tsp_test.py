import networkx as nx
import random
import matplotlib.pyplot as plt
import neal
import dwave_networkx as dnx

# Create a graph for the TSP
G = nx.Graph()

# Define the number of cities
num_cities = 10

# Generate random city coordinates
city_coordinates = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(num_cities)}

# Add cities as nodes with their coordinates
G.add_nodes_from(city_coordinates)

# Calculate distances (Euclidean distance) and add edges
for node1 in G.nodes():
    for node2 in G.nodes():
        if node1 != node2:
            distance = ((city_coordinates[node1][0] - city_coordinates[node2][0]) ** 2 +
                        (city_coordinates[node1][1] - city_coordinates[node2][1]) ** 2) ** 0.5
            G.add_edge(node1, node2, weight=distance)

# Solve the TSP using Simulated Annealing
sampler = neal.SimulatedAnnealingSampler()
tsp_solution = dnx.traveling_salesperson(G, sampler, num_reads=50)

# Extract the optimized TSP tour
optimal_tour = list(tsp_solution)

# Create a list of edges in the optimal tour
optimal_tour_edges = [(optimal_tour[i], optimal_tour[i + 1]) for i in range(len(optimal_tour) - 1)]
optimal_tour_edges.append((optimal_tour[-1], optimal_tour[0]))

# Create a plot to visualize the optimized TSP tour
pos = city_coordinates
plt.figure(figsize=(8, 6))
# nx.draw(G, pos, node_size=20, with_labels=True)

# Draw the optimized route (TSP tour)
nx.draw_networkx_edges(G, pos, edgelist=optimal_tour_edges, edge_color='b', width=2)

plt.title("Optimized TSP Tour for 10 Randomly Generated Cities")
plt.show()
