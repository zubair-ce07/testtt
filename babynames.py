#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  
  year_info = []
  
  try:
    html = open(filename, "rU").read()
  except IOError:
    sys.stderr.write("Input failed for file: " + filename)
    sys.exit(1)
  
  names_dict = {}
  
  year = re.search(r'Popularity\sin\s(\d\d\d\d)', html)
  names = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', html)
  
  if year:
    year_info.append(year.group(1))
  else:
    sys.stderr.write("Information for year not found")
    sys.exit(1)
  
  for name in names:
    rank = name[0]
    boy_name = name[1]
    girl_name = name[2]
    
    boy_name_count = names_dict.get(boy_name, 0)
    girl_name_count = names_dict.get(girl_name, 0)
    if boy_name_count == 0:
      names_dict[boy_name] = rank
    if girl_name_count == 0:
      names_dict[girl_name] = rank
  
  for (name, rank) in sorted(names_dict.items()): year_info.append(name+ " " + rank)
  return year_info


def summarize(info_list, filename):
  try:
    file_ = open(filename+".summary", 'w')
    info = '\n'.join(info_list) + '\n'
    file_.write(info)
    file_.close()
  except IOError:
    print "Output failed for file: ", filename

def console(info_list):
  for info in info_list: print info
  print '='*10 , "\n"

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  for filename in args:
    year_info = extract_names(filename) 
    if summary:
      summarize(year_info, filename)
    else:
      console(year_info)
    
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  
if __name__ == '__main__':
  main()
