Starlite: A Programmability Testing Environment for HammerBlade
===============================================================

This repository contains a setup for evaluating the programming infrastructure for the HammerBlade project.
HammerBlade is a custom architecture that is programmable using the domain-specific languages [PyTorch][], and [GraphIt][]. PyTorch is a popular prototyping language for ML computations, and GraphIt is an MIT-developed programming
language for developing and tuning graph computations. Our PyTorch tool flow maps down on to the TVM compiler infrastructure.
In some cases, it may be more convenient to use TVM directly.

To help users evaluate the usability of our programming interface, we have provided this repository, which contains
both domain specific languages, and also an energy profiling feature that allows users to get a "compass reading"
on how changes to their code affect energy efficiency. We thank you for working on this, and apologize for any snags encountered—the tools are very cutting edge, and doing very advanced code and data transformations, so it is wise to expect a few snags along the way. We are here to help—please contact us if you are encountering unexpected issues.

To help deploy this toolchain, we have provided in this repository a [Docker][] container setup that includes [PyTorch][], [GraphIt][], and tools for estimating the energy consumption of programs implemented using this infrastructure.

[tvm]: https://tvm.ai
[pytorch]: https://pytorch.org
[graphit]: http://graphit-lang.org
[docker]: https://www.docker.com


Setup
-----

Run the Docker container to get started.
If you don't have a `startEval.sh` script already to do that, see [the detailed setup instructions][setup].
If you ever need any of the example files from this repository, you can clone it:

    $ git clone https://github.com/bespoke-silicon-group/hb_starlite.git

[setup]: https://github.com/bespoke-silicon-group/hb_starlite/blob/master/setup.md


Training
--------

During the training phase, please learn how to use [PyTorch][], for tensor processing and machine learning, and [GraphIt][], for graph processing, including the Python interface to GraphIt.
Please also try running our efficiency estimation tools.
We describe all of these and more in detail below.
Your goal during the training phase is carefully read over everything in this document and to follow the linked tutorial resources.

By the end of the training phase, you should be able to do these things using our container infrastructure:

* *PyTorch:* Build, train, and evaluate an image classifier for the CIFAR-10 dataset. Export the trained network as an ONNX model and execute it in TVM.
* *GraphIt:* Implement a classic undergraduate-level graph processing algorithm, such as the [Floyd–Warshall shortest path algorithm][fw], in GraphIt. Invoke the graph processing kernel from a Python program that loads and supplies compressed sparse row (CSR) data.
* *Efficiency estimation:* Using programs you wrote in PyTorch and GraphIt, run our performance/energy estimation tools to compute projected efficiency when executing on a sample input.

[fw]: https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm


Development Guide
-----------------

Inside the container, you can use [PyTorch][], [TVM][], and [GraphIt][].

### PyTorch

For machine learning and dense linear algebra development, use [PyTorch][].
During training, begin with [the "60-minute blitz" PyTorch tutorial](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html), which shows you how to build and train an image classifier.
During the course of the tutorial, you'll download and train on the popular [CIFAR-10][cifar] dataset.
If you like watching screencasts, try [this PyTorch image classifier tutorial][pytorch-video]. But please be sure to follow the "60-minute blitz" tutorial too to make sure you don't miss anyting.

