#!/usr/bin/env python
import sys

# Author: William Roberts (w.roberts@sta.samsung.com)
# fixes up file permisions from audit2allow to allign with the macros defined in global_macros
# It reads from standard in and writes it results to standard out. This can be used in a pipe chain
# with audit2allow ahead of it.
#
# eg usage:
# adb shell dmesg | audit2allow | fixup.py

# This tool (fixup.py) is public domain, i.e. not copyrighted.

# Warranty Exclusion
# ------------------
# You agree that this software is a
# non-commercially developed program that may contain "bugs" (as that
# term is used in the industry) and that it may not function as intended.
# The software is licensed "as is". Samsung makes no, and hereby expressly
# disclaims all, warranties, express, implied, statutory, or otherwise
# with respect to the software, including noninfringement and the implied
# warranties of merchantability and fitness for a particular purpose.

# Limitation of Liability
# -----------------------
# In no event will Samsung be liable for any damages, including loss of data,
# lost profits, cost of cover, or other special, incidental,
# consequential, direct or indirect damages arising from the software or
# the use thereof, however caused and on any theory of liability. This
# limitation will apply even if Samsung has been advised of the possibility
# of such damage. You acknowledge that this is a reasonable allocation of
# risk.


# Mapping of macro permission sets to the macros defined in external/sepolicy/te_macros
x_file_perms = set(['getattr', 'execute', 'execute_no_trans'])
r_file_perms = set(['getattr', 'open', 'read', 'ioctl', 'lock'])
w_file_perms = set(['open', 'append', 'write'])
rx_file_perms = r_file_perms.union(x_file_perms)
ra_file_perms = r_file_perms.union(set('append'))
rw_file_perms = r_file_perms.union(w_file_perms)
rwx_file_perms = rw_file_perms.union(x_file_perms)
#link_file_perms = set(['getattr', 'link', 'unlink', 'rename'])
create_file_perms = rw_file_perms.union(rw_file_perms, set(['create', 'rename', 'setattr', 'unlink']))
r_dir_perms = set(['open', 'getattr', 'read', 'search', 'ioctl'])
w_dir_perms = set(['open', 'search', 'write', 'add_name', 'remove_name'])
ra_dir_perms = r_dir_perms.union(set(['add_name', 'write']))
rw_dir_perms = r_dir_perms.union(w_dir_perms)
create_dir_perms = rw_dir_perms.union(set(['create', 'reparent','rename', 'rmdir', 'setattr']))

# Maps the macro name (key) to a tuple of permission sets and class
perms = dict({'x_file_perms'      : (x_file_perms, "file"),
              'r_file_perms'      : (r_file_perms, "file"),
              'w_file_perms'      : (w_file_perms, "file"),
              'rx_file_perms'     : (rx_file_perms, "file"),
              'ra_file_perms'     : (ra_file_perms, "file"),
              'rw_file_perms'     : (rw_file_perms, "file"),
              'rwx_file_perms'    : (rwx_file_perms, "file"),
              'create_file_perms' : (create_file_perms, "file"),
              'r_dir_perms'       : (r_dir_perms, "dir"),
              'w_dir_perms'       : (w_dir_perms, "dir"),
              'ra_dir_perms'      : (ra_dir_perms, "dir"),
              'rw_dir_perms'      : (rw_dir_perms, "dir"),
              'create_dir_perms'  : (create_dir_perms, "dir")
               })

for line in sys.stdin:

    line = line.rstrip()
    if line.startswith('#'):
        print line
        continue

    chunks = line.split()

    if len(chunks) < 4:
        print(line)
        continue

    rule = chunks[0]
    domain = chunks[1]

    setype = None
    seclass = None
    for chunk in chunks:
        if ":" in chunk:
            setype = chunk.split(":")[0]
            seclass = chunk.split(":")[1]

    if setype == None:
        print(line)
        continue

    i = 3
    reqperms = set()
    while(i < len(chunks)):
        item = chunks[i]
        if "{" in item or "}" in item:
            i += 1
            continue

        if ";" in item:
            item = item.strip(";")
        reqperms.add(item)
        i += 1

    bestmatch = None
    bestmatchcnt = 0
    macrovalue = None
    for permkey in perms:
        permset = (perms[permkey])[0]
        permclass = (perms[permkey])[1]

        common = reqperms.intersection(permset)
        if bestmatch == None:
            if len(common) > 0 and permclass in seclass:
                bestmatch = permset
                bestmatchcount = len(common)
                macrovalue = permkey
        else:
            if len(common) >= bestmatchcount:
                if permclass in seclass:
                    currentlyassignedset = len((perms[macrovalue])[0])
                    possiblesmallerset = len(permset)
                    if currentlyassignedset > possiblesmallerset:
                        bestmatch = permset
                        bestmatchcount = len(common)
                        macrovalue = permkey

    if bestmatch == None:
        print line
    else:
        print(rule + " " + domain + " " + setype + ":" + seclass + " " + macrovalue + ";")
