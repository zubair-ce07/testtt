import sys
import re

def extract_names(filename):

  f = open(filename, 'rU')
  text = f.read()
  year = re.search(r'"\d\d\d\d"', text).group()[1:5]
  nameranks = re.findall(r'>(\d+)</td><td>(\w+)</td><td>(\w+)<', text)
  dict = {}
  for tuple in nameranks:
    dict[tuple[1]] = tuple[0]
    dict[tuple[2]] = tuple[0]

  finallist = []
  finallist.append(year)
  for name in sorted(dict.keys()):
    finallist.append(name+" "+dict[name])

  return finallist

def main():

  args = sys.argv[1:]
  if not args:
    print 'usage: [--summaryfile] file [file ...]'

  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]
  else:
    filename = sys.argv[1]
    names = extract_names(filename)
    print names
    sys.exit(1)

if __name__ == '__main__':
  main()