from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--outfile")
parser.add_argument("--infiles", nargs="+")


args = parser.parse_args()

inp = ""
for infile in args.infiles:
    with open(infile, "r") as hdl:
        inp += "\n".join(hdl.readlines())

with open(args.outfile, "w") as hdl:
    hdl.writelines([
        f"Input file is: {inp}",
        f"Running plot"
        ])
