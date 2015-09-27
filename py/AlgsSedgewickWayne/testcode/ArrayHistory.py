#!/ust/bni/env python
"""A module for helping to visualize array sorting."""

# Copyright (C) 2014-2015  DV Klopfenstein
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import sys
import copy

import AlgsSedgewickWayne.testcode.InputArgs as IA

def run(container, seqstr, expected=None, prt=sys.stdout, details=sys.stdout):
  """Run a sequence of Stack commands."""
  lst = IA.get_seq__int_or_str(seqstr)
  result = run_list(container, lst, details)
  if expected is not None:
    pf = result == expected
    pass_fail = "   Pass" if pf else " **FAIL"
    #prt.write("{}: EXP({}) ACTUAL({}) from seq: {}\n".format(
    prt.write("{PF} GIVEN({SEQ}) -> ACTUAL({ACT})".format(
      PF=pass_fail, EXP=expected, ACT=result, SEQ=seqstr))
    if not pf:
      prt.write(" EXPECTED({})".format(expected))
    prt.write("\n")

def run_list(container, item_list, prt=sys.stdout):
  """Inserts items in a string into a container. Prints steps. Returns end state."""
  if prt is not None:
    prt.write("\nINPUT: {}\n".format(' '.join([str(item) for item in item_list])))
  result = []
  for item in item_list:
    if item != "-":
      container.push(item)
      if prt is not None:
        prt.write("{:10}   PUSH {:10} +STACK: {}\n".format("", item, container))
    elif not container.isEmpty():
      popped = container.pop()
      result.append(popped)
      if prt is not None:
        prt.write("{:>10} <-POP  {:10} -STACK: {}\n".format(popped, item, container))
  if prt is not None:
    prt.write('({} left on stack)\n'.format(container.size()))
  return ' '.join([str(item) for item in result])

def run_Queue(container, seqstr, prt=sys.stdout):
  """Inserts items in a string into a container."""
  return run_Queue_list(container, IA.get_seq__int_or_str(seqstr), prt)

def run_Queue_list(container, item_list, prt=sys.stdout):
  """Inserts items in a string into a container. Prints steps. Returns end state."""
  prt.write("\nINPUT: {}\n".format(' '.join([str(item) for item in item_list])))
  result = []
  for item in item_list:
    if item != "-":
      container.enqueue(item)
      prt.write("{:10}   ENQUEUE {:10} +QUEUE: {}\n".format("", item, container))
    elif not container.isEmpty():
      popped = container.dequeue()
      result.append(popped)
      prt.write("{:>10} <-DEQUQUE {:10} -QUEUE: {}\n".format(popped, item, container))
  prt.write('({} left on stack)\n'.format(container.size()))
  return ' '.join([str(item) for item in result])

def ex_stdin(container, prt=sys.stdout):
  """Read a string sequence from STDIN."""
  result = ""
  while True:
    item = raw_input('TYPE WORDS OR -')
    if not item:
      break
    if item != "-":
      container.push(item)
    elif not container.isEmpty():
      result = ' '.join([result, container.pop()])
  prt.write('(%d left on stack) OUTPUT: %container\n'%(container.size(), result))

def chk(a, txt):
  b = txt.split()
  return arrays_equal(a, b)

def arrays_equal(a, b):
  """TBD: Remove?"""
  return len(a) == len(b) and len(a) == sum([1 for i, j in zip(a, b) if i == j])

def history_contains(array_history, potential_midpoint):
  """ Tests if a midpoint could have occured sometime during a sort."""
  for A in array_history:
    if arrays_equal(A[0], potential_midpoint):
      return True
  return False

def get_keystr(E):
  """TBD"""
  if isinstance(E, dict):
    if len(E) == 1:
      return str(E.keys()[0])
    else:
      raise Exception('TIME TO IMPLEMENT MUTIPLE KEYS')
  else:
    return E

def get_elem2num(array_history):
  """ 1 is assigned to smallest element.  len(arr)+1 is assigned to largest element."""
  # In array_history, last array should be the sorted arrayA
  elem2num = {}
  num = 1
  for elem in array_history[-1][0]:
    elem2num[get_keystr(elem)] = num
    num += 1
  return elem2num

def get_anno(idx, idx2sym):
  """TBD"""
  if idx2sym is None or idx not in idx2sym:
    return ' '
  return idx2sym[idx]

def xor_txt(txt_prev, txt_curr):
  """Xor two strings. Return string w/matches('.') and mismatches('X')"""
  ord_xor = [ord(a) ^ ord(b) for a,b in zip(txt_prev, txt_curr)]
  lst = []
  for n, c in zip(ord_xor, txt_curr):
    if c == ' ':
      lst.append(' ')
    elif n == 0:
      lst.append('.')
    else:
      lst.append('X')
  return ''.join(lst)

class ArrayHistory(object):
  """Class to manage array history for visualization and learning."""

  def __init__(self):
    self.array_history = []

  def add_history(self, ARR, anno):
    """Add current arry state to array history."""
    self.array_history.append([copy.deepcopy(ARR), anno])

  def __iter__(self):
    for array_state in self.array_history:
      yield array_state

  def prt(self, prt=sys.stdout):
    """ Prints array history with spaces between elements."""
    txt_prev = None
    txt_curr = None
    for idx, A in enumerate(self.array_history):
      txt_prev = txt_curr
      txt_curr = ' '.join([str(item) for item in A[0]])
      if txt_prev is not None:
        txt_mtch = xor_txt(txt_prev, txt_curr)
        prt.write('    {}\n'.format(txt_mtch))
      prt.write('{:2d}: {}\n'.format(idx, txt_curr))
    prt.write("\n")
  

  def show(self, desc, prt=sys.stdout):
    """ Print array history plus histogram bars (viewed horizontally) to help visualize sort."""
    if isinstance(self.array_history, list) and len(self.array_history) != 0:
      elem2num = get_elem2num(self.array_history)
      for incr, A in enumerate(self.array_history):
        Astr = [str(item) for item in A[0]]
        prt.write('{:2d} {}: {}\n'.format(incr, desc, ' '.join(Astr)))
        for idx, elem in enumerate(A[0]):
          anno = get_anno(idx, A[1])
          prt.write('{:2d} {}({:2d}): {}{:2} {}\n'.format(
              incr, desc, idx, anno, elem, ''.join(['*']*elem2num[get_keystr(elem)])))
        prt.write('\n')





