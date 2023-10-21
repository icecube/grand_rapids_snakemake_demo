from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--outfile")
parser.add_argument("--infile")
parser.add_argument("--seed", type=float)


args = parser.parse_args()

with open(args.infile, "r") as hdl:
    inp = "\n".join(hdl.readlines())

with open(args.outfile, "w") as hdl:
    hdl.writelines([
        f"Input file is: {inp}",
        f"Running proc_fl with seed: {args.seed}"
        ])
