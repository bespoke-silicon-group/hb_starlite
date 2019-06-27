Starlite: Setup
===============

This document contains extra instructions for running the Starlite evaluation setup "from scratch."


System Requirements
-------------------

This infrastructure requires only [Docker][].
The container requires a standard x86 server and does not require a GPU.

If you want to check that things are working inside the container, type `/test.sh`.
This should print some version information but no errors if everything's in order.


Running the Container
---------------------

First, clone this repository and `cd` into it:

    $ git clone https://gitlab.sdh.cloud/2019-06-submissions/washingtonsdhph1/hb_starlite.git
    $ cd hb_starlite

Next, you'll need to be sure you're logged into [the project's Docker registry][reg] using your provided GitLab credentials.
Do that with `docker login https://registry.sdh.cloud/v2/` if you haven't already.
Then, use our launch script to pull the container and start it up:

    $ ./docker/bash.sh registry.sdh.cloud/2019-06-submissions/washingtonsdhph1/hb_starlite

Or, if you don't have access to the private GitLab and Docker registry, you can use a publicly hosted version of the repository and Docker image instead:

    $ git clone https://github.com/bespoke-silicon-group/hb_starlite.git
    $ cd hb_starlite
    $ ./docker/bash.sh samps/hb_starlite

In either case, there's a chance you will need root permissions to run the Docker container (depending on your system).
If you encounter permissions problems, try `sudo` before the `./docker/bash.sh` command.

When you're inside the container, the default directory is `/workspace`, which is a mount of the `hb_starlite` directory on the host.
So you'll see everything in this repository, including this README file, when you type `ls`.

One additional note: please type `python3`, not just `python`, to use Python.
And if you need to install packages, use `pip3` instead of just `pip`.
All our tools are installed for Python 3.x, and `python` on this system is Python 2.x.

[reg]: https://gitlab.sdh.cloud/2019-06-submissions/washingtonsdhph1/hb_starlite/container_registry
