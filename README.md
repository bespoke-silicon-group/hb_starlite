Starlite: A Programmability Testing Environment for HammerBlade
===============================================================

This repository contains a setup for evaluating the programming infrastructure for the HammerBlade project.
HammerBlade is a custom architecture that is programmable using the domain specific languages **PyTorch**, and **GraphIt**. **PyTorch** is a popular prototyping language for ML computations, and **GraphIt** is an MIT-developed programming
language for developing and tuning graph computations. Our **PyTorch** tool flow maps down on to the **TVM** ML optimization
flow, which in itself is a ML-programming language. In some cases, it may be more convenient to use **TVM** directly.

To help users evaluate the usability of our programming interface, we have provided this repository, which contains
both domain specific languages, and also an energy profiling feature that allows users to get a "compass reading"
on how changes to their code affect energy efficiency.

To help deploy this toolchain, we have provided in this repository a **Docker** container setup that includes **PyTorch**, **GraphIt**, and tools for estimating the energy consumption of programs implemented using this infrastructure. Here
are the links to the component of this infrastructure so that you may get more information on them:

[*tvm*: https://tvm.ai ](https://tvm.ai)

[*pytorch*: https://pytorch.org ](https://pytorch.org)

[*graphit*: http://graphit-lang.org](http://graphit-lang.org)

[*docker*: https://www.docker.com](https://www.docker.com)


Running the Container
---------------------

To run the container, use our launch script to pull it from [Docker Hub][hub]:

    $ ./docker/bash.sh mutinifni/sdh-tvm-pytorch:latest

You might need root permissions based on your local Docker setup (so try this with `sudo` if it doesn't work without it).

[hub]: https://hub.docker.com
[dockerfile]: https://github.com/Mutinifni/hb_starlite/blob/master/docker/Dockerfile

You can also see the [Dockerfile][] source for details on how this is set up.
For other (standard) containers for TVM (including GPU support), see
[the official Dockerfiles](https://github.com/dmlc/tvm/tree/master/docker), and [related instructions](https://docs.tvm.ai/install/docker.html).


Development
-----------

Inside the container, you can use **PyTorch**, **TVM**, and **GraphIt**.

### PyTorch

For machine learning and dense linear algebra development, we recommend you use **PyTorch**.
To get started, begin with [the "60-minute blitz" PyTorch tutorial](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html).
Then, depending on the task you want to accomplish, explore [the full set of PyTorch tutorials](https://pytorch.org/tutorials/) to find examples that are closest to your domain.

### TVM

You can also opt to use **TVM** directly, especially via its [MXNet][] frontend.
See the extensive list of [tutorials that come with TVM][tvm-tut].

[tvm-tut]: https://docs.tvm.ai/tutorials/
[mxnet]: https://mxnet.apache.org

### GraphIt

To develop graph processing kernels, use **TVM**.
Begin by following the [Getting Started guide](http://graphit-lang.org/getting-started), which walks you through the implementation of the PageRank-Delta algorithm.
(You can skip the initial setup instructions; the compiler is already installed in the container for you.)
Then, check out the [language manual](http://graphit-lang.org/language) for more details.


Energy Profiling
-----------

There are two different mechanisms for profiling energy efficiency; one is most suited for profiling GraphIt programs, and one is most suited for profiling PyTorch programs.

Profiling GraphIt programs
-----------

### HBPintool

The tool only supports being run from the source root of `hbpintool` (`/hbpintool/` in this image).

From the `hbpintool` directory run these commands to profile your GraphIt program:

1. `source SOURCE_THIS`
2. `./hbpintool /path/to/your/graphit/program [your-graphit-program-arguments]`

You should find the output in a file called `hbpintool.out`

#### Preventing Compiler Inlining 

For accuracy the `hbpintool` relies on the GraphIt generated `edgeset_apply` function being defined in the program executable.

However, depending on how the GraphIt C++ output was compiled, this function may have been inlined.

To keep this from happening, open the `.cpp` file generated by `graphitc.py` and add `__attribute__((noinline))` to the definition 
of the templated `edgeset_apply` function (the exact name depends on the GraphIt schedules used).

#### Serial Code Only
This tool is only written to profile serial code (Don't compile the GraphIt program with -fopenmp).
The models it uses to calculate energy factors in the parallelism for the relevant hardware.

#### Intel 64
This tool can only run on Intel x86_64 processors.

### Perf Energy Tool

This tool estimates the energy consumption of TVM programs (and any other program as well) for the Intel E7-8894 v4 CPU. The tool must be run on this CPU to obtain appropriate estimates. It depends on the `perf` utility to read the CPU performance counters.

#### Usage

The tool is located in the `perf-energy-tool` folder.

	Usage options:
	1) If testing ordinary executable:
	             python3 energy_calc.py <executable>
	2) If testing Python program:
	             python3 energy_calc.py python3 <program.py>


Profiling PyTorch programs
---------

We recommend that testers use the PyTorch frontend for development.
Then, to profile an implementation you've created, we recommend you use TVM.
To do so, you will need to export the PyTorch model as [ONNX][] and import into TVM.
Follow these steps:

1. Export the model. Use [torch.onnx.export](https://pytorch.org/docs/master/onnx.html) to save your model to an ONNX file.
2. Import the model into TVM and compile. See [the TVM tutorial about importing ONNX models](https://docs.tvm.ai/tutorials/frontend/from_onnx.html#sphx-glr-tutorials-frontend-from-onnx-py).

[onnx]: https://onnx.ai
