#!/usr/bin/env python

from optparse import OptionParser
from sets import Set
import logging
import sys
import os
import re
import time

__VERSION = (0, 1)

'''
This tool works for 'typeof a, b;' syntax.
This tool reads the policy.conf file and inherit all rules from b to a.
'''

def extractAttribute(configfile):
    attrilist = []
    inputfile = open(configfile)
    for line in inputfile:
        if line.startswith('attribute'):
            attrilist.append(line.rstrip(';\n').split(' ')[1])

    return attrilist


def extractTypeof(configfile):
    typeoflist = []
    inputfile = open(configfile)
    for line in inputfile:
        if line.startswith('typeof'):
            # Format check
            if not bool(re.match('^typeof\s[a-z|_|0-9]*,\s[a-z|_|0-9]*;$', line)):
                sys.exit(0)
            typeoflist.append(line)
    inputfile.close() 
    return typeoflist

def extractPolicies(configfile):
    allpolicy = []
    inputfile = open(configfile)
    for line in inputfile:
        allpolicy.append(line)
    inputfile.close() 
    return allpolicy

def findNextLineNo(alllist, currentindex):
    nextlineno = 0
    linepattern = '^(#line)\s[0-9]+\s.*'
    # The end index is currentindex+50. That means the method tries to find the next #line line in the next
    # 50 lines. If it does not find, it will return 0 and a new line will be added.
    end = currentindex + 50 
    i = currentindex
    if end >= len(alllist):
	end = len(alllist)-1
    returnindex = currentindex
    for i in range(currentindex+1,end):
	# returnindex will determine if the next non-empty line starts with #line
	if (alllist[i].strip() !=  ''):
	    returnindex = returnindex + 1
	if bool(re.match(linepattern, alllist[i])):
	    linestr = alllist[i].split(" ")
            nextlineno = int(linestr[1])
	    break

    if (nextlineno == 0):
	# if nextlineno == 0, then initialize returnindex as well so that returnindex - currentindex!=1
	returnindex = 0
    return (nextlineno, returnindex)

