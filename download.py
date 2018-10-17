#! /usr/bin/python3
import urllib.request
import urllib.parse
import re
import argparse
import os
import os.path

def main(url, fileType, todir, debug=False):
  website = urllib.request.urlopen(url)
  coding = re.search('charset=([\w.-]+)',website.headers._headers[0][1]).group(1)
  html=website.read()
  strs = html.decode(coding)
  pattern0 = re.compile('(https?://[/\w.-]+%s)'%fileType)
  pattern1 = re.compile('href="([\w.-]+%s)"'%fileType)
  fileUrls=re.findall(pattern0, strs)
  hyperFiles=re.findall(pattern1, strs)
  if debug:
    for fileUrl in fileUrls:
      filename = fileUrl.split('/')[-1]
      print("fileUrl is %s, and filename is %s."%(fileUrl, filename))
      print('\n')
    for filename in hyperFiles:
      fileUrl = urllib.parse.urljoin(url, filename)
      print("fileUrl is %s, and filename is %s."%(fileUrl, filename))
      print('\n')
    return
  else:
    for filename in hyperFiles:
      fileUrl = urllib.parse.urljoin(url, filename)
      fileUrls.append(fileUrl)
    urlSet = set(fileUrls)
    total = len(urlSet)
    num=0
    for fileUrl in urlSet:
      filename = fileUrl.split('/')[-1]
      filepath = os.path.join(todir, filename)
      num+=1
      try:
        urllib.request.urlretrieve(fileUrl, filepath)
        print("%d/%d is downloaded."%(num,total))
      except Exception as e:
        print(e)
        print("Download file %s failed."%filename)


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
