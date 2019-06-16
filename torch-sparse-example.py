"""Some useful utilities for working with sparse tensors using the
`torch.sparse` library.
"""
import torch.sparse
import torch_sparse
import scipy.sparse
import numpy


def sparse_scipy2torch(matrix):
    """Convert a matrix from *any* `scipy.sparse` representation to a
    sparse `torch.tensor` value.
    """
    coo_matrix = matrix.tocoo()
    return torch.sparse.FloatTensor(
        torch.LongTensor(numpy.vstack((coo_matrix.row, coo_matrix.col))),
        torch.FloatTensor(coo_matrix.data),
        torch.Size(coo_matrix.shape),
    )


def sparse_torch2scipy(tensor):
    """Convert a sparse `torch.tensor` matrix (which must be
    two-dimensional, i.e., a matrix) to a `scipy.sparse` matrix. The
    result uses the COO representation, but you can convert it to any
    other sparse representation you need.
    """
    coalesced = tensor.coalesce()
    values = coalesced.values()
    rows, cols = coalesced.indices()
    return scipy.sparse.coo_matrix((
        values.numpy(),
        (rows.numpy(), cols.numpy()),
    ))


def sparse_sparse_mm(a, b):
    """Sparse/sparse matrix multiply for `torch.sparse` tensors.
    Requires the supplemental `torch_sparse` library.
    """
    assert a.shape[1] == b.shape[0], "dimension mismatch for multiply"
    a_coalesced = a.coalesce()
    b_coalesced = b.coalesce()
    c_indices, c_values = torch_sparse.spspmm(
        a_coalesced.indices(), a_coalesced.values(),
        b_coalesced.indices(), b_coalesced.values(),
        a.shape[0], a.shape[1], b.shape[1],
    )
    return torch.sparse.FloatTensor(
        c_indices,
        c_values,
        torch.Size([a.shape[0], b.shape[1]]),
    )
