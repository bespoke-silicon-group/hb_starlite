import graphit
import os
import shutil
import importlib


def load_cached(graphit_filename, lib_filename=None):
    """Get a Python module that wraps the GraphIt program, given as
    source code at the given path.

    If the source has been modified since the last time this function
    was called for the module, automatically recompile it. Specify
    `lib_filename` to choose where the shared object for the compiled code
    goes; otherwise, this will be chosen automatically to reside
    alongside the GraphIt source file.
    """
    if not lib_filename:
        base, _ = os.path.splitext(graphit_filename)
        lib_filename = '{}.so'.format(base)

    # Generate a name for the module.
    base, _ = os.path.splitext(lib_filename)
    mod_name = '{}_gt'.format(os.path.basename(base))

    # Compare the mtimes of the source and compiled version. Recompile
    # if necessary.
    if not os.path.exists(lib_filename) or \
       os.stat(graphit_filename).mtime > os.stat(lib_filename):
        # By default, the GraphIt module compiles to /tmp. We'll do
        # that, then copy the underlying file to our intended location.
        mod = graphit.compile_and_load(graphit_filename)
        shutil.copyfile(mod.__file__, lib_filename)

    # (Re)load the module.
    spec = importlib.util.spec_from_file_location(mod_name, lib_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
