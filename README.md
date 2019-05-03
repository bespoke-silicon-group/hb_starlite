Starlite: A Programmability Testing Environment for HammerBlade
===============================================================

This repository contains a setup for evaluating the programming infrastructure for the HammerBlade project.
The main component is a [Docker][] container setup that includes [TVM][], [PyTorch][], and [GraphIt][].
There are also tools for estimating the energy consumption of programs implemented using this infrastructure.

[tvm]: https://tvm.ai
[pytorch]: https://pytorch.org
[graphit]: http://graphit-lang.org
[docker]: https://www.docker.com


Running the Container
---------------------

To run the container, use our launch script to pull it from [Docker Hub][hub]:

    $ ./docker/bash.sh mutinifni/sdh-tvm-pytorch:both

You might need root permissions based on your local Docker setup (so try this with `sudo` if it doesn't work without it).

[hub]: https://hub.docker.com
[dockerfile]: https://github.com/Mutinifni/hb_starlite/blob/master/docker/Dockerfile

You can also see the [Dockerfile][] source for details on how this is set up.
For other (standard) containers for TVM (including GPU support), see
[the official Dockerfiles](https://github.com/dmlc/tvm/tree/master/docker), and [related instructions](https://docs.tvm.ai/install/docker.html).


Development
-----------

Inside the container, you can use [PyTorch][], [TVM][], and [GraphIt][].

### PyTorch

For machine learning and dense linear algebra development, we recommend you use [PyTorch][].
To get started, begin with [the "60-minute blitz" PyTorch tutorial](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html).
Then, depending on the task you want to accomplish, explore [the full set of PyTorch tutorials](https://pytorch.org/tutorials/) to find examples that are closest to your domain.

### TVM

You can also opt to use [TVM][] directly, especially via its [MXNet][] frontend.
See the extensive list of [tutorials that come with TVM][tvm-tut].

[tvm-tut]: https://docs.tvm.ai/tutorials/
[mxnet]: https://mxnet.apache.org

### GraphIt

To develop graph processing kernels, use [GraphIt][].
Begin by following the [Getting Started guide](http://graphit-lang.org/getting-started), which walks you through the implementation of the PageRank-Delta algorithm.
(You can skip the initial setup instructions; the compiler is already installed in the container for you.)
Then, check out the [language manual](http://graphit-lang.org/language) for more details.


Profiling
---------

We recommend that testers use the PyTorch frontend for development.
Then, to profile an implementation you've created, we recommend you use TVM.
To do so, you will need to export the PyTorch model as [ONNX][] and import into TVM.
Follow these steps:

1. Export the model. Use [torch.onnx.export](https://pytorch.org/docs/master/onnx.html) to save your model to an ONNX file.
2. Import the model into TVM and compile. See [the TVM tutorial about importing ONNX models](https://docs.tvm.ai/tutorials/frontend/from_onnx.html#sphx-glr-tutorials-frontend-from-onnx-py).

[onnx]: https://onnx.ai