Also, explore [the full set of PyTorch tutorials](https://pytorch.org/tutorials/). During development, you may find examples there that are close to the domain you're working in.

When following these tutorials, remember to invoke Python by typing `python3`, not just `python`.

[pytorch-video]: https://youtu.be/XriwHXfLi6M
[cifar]: https://www.cs.toronto.edu/~kriz/cifar.html

#### Sparse Tensors

For dealing with sparse tensor data, please use the [torch.sparse][] module.
It's marked as experimental, but it's good for most common uses of sparse matrix data.
Here are some tips for using this module:

[torch.sparse]: https://pytorch.org/docs/stable/sparse.html

##### Sparse Matrix Operations

The most common thing you'll need to do with a sparse matrix is multiply it by a dense matrix.
To do this, use the [`torch.sparse.mm`][sparsemm] method, which is like the more standard `torch.mm` but it works with sparse tensors.
Specifically, use:

    import torch.sparse
    out = torch.sparse.mm(sparse_matrix, dense_matrix)

to produce `out` as a dense matrix.

You can also use standard math operators on sparse tensors.
For example, `a + b` can add two sparse matrices or a sparse and a dense matrix, and `a * b` does *pointwise* multiplication.
The matrix multiply operator, as in `a @ b`, works like the `mm` function above: it implements sparse/dense matrix multiplication.


To convert a sparse tensor to a standard, dense PyTorch tensor, use the `.to_dense()` method.
When debugging, it is often useful to convert a matrix to dense format for printing.

[sparsemm]: https://pytorch.org/docs/stable/sparse.html#torch.sparse.mm
[pytorch_sparse]: https://github.com/rusty1s/pytorch_sparse

##### Sparse/Sparse Matrix Multiplication

The built-in [torch.sparse][] library only supports matrix multiplication between sparse and dense matrices.
If you need sparse/sparse matrix multiplication, please use the companion [pytorch_sparse][] library.
To install it, type:

    $ pip3 install --user torch-scatter torch-sparse

Then, in your code, use the [`sparse_sparse_mm`][spmm-function] function from our `torch-sparse-example.py` file.

[spmm-function]: https://github.com/bespoke-silicon-group/hb_starlite/blob/32fcbe3bca025884e39f4a79fcb1cb7e3a8bf586/torch-sparse-example.py#L37-L53

##### Convert Between SciPy and PyTorch Sparse Tensors

If you have data as a [scipy.sparse][] matrix, we have provided some utilities to convert between that and the torch.sparse representation.
See the [`sparse_scipy2torch` and `sparse_torch2scipy`][convert-funcs] functions in the accompanying `torch-sparse-example.py` file.
You can copy these functions into your code if you need to.

[convert-funcs]: https://github.com/bespoke-silicon-group/hb_starlite/blob/32fcbe3bca025884e39f4a79fcb1cb7e3a8bf586/torch-sparse-example.py#L10-L34
[scipy.sparse]: https://docs.scipy.org/doc/scipy/reference/sparse.html

### TVM

You can also opt to use [TVM][] directly, especially via its [MXNet][] frontend.
See the extensive list of [tutorials that come with TVM][tvm-tut].

[tvm-tut]: https://docs.tvm.ai/tutorials/
[mxnet]: https://mxnet.apache.org

### GraphIt

To develop graph processing kernels, use [GraphIt][].
Begin by following the [Getting Started guide](http://graphit-lang.org/getting-started), which walks you through the implementation of the PageRank-Delta algorithm.
(You can skip the initial setup instructions; the compiler is already installed in the container for you.)
We recommend watching [our GraphIt tutorial screencast][graphit-video] for an introduction to the language.

Once you've gotten the basics down, check out the [language manual](http://graphit-lang.org/language) for more details.
The included [example applications][apps] are also useful as reference material.

We recommend that you *do not use [GraphIt's scheduling language][gtsched]*.
Sticking with the default schedule should be fine for this programmability evaluation, so please just focus on expressing the algorithm.
We also recommend, when writing GraphIt programs, that you never hard-code parameters or filenames---always accept them as command-line arguments.
Keeping these flexible will make it easier to run on multiple inputs.

[graphit-video]: http://homes.cs.washington.edu/~eafurst/graphit_tutorial.html
[apps]: https://github.com/GraphIt-DSL/graphit/tree/master/apps
[gtsched]: http://graphit-lang.org/language#scheduling-language

#### Interop

To build applications that use *both* tensor-oriented compute and graph processing, use Python.
PyTorch (and TVM) use Python natively as their interface, and [GraphIt has Python bindings][graphit-py].

To use GraphIt from Python, you can imitate [our example project](https://github.com/bespoke-silicon-group/hb_starlite/tree/master/py-graphit-example), which shows how to interact with a single-source shortest path (SSSP) kernel from a Python program.
Specifically, follow these steps:

1. Change your GraphIt program by renaming your `main` function to something descriptive, and mark it using [the `export` keyword](http://graphit-lang.org/language#graphit-language-extensions).

2. Replace any globals that come from `argv` or are read from files to instead come from arguments to this function.
   For example, [our SSSP program](https://github.com/bespoke-silicon-group/hb_starlite/blob/master/py-graphit-example/sssp.gt) defines a function like this:

        export func do_sssp(input_edges : edgeset{Edge}(Vertex,Vertex,int), source_vertex : int) -> output : vector{Vertex}(int)
           edges = input_edges;
           vertices = edges.getVertices();
           ...

   whereas [the "standalone" version](https://github.com/GraphIt-DSL/graphit/blob/6f60a231c362b4d2c1211d403702130a63dc8faf/apps/sssp.gt) gets `edges` from a file (by calling `load`) and `source_vertex` comes from `argv`.
   However, `edges` and `vertices` remain as global `const` declarations.

3. In your Python program, add `import graphit`. Then, use `graphit.compile_and_load` to import your GraphIt code as a module.
   In [our example][gpyex], we call it `sssp_module`:

       sssp_module = graphit.compile_and_load("sssp.gt")

   The argument to `compile_and_load` is the filename of your GraphIt source code.

4. Call `<module>.<function>(...)` to invoke your GraphIt function.
   In [our example][gpyex], for instance, we call `sssp_module.do_sssp(edges, start_vertex)`.
   To supply `edgeset` and `vector{Vertex}` arguments to GraphIt functions, use [`scipy.sparse.csr_matrix`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html) and [NumPy array](https://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html) values, respectively.
   You can construct a `csr_matrix` manually or [load one from an `.npz` file](https://docs.scipy.org/doc/scipy-1.0.0/reference/generated/scipy.sparse.load_npz.html), for example.

5. If you need to, you can convert the output from a GraphIt function into a [PyTorch tensor][tensor]. Just use `torch.tensor(vals)`.

We have also provided some utilities for interacting with GraphIt in [`graphit_util.py`][gtutil].
You might want to use these functions:

* The function `load_cached` there works like `graphit.compile_and_load`, but it will skip compilation if the GraphIt source file has not changed.
  This can make development and testing faster: compiling takes a few seconds, even for short programs.
* A `read_adjacency_tsv` function parses "adjacency TSV" files, of the sort made popular by the [MIT GraphChallenge][grdata] datasets.

To see these utilities in action, see [our more complete `example.py`][examplepy].
You can run this example on a non-trivial input graph:

    $ curl -LO 'https://graphchallenge.s3.amazonaws.com/snap/ca-GrQc/ca-GrQc_adj.tsv'
    $ python3 example.py ./ca-GrQc_adj.tsv 3

[graphit-py]: http://graphit-lang.org/language#python-binding
[gpyex]: https://github.com/bespoke-silicon-group/hb_starlite/blob/master/py-graphit-example/sssp.py
[tensor]: https://pytorch.org/docs/stable/torch.html#torch.tensor
[gtutil]: https://github.com/bespoke-silicon-group/hb_starlite/blob/master/py-graphit-example/graphit_util.py
[grdata]: https://graphchallenge.mit.edu/data-sets
[examplepy]: https://github.com/bespoke-silicon-group/hb_starlite/blob/master/py-graphit-example/example.py


Performance Estimation
----------------------

There are two different mechanisms for profiling projected performance & energy efficiency.
The first is better suited to profiling GraphIt programs, and the second is a better fit for PyTorch programs.
If you need to profile a program that uses both, you can either (a) profile the components independently and add their results together or (b) use the second tool (`energy_calc`) for the entire application.

### hbpintool: Profiling GraphIt Programs

To run `hbpintool`, you must be in its directory at `/hbpintool-release` inside the container. Follow these steps:

1. `cd /hbpintool-release`
2. `source SOURCE_THIS`
3. `./hbpintool /your/compiled/graphit/program [arguments]`
4. Find the output in a file called `hbpintool.out`.

In the third step, provide the name of your compiled executable and any arguments it requires.
In other words, if you use `/dir/myapp 1 2` to run the program normally, use `./hbpintool /dir/myapp 1 2` to run it with profiling.

Here are some recommendations for getting the best results out of the tool:

- **Compile with `-O3`.** You'll get more accurate measurements if aggressive compiler optimizations are turned on.
- **Prevent compiler inlining.** For accuracy, `hbpintool` relies on the GraphIt-generated `edgeset_apply` function being defined in the program executable. However, depending on how the GraphIt C++ output was compiled, this function may have been inlined. To keep this from happening, open the `.cpp` file generated by `graphitc.py` and add `__attribute__((noinline))` to the definition of the templated `edgeset_apply` function (the exact name depends on the GraphIt schedules used).
- **Use the GraphIt serial backend when profiling.** Our profiling infrastructure makes use of the GraphIt serial backend, so when you are profiling, please don't compile the GraphIt program with `-fopenmp`. The models it uses to calculate energy factor in the parallelism for the relevant hardware.

#### hbpintool and Python

It's possible to use hbpintool to profile GraphIt kernels even when they're invoked from a Python wrapper.
You'll need to do a few extra things:

- Supply an additional command-line option: `--gtdll <kernel.so>`.
  Give the path to the compiled GraphIt shared object file that your Python program invokes.
- Explicitly supply the path to the Python executable (instead of just giving your Python source file as an argument).
  In this container, use `which python3.5`.

In summary, you can invoke your program like this:

    ./hbpintool --gtdll /path/to/your/graphit/app.so `which python3.5` /path/to/your/python/script.py [your-python-script-arguments]`

### energy_calc: Profiling PyTorch & TVM Programs

We recommend that testers use the PyTorch frontend for development.
Then, to profile an implementation you've created, we recommend you use TVM.
To do so, you will need to export the PyTorch model as [ONNX][] and import into TVM.
Follow these steps:

1. Export the model. Use [torch.onnx.export](https://pytorch.org/docs/master/onnx.html) to save your model to an ONNX file.
2. Import the model into TVM and compile. See [the TVM tutorial about importing ONNX models](https://docs.tvm.ai/tutorials/frontend/from_onnx.html#sphx-glr-tutorials-frontend-from-onnx-py).

[onnx]: https://onnx.ai

The profiling tool uses `perf` and performance counters to estimate energy costs.
The tool is located in the `perf-energy-tool` directory.
You can use the tool to estimate the energy of any program you've written, including models executing in TVM.
Run `energy_calc.py` and specify the program you want to profile:

    $ python3 energy_calc.py <command>

For example, if the thing you're profiling is itself a Python program (e.g., a TVM-based model), do something like this:

     $ python3 energy_calc.py python3 <program.py>

Note that if the provided `perf` version does not work on your machine, you can try one of two steps:

- [Install `perf`](https://askubuntu.com/a/578618) directly on your test container (recommended).
- Rebuild your test container to update perf by running `docker build -t <container-name> .` in the `docker` folder, and using this image for testing.
