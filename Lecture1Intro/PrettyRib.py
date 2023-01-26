#!/usr/bin/env python
#
# (Copyright (C) 2008  Jonathan Macey jmacey@bournemouth.ac.uk
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Should you need to contact me, the author, you can do so either by
# e-mail <jmacey@bournemouth.ac.uk>, or by paper mail:
# J. Macey National Center for Computer Animation
#					 Bournemouth University
#					 Fern Barrow, Poole Dorset
#					 England BH125BB
# tidy machine generated RIBs to make them more readble
# Jon Macey jmacey@bmth.ac.uk
# version 1.0 
# Change Log :
#
# Todo : add command line options for different tab sizes etc
#		 add command line options for different file name output
# 		 
import os, commands, getopt, sys

def usage():
	print ("PrettyRib")
	print ("(C) Jon Macey jmacey@bmth.ac.uk")
	print ("_______________________________________")
	print ("-h print this help")
	print (""" Basically PrettyRib adds indentation to a rib file created by prman's python binding \n
	This is only to make the output more readable for inspection etc""")

# exception class for command line arguments
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

# tokens to search for, BeginTokens will add a \t after thay are found to the TABLEVEL
BeginTokens=["WorldBegin" ,"TransformBegin","AttributeBegin","FrameBegin","MotionBegin" ,"SolidBegin","ObjectBegin"]
# end tokens will remove a \t from the TABLEVEL
EndTokens=["WorldEnd" ,"TransformEnd","AttributeEnd","FrameEnd","MotionEnd" ,"SolidEnd","ObjectEnd"]

# function to tidy the rib file, at present we create a new rib in memort from the file
# passed in and add the TABLEVEL number of \t to the output stream
# finally we save back to the same file name

def RibTidy(File) :
	print ("opening : "+File)
	# default to no tabs
	TABLEVEL=""
	# open the file
	ip = open(File,'r')
	#grab the data as lines
	data=ip.readlines()
	# opdata is where our output is placed with the new tabs
	opdata=""
	# for each line check for one of our tokens
	for line in data :
		# we assume that our Tokens are always the first element of the line (which IIRC the rispec specifies)
		# so we split each line and look at the first element
		tokens=line.split()	
		# make sure we have a token to check against
		if(len(tokens) >0 ) :
		# if we have one of the begin tokens we write out the line then add a tab to the tokens
		# i.e.
		# WorldBegin
		# \t next lines
		# every thing after has a tab in it.

			if(tokens[0] in BeginTokens) :
				opdata+=TABLEVEL+line
				TABLEVEL+="\t"
			# for the End Tokens we do the opposite of above, so we remove the \t then print the line so
			# the token will be un-indented a level
			elif (tokens[0] in EndTokens) :
				# we can use the [: size] operation to copy the TABLEVEL - the last token (\t is 1 element long)
				TABLEVEL=TABLEVEL[:len(TABLEVEL)-1]
				opdata+=TABLEVEL+line
			# if it's not a begin or end token print out TABS then line verbatim
			else :
				opdata+=TABLEVEL+line
	# close the file
	ip.close()
	# now write over it with the pretty version
	op = open(File,'w')
	op.write(opdata)
	# tell the user were finished.
	print( "Done ")


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "h", ["help"])
		except getopt.error, msg:
			raise Usage(msg)
    	except Usage, err:
			print (sys.stderr, err.msg)
			print (sys.stderr, "for help use --help")
			return 2
	for opt, arg in opts:               
		if opt in ("-h", "--help"):      
			usage()
		
	# loop through the files passed as arguments
	for Files in argv[1:] :
		# if it end in rib then process it so we can use wildcards 
		if (Files.endswith('.rib') ):
			print ("Adding indentation to "+Files)
			RibTidy(Files)

if __name__ == "__main__":
    sys.exit(main())

