#!/usr/bin/env python

import os
import sys
import hashlib
from optparse import OptionParser
from datetime import datetime

__VERSION = (0, 2)

def main():

	usage  = "This tool supports a revision file that maps an md5sum to a revision for the policy files\n"

	version = "%prog " + str(__VERSION)

	parser = OptionParser(usage=usage, version=version)

	parser.add_option("-o", "--output", default="stdout", dest="output_file",
		              metavar="FILE", help="Specify an output file, default is stdout")

	parser.add_option("-r", "--revision", default="NONE", dest="revision",
		              metavar="REVISION", help="Specify a revision for this policy")

	(options, args) = parser.parse_args()

	output_file = sys.stdout if options.output_file == "stdout" else open(options.output_file, "w")

	output_file.write('VE=' + options.revision + '\n')

	for f in args:

		name = os.path.basename(f)
#		m = hashlib.md5()
		m = hashlib.sha256()
		m.update(open(f, "r").read())
		hexd = m.hexdigest()
		if (name =="sepolicy"):
			output_file.write('HS=' + hexd + '\n')
		if (name == "seapp_contexts"):
			output_file.write('HA=' + hexd + '\n')
		if (name == "property_contexts"):
			output_file.write('HP=' + hexd + '\n')
		if (name == "file_contexts"):
			output_file.write('HF=' + hexd + '\n')            
		if (name == "mac_permissions.xml"):
			output_file.write('HM=' + hexd + '\n')       			
		if (name == "service_contexts"):
			output_file.write('HV=' + hexd + '\n')       			
    			
	now = datetime.now()
  	buildDate = now.strftime("%a %b %d %H:%M:%S %Y")
	output_file.write('BD=' + buildDate + '\n')
	output_file.write('MP=SHA-256' + '\n')       			
	output_file.write('MV=SHA-256' + '\n')   

if __name__ == "__main__":
	main()
