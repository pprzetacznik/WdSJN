# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re
import sys

allowed_set = {
  u'fin',
  u'bedzie',
  u'aglt',
  u'praet',
  u'impt',
  u'imps',
  # u'inf',
  u'pcon',
  u'pant',
  u'ger',
  u'pact',
  u'ppas'
}

def parse_side(side_tuple):
  left_data = re.findall(ur"([^\s]+?) \[(.*?)\]", side_tuple, re.DOTALL)
  left_data = [(key, value.split(':')) for (key, value) in left_data]
  return left_data

def filter_left(side_list):
  new_side_list = None
  for i in xrange(len(side_list)-1, 0, -1):
    classes = side_list[i][1]
    if bool(allowed_set & set(classes)):
      new_side_list = side_list[i:]
      break
  return new_side_list

def filter_right(side_list):
  new_side_list = None
  for i in xrange(len(side_list)):
    classes = side_list[i][1]
    if bool(allowed_set & set(classes)):
      new_side_list = side_list[:i+1]
      break
  return new_side_list

def parse_note_to_snippet_list(note_tuple):
  left = filter_left(parse_side(note_tuple[0]))
  right = filter_right(parse_side(note_tuple[3]))
  return [left, note_tuple[1], right] if (left and right) else None

def parse_note(filename):
  with open(filename, 'r') as f:
    data = unicode(f.read(), "utf-8")
  data = re.findall(ur"<tr><td[^>]*?>\s?(.*?)</td><td[^>]*?><strong>\s?(.*?)</strong>\s?(.*?)</td><td[^>]*?>\s?(.*?)</td></tr>", data, re.DOTALL)
  snippet_list = map(parse_note_to_snippet_list, data)
  snippet_list = [x for x in snippet_list if x is not None]
  return snippet_list

def print_snippet(snippet, verbose=True):
  if verbose:
    left = [i[0] for i in snippet[0]]
    right = [i[0] for i in snippet[2]]
  else:
    left = [snippet[0][0][0]]
    right = [snippet[2][-1][0]]
  middle = [snippet[1]]
  whole_set = left + middle + right
  print u' '.join(whole_set).encode('utf-8')

def print_snippet_list(snippet_list, verbose=True):
  for snippet in snippet_list:
    print_snippet(snippet, verbose)

def main(filename, verbose):
  print_snippet_list(parse_note(filename), verbose)

if __name__ == '__main__':
  if len(sys.argv) >= 2:
    filename = sys.argv[1]
    verbose = (sys.argv[2] == 'True') if len(sys.argv) == 3 else True
    main(filename, verbose)
  else:
    print "Usage:"
    print "  python -m parse_notes [filename.html] [verbose]"
    print "  eg. python -m parse_notes data/orzel.html False"