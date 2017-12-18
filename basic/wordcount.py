import sys

def make_dict(filename):

  f = open(filename, 'rU')
  dict = {}
  for line in f:
    words = line.split()
    for word in words:
      if word.lower() in dict:
        dict[word.lower()] += 1
      else:
        dict[word.lower()] = 1

  return dict

def print_words(filename):

  dict = make_dict(filename)
  for key in sorted(dict.keys()):
    print key+" "+str(dict[key])

def print_top(filename):

  dict = make_dict(filename)
  count = 0
  dictReverse = sorted(dict.keys(), key = dict.get, reverse=True)
  for k in dictReverse:
    if count<20:
      print k + " " + str(dict[k])
      count += 1
    else:
      break

def main():

  if len(sys.argv) != 3:
    print 'usage: ./wordcount.py {--count | --topcount} file'
    sys.exit(1)

  option = sys.argv[1]
  filename = sys.argv[2]
  if option == '--count':
    print_words(filename)
  elif option == '--topcount':
    print_top(filename)
  else:
    print 'unknown option: ' + option
    sys.exit(1)

if __name__ == '__main__':
  main()