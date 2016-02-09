#!/usr/bin/python
from os import *
from os.path import *

import os, commands, getopt, sys			
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
		
def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "c", ["clean"])
		except getopt.error, msg:
			raise Usage(msg)
    	except Usage, err:
			print >>sys.stderr, err.msg
			print >>sys.stderr, "for help use --help"
			return 2
	BUILD="render"
	for opt, arg in opts:               
		if opt in ("-c", "--clean"):      
			BUILD+=" -c"
	
	FileNames=listdir(".")
	for Files in FileNames :
		if (Files.endswith('.rib')  ):
			print "Rendering ",Files
			system(BUILD+" "+Files)
			
			
			

if __name__ == "__main__":
    sys.exit(main())

