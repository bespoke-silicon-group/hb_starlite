import graphit
import os
import importlib
import subprocess
import platform


def _compile(graphit_source_file, module_name, module_file):
    base, _ = os.path.splitext(module_file)
    module_filename_cpp = '{}.cpp'.format(base)
    module_filename_object = '{}.o'.format(base)

    subprocess.check_call(
        "python " + graphit.GRAPHIT_BUILD_DIRECTORY +
        "/bin/graphitc.py -f " + graphit_source_file + " -o " +
        module_filename_cpp + " -m " + module_name,
        shell=True,
    )

    compile_command = (
        graphit.CXX_COMPILER + " -I" +
        graphit.pybind11.get_include(True) +
        " $(python3-config --includes) -c -I " +
        graphit.GRAPHIT_SOURCE_DIRECTORY + "/src/runtime_lib/ " +
        "-std=c++11 -DGEN_PYBIND_WRAPPERS -flto "
        "-fno-fat-lto-objects -fPIC -fvisibility=hidden "
    )

    subprocess.check_call(
        compile_command + module_filename_cpp +
        " -o " + module_filename_object,
        shell=True,
    )

    cmd = (
        graphit.CXX_COMPILER + " -fPIC -shared -o " + module_file +
        " " + module_filename_object + " -flto "
    )

    if platform.system() == "Darwin":
        cmd = cmd + "-undefined dynamic_lookup"

    subprocess.check_call(cmd, shell=True)
    spec = importlib.util.spec_from_file_location(module_name, module_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    os.unlink(module_filename_cpp)
    os.unlink(module_filename_object)


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
       os.stat(graphit_filename).st_mtime > os.stat(lib_filename).st_mtime:
        _compile(graphit_filename, mod_name, lib_filename)

    # (Re)load the module.
    spec = importlib.util.spec_from_file_location(mod_name, lib_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
