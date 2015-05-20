# -*- coding: utf-8 -*-

from os.path import dirname, join
from setuptools import setup

setup(
    author = "Ruslan Korniichuk",
    author_email = "ruslan.korniichuk@gmail.com",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities"
    ],
    description = ("Remote jupyter kernel/kernels administration utility"),
    download_url = "https://github.com/korniichuk/rk/archive/0.2.zip",
    entry_points = {
        'console_scripts': 'rk = rk.rk:main'
    },
    include_package_data = True,
    install_requires = [
        "configobj",
        "execnet"
    ],
    keywords = ["ipython", "jupyter", "remote kernel", "python2"],
    license = "Public Domain",
    long_description = open(join(dirname(__file__), "README.rst")).read(),
    name = "rk",
    packages = ["rk"],
    platforms = ["Linux"],
    scripts=['scripts/rkscript'],
    url = "https://github.com/korniichuk/rk",
    version = "0.2a1",
    zip_safe = True
)