def addInheritRules(typeitem, alllist, allattris):
    newpolicylist = []
    m = re.search('(?<=typeof ).*', typeitem.rstrip())
    subtype = m.group(0).strip(';').partition(', ')[0]
    obtype = m.group(0).strip(';').partition(', ')[2]
    if not subtype or not obtype:
        sys.exit(0)
    # Syntax check, obtype cannot be attribute
    if obtype in allattris:
        sys.exit(0)

    ## Search the related rules for the obtype in allpolicy
    ###TODO add binder_call in the future
    pattern0 = '^(type|typeattribute|type_transition).*(\s)'+obtype+'(\s|,\s?|_|:).*'
    pattern0_1 = '^(type_transition).*(\s)'+obtype+';.*'
    pattern_not1 = '^(type|typeattribute|type_transition).*(\s)'+obtype+'(_data_file|.+cts_.*domain).*'
    pattern1_1 = '^(type_transition)'+'.*(\s)'+obtype+'.*(\s)'+obtype+'_data_file.*'
    pattern_not2 = '^(typealias)'+'.*(\s)'+obtype+'.*;(\s)*'
    pattern2 = '^(allow|neverallow|dontaudit).*(\s)'+obtype+'(\s|:).*'
    pattern3 = '^(allow|neverallow|dontaudit).*({.*)'+obtype+'\s.*}.*'
    pattern4 = '^(allow|neverallow|dontaudit).*{.*(-\s?)'+obtype+'(\s?}|\s.*}).*'
    pattern5 = '^(allow|neverallow|dontaudit).*({.*[a-z]\s|{\s)'+obtype+'(\s?}|\s.*}).*'
    pattern6_1 = '(.*(\s).*|}| );' 
    pattern6_2 = '^(#)'
    pattern6_3 = '^(allow|neverallow|dontaudit|type|typeattribute|type_transition)'
    pattern7 = '^(#line)\s[0-9]+\s.*'
    pattern8 = '(#ignoretypeofrule)$'
    defstr = ''
    multilinepolicy=defstr
    nooflines = 0
    recentlineno = 0
    countfromlastline = 0
    nextlinemarkerno = 0
    for n,policy in enumerate(alllist):
        #check if it is a line indicating current line no
	# This is important for finding the correct line no in the correct te file for debugging purpose 
	if bool(re.match(pattern7, policy)):
	    linenostr = policy.split(" ")
  	    recentlineno = int(linenostr[1])
	    countfromlastline = 0
	else:
	    countfromlastline = countfromlastline + 1 

        # check if policy is multi-line policy
        # collapse to single line but find the total no of lines in the multiline rule for correct debugging
        if not bool(re.match(pattern6_1, policy)) and not policy.strip() == '':
	    # This means the rule is a multiline allow/neverallow/type/type_transition/typeattribute/dontaudit
	    if bool(re.match(pattern6_3,policy.strip())) and multilinepolicy.strip() == '':
                multilinepolicy = policy.strip()
	        nooflines = nooflines+1
                continue
	    # The next lines of a multiline allow rule will not have keywords but except multilinepolicy!=''
            elif not bool(re.match(pattern6_2,policy.strip())) and multilinepolicy.strip() != '':
                multilinepolicy = multilinepolicy + ' '+policy.strip()
                nooflines = nooflines+1
                continue
        if not (multilinepolicy.strip() == ''):
            nooflines = nooflines+1
            policy = multilinepolicy[:]+' '+policy.strip()+'\n'

	#check if the line has #ignoretypeofrule tag. If yes, then proceed to next line. If not, check to see if other conditions are matched.
	if bool(re.search(pattern8, policy.rstrip(), re.I|re.M)):
	    newpolicylist.append(policy)
	    continue
 	# Check if the policy line needs change because of typeof rules        
        if not policy.startswith('typeof'):
            newpolicylist.append(policy)
        if obtype in policy:
	    if bool(re.match(pattern0_1, policy)):
	        newpolicylist.pop(len(newpolicylist)-1)
                newpolicylist.append(policy.replace(' '+obtype+' ', ' '+subtype+' ').replace(' '+obtype+';', ' '+subtype+';'))
            elif ( bool(re.match(pattern0, policy)) and bool(re.match(pattern1_1,policy))) or (bool(re.match(pattern0, policy)) and not bool(re.match(pattern_not1, policy)) and not bool(re.match(pattern_not2, policy))) :
                str1 = policy.replace(' '+obtype+' ', ' '+subtype+' ').replace(' '+obtype+',', ' '+subtype+',')
		if not policy == str1:
		     # If next line is not #line , then calculate line no and add line
		     newpolicylist.append(str1)
		     nextlinemarkerno, index = findNextLineNo(alllist, n)
		     if (index-n!=1 and (nextlinemarkerno <=1  or (nextlinemarkerno != 1 and nextlinemarkerno > recentlineno + countfromlastline))):
                        newpolicylist.append("#line "+str(recentlineno + countfromlastline )+'\n');
            elif bool(re.match(pattern2, policy)) and not bool(re.match(pattern3, policy)):
                str1 = policy.replace(' '+obtype+' ', ' '+subtype+' ').replace(' '+obtype+':', ' '+subtype+':')
                if not policy == str1:
                     # If next line is not #line , then calculate line no and add line
		     newpolicylist.append(str1)
		     nextlinemarkerno, index = findNextLineNo(alllist, n)
                     if (index-n!= 1 and (nextlinemarkerno <=1  or (nextlinemarkerno != 1 and nextlinemarkerno > recentlineno + countfromlastline))):
   			newpolicylist.append("#line "+str(recentlineno + countfromlastline )+'\n');
            elif bool(re.match(pattern4, policy)):
                newpolicylist.pop(len(newpolicylist)-1)
                newpolicylist.append(policy.replace('-'+obtype, '-'+obtype+' -'+subtype))
            elif bool(re.match(pattern5, policy)):
                newpolicylist.pop(len(newpolicylist)-1)
                newpolicylist.append(policy.replace(' '+obtype, ' '+obtype+' '+subtype))
        if (nooflines > 0):
            nextlinemarkerno, index = findNextLineNo(alllist, n)
            if (index-n != 1 and (nextlinemarkerno <=1  or (nextlinemarkerno != 1 and nextlinemarkerno > recentlineno + countfromlastline))):
                newpolicylist.append("#line "+str(recentlineno+countfromlastline)+'\n')
	
	multilinepolicy = defstr
        nooflines = 0
    return newpolicylist


if __name__ == "__main__":

    start_time = time.time()
    usage = "usage: %prog [options] INPUT_FILE \n"
    usage += "This tool is to support the inheritance function for sepolicy.\n"
    usage += "If the type is defined with 'typeof' syntax in sepolicy,\n"
    usage += "it will inherit all the allow rules from the parent type.\n"

    version = "%prog " + str(__VERSION)

    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print internal operations to stdout")

    parser.add_option("-c", "--cwd", default=os.getcwd(), dest="root",
                      metavar="DIR", help="Specify a root (CWD) directory to run this from, it" \
                                           "chdirs' AFTER loading the config file")

    parser.add_option("-o", "--output", default="stdout", dest="output_file",
                      metavar="FILE", help="Specify an output file, default is stdout")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Must specify a policy config file (policy.conf)!")

    logging.basicConfig(level=logging.INFO if options.verbose == True else logging.WARN)

    output_file = sys.stdout if options.output_file == "stdout" else open(options.output_file, "w")
    logging.info("Setting output file to: " + options.output_file)

    # Extract typeof sentences
    targetlist = extractTypeof(args[0])
    allpolicy = extractPolicies(args[0])
    allattris = extractAttribute(args[0])

    # Process the typeof logic
    for item in targetlist:
        # Get related rules and dup them
        allpolicy = addInheritRules(item, allpolicy, allattris)
    # Record the rules
    for rule in allpolicy:
        output_file.write(rule)
    print("start time:"+ str(start_time)+" end time:"+str(time.time()))
    print("time taken for script:"+str(time.time()-start_time)+" seconds")
