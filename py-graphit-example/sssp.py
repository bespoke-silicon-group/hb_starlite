import graphit
from scipy.sparse import csr_matrix


sssp_module = graphit.compile_and_load("sssp.gt")
graph = csr_matrix((
    [4, 5, 6, 4, 5, 6],
    [1, 2, 3, 0, 0, 0],
    [0, 3, 4, 5, 6],
))
distances = sssp_module.do_sssp(graph)
print(distances)
