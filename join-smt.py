#!/usr/bin/python3

import argparse
import os
import re
from anytree import NodeMixin, RenderTree, PreOrderIter  # Requires to install anytree (eg. "pip install anytree")


"""The concept is to parse the .smt files in order of their filenames, which consist of source_name.5_digit_pid.smt.
   It is asummed that the pids are given in increasing order without wrap-around."""


class MyNodeClass(object):
  """Just an example of a base class."""
  foo = 42
  

class MyTreeClass(MyNodeClass, NodeMixin):

  def __init__(self, name, parent = None):
    """Add node features."""
    super(MyTreeClass, self).__init__()
    self.name = name
    self.parent = parent
  
  def find_node(node_name, tree):
    for node in tree:
      if node_name == node.name:
        return node

  def get_tree_structure(smt_files):
    pre_tree = []
    # Read first line of each file
    for file in smt_files:
      fp = open(os.path.dirname(path) + "/" + file, 'r')
      first_line = fp.readline()
      first_line = first_line.replace("; ", "", 1).replace("\n", "", 1)
      print(first_line)
      fp.close()
      order_list = first_line.split("-")
      print(order_list)
      pre_tree.append(order_list)
      
    return pre_tree

  def build_tree(pre_tree):
    tree = []
    
    for smt in pre_tree:
      if len(smt) > 1:
        tree.append(MyTreeClass(smt[-1], parent = MyTreeClass.find_node(smt[-2], tree)))
      elif len(smt) == 1:
        tree.append(MyTreeClass(str(pre_tree[0][0])))  # root has no parent
      else:
        print('Something went horribly wrong. exit')
        exit()
    
    return tree


def parsing():
  """Argument Parsing"""
  parser = argparse.ArgumentParser(
    description='Assembles split .smt files into one .smt file. Takes the original .c file as argument. It requires the .smt files to be already generated in the same folder as the .c file.')  
  parser.add_argument('path', type=str, help='Input .c file of SMT-File generation.')

  args = parser.parse_args()
  path = args.path
  if not (os.path.isfile(path) and path.endswith('.c')):
    print('Input', path, 'is not a valid file.')
    exit()
  
  return path


path = parsing()
# Prepare filenames
name = os.path.basename(path).replace(".c", "", 1)
# print(name)

smt_files = [f for f in os.listdir(os.path.dirname(path)) if re.match(name + r'\.[0-9]{5}\.smt', f)]
if not smt_files:
  print('There are no .smt files in the same folder as the .c source file.')
  exit()
# print(smt_files)

output_file = os.path.dirname(path) + "/" + name + ".smt"
# print(output_file)

pre_tree = MyTreeClass.get_tree_structure(smt_files)

tree = MyTreeClass.build_tree(pre_tree)

# Print the tree in a visually pleasent way
for pre, fill, node in RenderTree(tree[0]):
  print("%s%s" % (pre, node.name))
  
pid_order = [node.name for node in PreOrderIter(tree[0])]
file_order = []

for pid in pid_order:
  file_order.append(os.path.dirname(path) + "/" + name + "." + pid + ".smt")
  
file_out = open(output_file, "w")

for smt_file_name in file_order:
  smt_file = open(smt_file_name, "r")
  contents = smt_file.read()
  contents = re.sub(r'; [0-9]{5}(-[0-9]{5})*\n', "", contents)
  contents = re.sub(r'\(exit\)', "", contents)
  file_out.write(contents)
  smt_file.close()
file_out.write("(exit)\n")
file_out.close()

# TODO: Replace variable names in output file
