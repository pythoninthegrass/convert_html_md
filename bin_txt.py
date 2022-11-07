#!/usr/bin/env python3

# flake8: noqa

# SOURCE: https://cyrille.rossant.net/profiling-and-optimizing-python-code/

import pstats
import sys

# check argv for file name (fn)
if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = input("Profile output to convert?: ")

out = input("Output file name?: ")

with open(out, "w") as f:
    stats = pstats.Stats(fn, stream=f).strip_dirs().sort_stats("cumulative").print_stats()
