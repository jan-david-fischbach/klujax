""" KLUJAX Setup. """

import os
import site
import sys
from glob import glob

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

CWD = os.path.dirname(os.path.abspath(__file__))

include_dirs = [
    os.path.join(CWD, "xla"),
    os.path.join(CWD, "pybind11", "include"),
    os.path.join(CWD, "suitesparse", "SuiteSparse_config"),
    os.path.join(CWD, "suitesparse", "AMD", "Include"),
    os.path.join(CWD, "suitesparse", "COLAMD", "Include"),
    os.path.join(CWD, "suitesparse", "BTF", "Include"),
    os.path.join(CWD, "suitesparse", "KLU", "Include"),
]

suitesparse_sources = [
    os.path.join(CWD, "suitesparse", "SuiteSparse_config", "SuiteSparse_config.c"),
    *glob(os.path.join(CWD, "suitesparse", "AMD", "Source", "*.c")),
    *glob(os.path.join(CWD, "suitesparse", "COLAMD", "Source", "*.c")),
    *glob(os.path.join(CWD, "suitesparse", "BTF", "Source", "*.c")),
    *glob(os.path.join(CWD, "suitesparse", "KLU", "Source", "*.c")),
]


if sys.platform == "linux":  # gcc
    extension = Extension(
        name="klujax_cpp",
        sources=["klujax.cpp", *suitesparse_sources],
        include_dirs=include_dirs,
        library_dirs=site.getsitepackages(),
        extra_compile_args=["-std=c++17"],
        extra_link_args=["-static-libgcc", "-static-libstdc++"],
        language="c++",
    )
elif sys.platform == "win32":  # cl
    extension = Extension(
        name="klujax_cpp",
        sources=["klujax.cpp", *suitesparse_sources],
        include_dirs=include_dirs,
        library_dirs=site.getsitepackages(),
        extra_compile_args=["/std:c++17"],
        extra_link_args=[],
        language="c++",
    )
elif sys.platform == "darwin":  # MacOS: clang
    extension = Extension(
        name="klujax_cpp",
        sources=["klujax.cpp", *suitesparse_sources],
        include_dirs=include_dirs,
        library_dirs=site.getsitepackages(),
        extra_compile_args=[],  # clang defaults to c++17 and setting -std=c++17 prevents combined build with suitesparse c source.
        extra_link_args=[],
        language="c++",
    )
else:
    raise RuntimError(f"Platform {sys.platform} not supported.")


setup(
    name="klujax",
    version="0.2.10",
    author="Floris Laporte",
    author_email="floris.laporte@gmail.com",
    description="a KLU solver for JAX",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flaport/klujax",
    py_modules=["klujax"],
    ext_modules=[extension],
    cmdclass={"build_ext": build_ext},
    install_requires=["jax>=0.4.35", "jaxlib>=0.4.35"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    package_data={
        "*": [
            "LICENSE",
            "README.md",
            "MANIFEST.in",
        ],
    },
)
