#!/usr/bin/env python

# call with list of files where the #includes should be fixed as follows:
# * if an include is '#include "dlvhex/<foo>.h"'
#   it is changed to '#include "dlvhex/<foo>.hpp"'

import sys
import re

def dbg(st):
  st = st # <-- to make the interpreter happy
  #print >>sys.stderr, "dbg: %s" % (st,)

if len(sys.argv) < 2:
  print >>sys.stderr, "usage: %s <files to fix>" % (sys.argv[0],)
  sys.exit(-1)

# give files to manage as arguments
files = sys.argv[1:]
dbg("fixing files %s" % (files,))

def fixIncludeHelper(matchobj):
  fullstr = matchobj.group(0)
  gr1 = matchobj.group(1)
  gr2 = matchobj.group(2)
  #dbg("fixincludehelper got '%s'" % (fullstr,))
  #dbg("fixincludehelper got gr '%s' '%s'" % (gr1,gr2))
  return gr1 + "hpp" + gr2

pattern = re.compile(r'''
  # verbose regex
  ^( # start of line
  \s* # whitespace
  \#include\s*\"dlvhex\/.*\.)h(\" # target include directive
  \s* # whitespace
  )$ # end of line
  ''', re.VERBOSE | re.MULTILINE)
#dbg(pattern.pattern)
#dbg(pattern.findall("bar \n#include \"dlvhex/foo.h\"\n baz"))

def fixIncludesIn(fname):
  f = open(fname,"r")
  contents = f.read()
  f.close()

  lenbak = len(contents)
  contents = pattern.sub(fixIncludeHelper, contents)
  if lenbak == len(contents):
    print >>sys.stdout, "includes in %s are ok." % (fname,)
  else:
    dbg("new file contents:\n" + contents)
    newf = open(fname,"w")
    newf.write(contents)
    newf.close()
    print >>sys.stderr, "includes in %s have been changed!" % (fname,)

for f in files:
  dbg("fixing file %s" % (f,))
  fixIncludesIn(f)
