import sys
import re
import os
import shutil
import commands

def get_special_paths(dir):

  filenames = os.listdir(dir)
  matches = re.findall(r'\w+_+\w+_+\.\w+', ' '.join(filenames))
  return [os.path.abspath(os.path.join(dir, f)) for f in matches]

def copy_to(paths, dir):

  for path in paths:
    if not os.path.exists(dir):
      os.mkdir(dir)

    shutil.copy(path,dir)

def zip_to(paths, zippath):

  allpaths = ' '.join(paths)
  cmd = 'zip -j '+zippath+' '+allpaths
  (status, output) = commands.getstatusoutput(cmd)
  return

def main():

  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  if args[0] == '--todir':
    todir = args[1]
    dir = args[2]
    paths = get_special_paths(dir)
    copy_to(paths, todir)
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    dir = args[2]
    paths = get_special_paths(dir)
    zip_to(paths,tozip)
    del args[0:2]

    sys.exit(1)

if __name__ == "__main__":
  main()