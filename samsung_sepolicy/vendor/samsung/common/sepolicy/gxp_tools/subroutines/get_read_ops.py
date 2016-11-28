 
access_vectors = open("../access_vectors_GXP", 'r')
write_ops = open("../gxp_outs/read_ops.out", 'w')

#untrusted_list = ['untrusted_app.te', 'app.te', './knox_common/knox_untrusted_app.te']

#write_ops = ['write', 'ioctl']

for line in access_vectors:
	#print len(line.split())
	if (len(line.split()) >= 2):
		#print line.split()[1]
		if (line.split()[1] == 'R' or line.split()[1] == 'RW'):
			write_ops.write(line.split()[0]+ '\n') 
