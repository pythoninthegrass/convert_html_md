#!/usr/bin/env python3

# flake8: noqa

# SOURCE: https://cyrille.rossant.net/profiling-and-optimizing-python-code/

import pstats
import sys

# TODO: re-run 3.10.8 cprofile bench - `EOFError: EOF read where object expected`

# check argv for file name (fn)
if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = input("Profile output to convert?: ")

out = input(f"Output file name? [default: {fn}.txt]: ")
if not out:
    out = f"{fn}.txt"

with open(out, "w") as f:
    stats = pstats.Stats(fn).strip_dirs().sort_stats("cumulative").print_stats()
