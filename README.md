SDH: TVM
===

This repository contains:

- A Docker container setup that packages TVM, PyTorch and other deep learning frameworks (in `docker/`), and instructions on how to use it (in this `README`). 

- A tool to estimate energy consumption of TVM programs (in `energy-tool/`)

Docker
---

We have packaged TVM and PyTorch into a single Docker container. The Dockerfile used to generate the container image can be found in `docker/`. 

You can directly execute our Docker image by pulling it from Docker Hub:

```
$ ./docker/bash.sh mutinifni/sdh-tvm-pytorch:both
```
Note: You might need root permissions based on your local Docker setup.

Below is an example program run using TVM on the Docker container:

```
root@sdh-tvm-pytorch:~# python3
Python 3.5.2 (default, Nov 12 2018, 13:43:14)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tvm
>>> n = tvm.var("n")
>>> A = tvm.placeholder((n,), name='A')
>>> B = tvm.placeholder((n,), name='B')
>>> C = tvm.compute(A.shape, lambda i: A[i] + B[i], name="C")
>>> print(type(C))
<class 'tvm.tensor.Tensor'>
>>>
```

We can also run PyTorch examples on the container as shown below:

```
root@sdh-tvm-pytorch:~# python3
Python 3.5.2 (default, Nov 12 2018, 13:43:14)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from __future__ import print_function
>>> import torch
>>> x = torch.rand(5, 3)
>>> print(x)
tensor([[0.8631, 0.1452, 0.4480],
        [0.2124, 0.6833, 0.6346],
        [0.9590, 0.0705, 0.0502],
        [0.3226, 0.2670, 0.3571],
        [0.7307, 0.6423, 0.3341]])
>>>
```

You can find additional TVM Docker images (including GPU support) at:
[https://github.com/dmlc/tvm/tree/master/docker](https://github.com/dmlc/tvm/tree/master/docker), and related instructions at: [https://docs.tvm.ai/install/docker.html](https://docs.tvm.ai/install/docker.html).

Profiling
---

We recommend that testers use the PyTorch frontend for development.
Then, to profile an implementation you've created, we recommend you use TVM.
To do so, you will need to export the PyTorch model as [ONNX][] and import into TVM.
Follow these steps:

1. Export the model. Use [torch.onnx.export](https://pytorch.org/docs/master/onnx.html) to save your model to an ONNX file.
2. Import the model into TVM and compile. See [the TVM tutorial about importing ONNX models](https://docs.tvm.ai/tutorials/frontend/from_onnx.html#sphx-glr-tutorials-frontend-from-onnx-py).

[onnx]: https://onnx.ai

TVM Tutorials
---

You can use the Docker image to try out TVM's extensive tutorials available at: [https://docs.tvm.ai/tutorials/index.html](https://docs.tvm.ai/tutorials/index.html).

