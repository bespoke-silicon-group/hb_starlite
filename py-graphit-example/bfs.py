import graphit
from scipy.sparse import csr_matrix


bfs_module = graphit.compile_and_load("bfs.gt")
graph = csr_matrix((
    [4, 5, 6, 4, 5, 6],
    [1, 2, 3, 0, 0, 0],
    [0, 3, 4, 5, 6],
))
bfs_module.do_bfs(graph, 1)
