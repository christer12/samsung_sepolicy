from collections import OrderedDict

file = open("../gxp_outs/read_ops.out", 'r')
file_out = open("../gxp_outs/no_duplicates_read_ops.out", 'w')
ops_list = []

for word in file:
	ops_list.insert(0, word)

ops_list.sort()
list = OrderedDict.fromkeys(ops_list)	

#file_out.write(str(list))

for op in list:
	file_out.write(op.rstrip() +"','")
