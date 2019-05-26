Starlite: A Programmability Testing Environment for HammerBlade
===============================================================

This repository contains a setup for evaluating the programming infrastructure for the HammerBlade project.
HammerBlade is a custom architecture that is programmable using the domain specific languages [PyTorch][], and [GraphIt][]. [PyTorch][] is a popular prototyping language for ML computations, and [GraphIt][] is an MIT-developed programming
language for developing and tuning graph computations. Our [PyTorch][] tool flow maps down on to the [TVM][] ML optimization
flow, which in itself is a ML-programming language. In some cases, it may be more convenient to use [TVM][] directly.

To help users evaluate the usability of our programming interface, we have provided this repository, which contains
both domain specific languages, and also an energy profiling feature that allows users to get a "compass reading"
on how changes to their code affect energy efficiency. We thank you for working on this, and apologize for any snags encountered—the tools are very cutting edge, and doing very advanced code and data transformations, so it is wise to expect a few snags along the way. We are here to help—please contact us if you are encountering unexpected issues.

To help deploy this toolchain, we have provided in this repository a [Docker][] container setup that includes [PyTorch][], [GraphIt][], and tools for estimating the energy consumption of programs implemented using this infrastructure.

[tvm]: https://tvm.ai
[pytorch]: https://pytorch.org
[graphit]: http://graphit-lang.org
[docker]: https://www.docker.com


Running the Container
---------------------

To run the container, first log into [the SDH Docker registry][reg] using your SDH GitLab credentials:

    $ docker login https://registry.sdh.cloud/v2/

Then, use our launch script to pull the container and start it up:

    $ ./docker/bash.sh registry.sdh.cloud/2019-06-submissions/washingtonsdhph1/hb_starlite

You might need root permissions based on your local Docker setup (so try this with `sudo` if it doesn't work without it).
The container requires a standard x86 server and does not require a GPU.

[reg]: https://gitlab.sdh.cloud/2019-06-submissions/washingtonsdhph1/hb_starlite/container_registry

Inside the container, type this command to make sure things are working:

    $ /test.sh

You can also see the `Dockerfile` source for details on how this is set up.
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

To develop graph processing kernels, use **GraphIt**.
Begin by following the [Getting Started guide](http://graphit-lang.org/getting-started), which walks you through the implementation of the PageRank-Delta algorithm.
(You can skip the initial setup instructions; the compiler is already installed in the container for you.)
Then, check out the [language manual](http://graphit-lang.org/language) for more details.

### Interop

To build applications that use *both* tensor-oriented compute and graph processing, use Python.
PyTorch (and TVM) use Python natively as their interface, and [GraphIt has Python bindings][graphit-py].

To use GraphIt from Python, you can imitate [our example project](https://github.com/bespoke-silicon-group/hb_starlite/tree/master/py-graphit-example), which shows how to interact with a single-source shortest path (SSSP) kernel from a Python program.
Specifically, follow these steps:

1. Change your GraphIt program by renaming your `main` function to something descriptive, and mark it using [the `export` keyword](http://graphit-lang.org/language#graphit-language-extensions).

2. Replace any globals that come from `argv` or are read from files to instead come from arguments to this function.
   For example, [our SSSP program](https://github.com/bespoke-silicon-group/hb_starlite/blob/master/py-graphit-example/sssp.gt) defines a function like this:

       export func do_sssp(input_edges : edgeset{Edge}(Vertex,Vertex, int)) -> output : vector{Vertex}(int)
           edges = input_edges;
           vertices = edges.getVertices();
           ...

   whereas [the "standalone" version](https://github.com/GraphIt-DSL/graphit/blob/6f60a231c362b4d2c1211d403702130a63dc8faf/apps/sssp.gt) gets `edges` from a file (by calling `load`).
   However, `edges` and `vertices` remain as global `const` declarations.

3. In your Python program, add `import graphit`. Then, use `graphit.compile_and_load` to import your GraphIt code as a module.
   In [our example][gpyex], we call it `sssp_module`:

       sssp_module = graphit.compile_and_load("sssp.gt")

   The argument to `compile_and_load` is the filename of your GraphIt source code.

4. Call `<module>.<function>(...)` to invoke your GraphIt function.
   In [our example][gpyex], for instance, we call `sssp_module.do_sssp(edges, start_vertex)`.
   To supply `edgeset` and `vector{Vertex}` arguments to GraphIt functions, use [`scipy.sparse.csr_matrix`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html) and [NumPy array](https://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html) values, respectively.
   You can construct a `csr_matrix` manually or [load one from an `.npz` file](https://docs.scipy.org/doc/scipy-1.0.0/reference/generated/scipy.sparse.load_npz.html), for example.

[graphit-py]: http://graphit-lang.org/language#python-binding
[gpyex]: https://github.com/bespoke-silicon-group/hb_starlite/blob/master/py-graphit-example/sssp.py


Energy Profiling
----------------

There are two different mechanisms for profiling energy efficiency; one is most suited for profiling GraphIt programs, and one is most suited for profiling PyTorch programs.

### Profiling GraphIt programs

#### HBPintool

The tool only supports being run from the source root of `hbpintool` (`/hbpintool/` in this image).

From the `hbpintool` directory run these commands to profile your GraphIt program:

1. `source SOURCE_THIS`
2. `./hbpintool /path/to/your/graphit/program [your-graphit-program-arguments]`

You should find the output in a file called `hbpintool.out`

#### Compile with -O3

You'll get more accurate measurements if aggresive compiler optimizations are turned on.

#### Preventing Compiler Inlining 

For accuracy the `hbpintool` relies on the GraphIt generated `edgeset_apply` function being defined in the program executable.

However, depending on how the GraphIt C++ output was compiled, this function may have been inlined.

To keep this from happening, open the `.cpp` file generated by `graphitc.py` and add `__attribute__((noinline))` to the definition 
of the templated `edgeset_apply` function (the exact name depends on the GraphIt schedules used).

#### Use GraphIt Serial Backend when Profiling

Our profiling infrastructure makes use of the GraphIt serial backend, so when you are profiling, please don't compile the GraphIt program with -fopenmp. The models it uses to calculate energy factor in the parallelism for the relevant hardware.

#### Intel 64

The energy profiling infrastructure can only run on Intel x86_64 processors.


### Profiling PyTorch programs

We recommend that testers use the PyTorch frontend for development.
Then, to profile an implementation you've created, we recommend you use TVM.
To do so, you will need to export the PyTorch model as [ONNX][] and import into TVM.
Follow these steps:

1. Export the model. Use [torch.onnx.export](https://pytorch.org/docs/master/onnx.html) to save your model to an ONNX file.
2. Import the model into TVM and compile. See [the TVM tutorial about importing ONNX models](https://docs.tvm.ai/tutorials/frontend/from_onnx.html#sphx-glr-tutorials-frontend-from-onnx-py).

[onnx]: https://onnx.ai

#### Perf Energy Tool

This tool estimates the energy consumption of TVM programs (and any other program as well) for the Intel E7-8894 v4 CPU. The tool assumes it is using this CPU. It depends on the `perf` utility to read the CPU performance counters.

#### Usage

The tool is located in the `perf-energy-tool` folder.
You can use the tool to estimate the energy of any program you've written, including models executing in TVM.
Just run `energy_calc.py` and specify the program you want to profile:

    $ python3 energy_calc.py <command>

For example, if the thing you're profiling is itself a Python program (e.g., a TVM-based model), do something like this:

     $ python3 energy_calc.py python3 <program.py>

