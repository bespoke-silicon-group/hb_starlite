from scipy.sparse import csr_matrix
from scipy.sparse import csgraph
from numpy import inf
import graphit_util
import os
import sys

# You can represent a graph as an *adjacency matrix*. The entry at
# (i, j) gives the edge weight for the edge from vertex i to vertex j.
# The adjacency matrix for an undirected graph is a symmetric matrix.
# In this example, the graph has 3 nodes. The 0<->1 edge has weight 2,
# the 0<->2 edge has weight 1, and the 1<->2 edge does not exist.
MY_GRAPH = [
    [0, 2, 1],
    [2, 0, 0],
    [1, 0, 0],
]

# The path to our GraphIt source file, relative to this Python file.
SSSP_SOURCE = os.path.join(os.path.dirname(__file__), 'sssp.gt')


def sssp_scipy(graph, source):
    """Use SciPy's built-in shortest path algorithm to compute a vector
    of shortest paths from the source matrix, given as an index.
    """
    # Compute the all-paths distance matrix and pull out the row we're
    # interested in.
    dists = csgraph.shortest_path(graph)
    return dists[source]


def sssp_graphit(graph, source):
    """Use our GraphIt example implementation to compute the shortest
    paths vector for a given source vector index.
    """
    # Compile a GraphIt source file and load it so we can call its
    # exported function.
    sssp_module = graphit_util.load_cached(SSSP_SOURCE)

    # Invoke the `do_sssp` GraphIt function from the loaded module. A
    # `csr_matrix` value, which represents a graph, gets translated to an
    # `edgelist` within the GraphIt code.
    return sssp_module.do_sssp(graph, source)


def compare(graph, source=2):
    # Run both shortest-path algorithms.
    dists_a = sssp_scipy(graph, source)
    dists_b = sssp_graphit(graph, source)

    # Check that the results agree.
    assert all(a == b or a == inf and b == 2147483647
               for a, b in zip(dists_a, dists_b))


def main():
    # Use our built-in graph, or load one from a file.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename) as f:
            graph = graphit_util.read_adjacency_tsv(f)
    else:
        graph = csr_matrix(MY_GRAPH)

    # Get the source matrix index.
    if len(sys.argv) > 2:
        source = int(sys.argv[2])
    else:
        source = 0

    compare(graph, source)


if __name__ == '__main__':
    main()
