Starlite: A Programmability Testing Environment for HammerBlade
===============================================================

This repository contains a setup for evaluating the programming infrastructure for the HammerBlade project.
HammerBlade is a custom architecture that is programmable using the domain-specific languages [PyTorch][], and [GraphIt][]. PyTorch is a popular prototyping language for ML computations, and GraphIt is an MIT-developed programming
language for developing and tuning graph computations. Our PyTorch tool flow maps down on to the TVM compiler infrastructure.

To help deploy this toolchain, we have provided in this repository a [Docker][] container setup that includes [PyTorch][], [GraphIt][], and tools for estimating the energy consumption of programs implemented using this infrastructure.

[tvm]: https://tvm.ai
[pytorch]: https://pytorch.org
[graphit]: http://graphit-lang.org
[docker]: https://www.docker.com


Running the Container
---------------------

First, clone this repository and `cd` into it:

    $ git clone https://github.com/bespoke-silicon-group/hb_starlite.git
    $ cd hb_starlite

(You can also use the internal GitLab instance instead of the public GitHub repository if you prefer. They contain the same code.)
Then, use our launch script to pull the container and start it up:

    $ ./docker/bash.sh samps/hb_starlite

Or, if you don't have access to the private GitLab and Docker registry, you can use a publicly hosted version of the repository and Docker image instead:

When you're inside the container, the default directory is `/workspace`, which is a mount of the `hb_starlite` directory on the host.
So you'll see everything in this repository, including this README file, when you type `ls`.

One additional note: please type `python3`, not just `python`, to use Python.
And if you need to install packages, use `pip3` instead of just `pip`.
All our tools are installed for Python 3.x, and `python` on this system is Python 2.x.


Development Guide
-----------------

Inside the container, you can use [PyTorch][], [TVM][], and [GraphIt][].

### PyTorch

For machine learning and dense linear algebra development, use [PyTorch][].
Consider starting with [the "60-minute blitz" PyTorch tutorial](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html), which shows you how to build and train an image classifier.

When following these tutorials, remember to invoke Python by typing `python3`, not just `python`.

[pytorch-video]: https://youtu.be/XriwHXfLi6M
[cifar]: https://www.cs.toronto.edu/~kriz/cifar.html

#### Sparse Tensors

For dealing with sparse tensor data, please use the [torch.sparse][] module.
It's marked as experimental, but it's good for most common uses of sparse matrix data.

[torch.sparse]: https://pytorch.org/docs/stable/sparse.html

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

### Interop

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
