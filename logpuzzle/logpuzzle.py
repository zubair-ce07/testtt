import os
import re
import sys
import urllib

def read_urls(filename):

  server = re.search(r'_\w+\.\w+\.\w+', filename).group()[1:]
  f = open(filename, 'rU')
  text = f.read()
  matches = re.findall(r'GET\s(\S+puzzle\S+)\sHTTP', text)
  fullmatches = ["http://"+server+match for match in matches]
  return fullmatches

def download_images(img_urls, dest_dir): # This function did not work; images kept getting replaced somehow.

  for img in img_urls:
    urllib.urlretrieve(img, dest_dir)
  return

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()