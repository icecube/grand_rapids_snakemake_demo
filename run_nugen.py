from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("--outfile")
parser.add_argument("--seed", type=float)
parser.add_argument("--xsec")

args = parser.parse_args()

with open(args.outfile, "w") as hdl:
    hdl.write(f"Running nugen with seed: {args.seed} and xsec: {args.xsec}\n ENV: {os.environ['CONDA_PREFIX']}")
