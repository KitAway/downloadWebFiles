#! /usr/bin/python3
import urllib.request
import urllib.parse
import re
import argparse
import os
import os.path

def main(url, fileType, todir):
  website = urllib.request.urlopen(url)
  html=website.read()
  pattern = re.compile('href="(.*%s)"'%fileType)
  files=re.findall(pattern, html.decode('utf-8'))
  for file in files:
    filepath = os.path.join(todir, file)
    fullLink = urllib.parse.urljoin(url, file)
    try:
      urllib.request.urlretrieve(fullLink, filepath)
    except Exception as e:
      print(e)
      print("Download file %s failed."%file)
#  print(links)


if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Download the certain type of files from the given website")
  parser.add_argument('--url', help='website URL',default=None)
  parser.add_argument('--todir', help='Folder stores the files', default='./data/')
  parser.add_argument('--filetype', help='suffix of the file',default=None)
  
  args = parser.parse_args()
  if args.url==None or args.filetype==None:
    parser.print_help()
  else:
    
    if not os.path.exists(args.todir):
      os.mkdir(args.todir)
    main(args.url, args.filetype, args.todir)
