from scipy.sparse import csr_matrix
from scipy.sparse import csgraph
import graphit_util
import os

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
    # The SciPy graph algorithms, like GraphIt functions, want graphs
    # represented as SciPy's `csr_matrix` values. Use `csr_matrix` to
    # convert an adjacency matrix to the right format.
    mat = csr_matrix(graph)

    # Compute the all-paths distance matrix and pull out the row we're
    # interested in.
    dists = csgraph.shortest_path(mat)
    return dists[source]


def sssp_graphit(graph, source):
    """Use our GraphIt example implementation to compute the shortest
    paths vector for a given source vector index.
    """
    # Compile a GraphIt source file and load it so we can call its
    # exported function.
    sssp_module = graphit_util.load_cached(SSSP_SOURCE)

    # In GraphIt, `edgeset`s define graphs. Use SciPy's `csr_matrix` to
    # create these values, which we'll pass into a GraphIt function.
    mat = csr_matrix(graph)

    # Invoke the `do_sssp` GraphIt function from the loaded module.
    return sssp_module.do_sssp(mat, 1)


def compare():
    # Run both shortest-path algorithms.
    dists_a = sssp_scipy(MY_GRAPH, 1)
    dists_b = sssp_graphit(MY_GRAPH, 1)

    # Check that the results agree.
    assert all(a == b for a, b in zip(dists_a, dists_b))


if __name__ == '__main__':
    compare()
