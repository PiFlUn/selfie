#!/usr/bin/python3

import argparse
import os
import re
from anytree import Node

# Argument Parsing
parser = argparse.ArgumentParser(description='Assembles split .smt files into one .smt file. Give the original .c file as argument.')
parser.add_argument('path', type=str, help='Input .c file of SMT-File generation.')

args = parser.parse_args()
path = args.path
if not os.path.isfile(path):
  print('Input is not a valid file.')
  exit()

# Prepare filenames
name = os.path.basename(path).replace(".c", "", 1)
print(name)

smt_files = [f for f in os.listdir(os.path.dirname(path)) if re.match(name + r'\.[0-9]{5}\.smt', f)]
print(smt_files)

output_file = os.path.dirname(path) + "/" + name + ".smt"
print(output_file)

# Read first line of each file
for file in smt_files:
  fp = open(os.path.dirname(path) + "/" + file, 'r')
  first_line = fp.readline()
  first_line = first_line.replace("; ", "", 1).replace("\n", "", 1)
  print(first_line)
  fp.close()
  order_list = first_line.split("-")
  # TODO: Build tree

# TODO: Concatenate files

# TODO: Replace variable names in output file

#print(args.path)


