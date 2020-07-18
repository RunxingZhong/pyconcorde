
from concorde.tsp import TSPSolver
import networkx as nx 
import matplotlib.pyplot as plt 
import os 
import tsplib95
from time import time

def plot(problem, tour):
    G = problem.get_graph()
    if len(problem.node_coords) == 0:
        coord = problem.display_data
    else:
        coord = {}
        for node in G.nodes:
            coord[node] = problem.node_coords[node]
    
    # remove original edges
    G.remove_edges_from(list(G.edges))
    plt.subplot(121)
    nx.draw_networkx_nodes(G, coord, node_size=15)

    # add edges
    edges = []
    for i in range(len(tour)-1):
        n1, n2 = tour[i], tour[i+1]
        edges.append((n1, n2))
    edges.append((tour[-1], tour[0]))
    G.add_edges_from(edges)
    plt.subplot(122)
    nx.draw_networkx(G, coord, node_size=15, with_labels=False)
    plt.show()

def get_example_path():
    path = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(path, "example_data")
    return datapath

def run(filename, is_plot=True):
    datapath = get_example_path()
    filepath = os.path.join(datapath, filename)
    problem = tsplib95.load(filepath)
    start = time()
    solver = TSPSolver.from_tspfile(filepath)
    solution = solver.solve()
    end = time()
    print("Time spent to solve {}s".format(end-start))
    print("Optimal value: ", solution.optimal_value)
    tour = solution.tour
    tour = [t+1 for t in tour]
    plot(problem, tour)

if __name__ == "__main__":
    run("pr2392.tsp")
