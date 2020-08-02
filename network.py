import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns

def partition_by_degree(g, n) :
    greater_than_n = []
    less_eql_n = []
    for node in g.nodes() :
        if g.degree(node) > n :
            greater_than_n.append(node)
        else :
            less_eql_n.append(node)
    return network.subgraph(greater_than_n), network.subgraph(less_eql_n)

def mean_degree(g):
    degree_list = [d for n, d in g.degree()]
    return np.mean(degree_list)

def parse_file(file) :
    proteins_w_domains = {}
    with open(file, 'r') as f :
        header = f.readline().strip()
        for line in f:
            columns = line.strip().split("\t")
            if len(columns) == 2:
                (PfamID, proteinID) = columns
                if proteinID in proteins_w_domains :
                    proteins_w_domains[proteinID] += PfamID
                else:
                    proteins_w_domains[proteinID] = PfamID
            else:
                proteinID = columns[0]
                proteins_w_domains[proteinID] = []
    return proteins_w_domains

def count_domains_per_proteinID() :
    counts = {}
    proteins_w_domains = parse_file("downloads/proteins_w_domains.txt")
    for proteinID in proteins_w_domains:
        if type(proteins_w_domains[proteinID]) == int:
            counts[proteinID] = 1
        else:
            counts[proteinID] = len(proteins_w_domains[proteinID])
    return counts

def count_domains_per_node(graph) :
    partitioned_domain_counts = []
    for node in graph :
        proteinID = node.replace('9606.','')
        if proteinID in domain_counts:
            partitioned_domain_counts.append(domain_counts[proteinID])
    return partitioned_domain_counts

#create a graph
protein_links = pd.read_csv('downloads/9606.protein.links.v11.0.txt', sep = ' ', header = 0)
significant_protein_links = protein_links[protein_links['combined_score'] >= 500]
network = nx.from_pandas_edgelist(significant_protein_links, source = "protein1", target = "protein2", edge_attr = "combined_score")

#partition by degree
(subgraph_greater_100, subgraph_less_100) = partition_by_degree(network, 100)
print("partition_degree_mean_more: ", mean_degree(subgraph_greater_100))
print("partition_degree_mean_less: ", mean_degree(subgraph_less_100))

#count domains
domain_counts = count_domains_per_proteinID()
greater = count_domains_per_node(subgraph_greater_100)
print("partition_domain_counts_mean_more: ", np.mean(greater))
less = count_domains_per_node(subgraph_less_100)
print("partition_domain_counts_mean_less: ", np.mean(less))

#store the counts
df_1 = pd.DataFrame(greater, columns = ['#domain']).assign(label = 'degree > 100')
df_2 = pd.DataFrame(less, columns = ['#domain']).assign(label = 'degree <= 100')
df = pd.concat([df_1, df_2])

#plot
plot = sns.boxplot(x = "label", y = "#domain", data = df, showfliers = False, notch = True, showmeans=True)
figure = plot.get_figure()
figure.savefig("protein_domains_vs_string_degree.png")
print("Plot generated!")
