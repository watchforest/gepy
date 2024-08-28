import networkx as nx

path = "assets/network/random_graph_100_nodes.gexf"

# Read the graph and compute the communities
g = nx.read_gexf(path)
communities_generator = nx.community.greedy_modularity_communities(g)

# Create an inverted dictionary directly
inverted_dict = {
    int(node): i
    for i, community in enumerate(communities_generator)
    for node in community
}

print(inverted_dict[0])