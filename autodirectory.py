#!/usr/bin/python3

import argparse
import autodir

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("--cols", help="number of columns",
                    action="store", required=True, type=int)
parser.add_argument("--rows", help="number of rows",
                    action="store", required=True, type=int)
parser.add_argument("--input", help="input directory",
                    action="store", required=True)
parser.add_argument("--logdir", help="logging directory",
                    action="store")

args = parser.parse_args()

autodir.generate_pdf(indir=args.input, outdir=args.input, rows=args.rows, cols=args.cols, logdir=args.logdir)
