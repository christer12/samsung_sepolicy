obj_read = open("../gxp_outs/target_object_trusted.out", 'w')

stage = 0
skip = 0

with open('../gxp_outs/reads_by_trusted.out') as f:
        for line in f:
		for c in line:
			if c == ' ' and stage == 0:
				stage = 1
				continue
			elif c == ' ' and stage == 1 and skip == 0:
				stage = 2
				continue
			elif c == ' ' and stage == 3:
				stage = 4
				continue
			elif stage == 4:
				break						
			elif c == ':' and stage == 2:
				stage = 3
				obj_read.write(c)
				continue
			elif c == '{' and stage == 1 and skip == 0:
				skip = 1
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
			elif stage == 2:
				obj_read.write(c)
			elif c == '{' and stage == 3 and skip == 0:
				skip = 1
				obj_read.write(c)
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
				obj_read.write(c)
			elif stage == 3:
				obj_read.write(c)
				
		obj_read.write('\n')
		skip = 0
		stage = 0	
f.close()


obj_written = open("../gxp_outs/target_object_untrusted.out", 'w')

stage = 0
skip = 0

with open('../gxp_outs/writes_by_untrusted.out') as f:
        for line in f:
		for c in line:
			if c == ' ' and stage == 0:
				stage = 1
				continue
			elif c == ' ' and stage == 1 and skip == 0:
				stage = 2
				continue
			elif c == ' ' and stage == 3:
				stage = 4
				continue
			elif stage == 4:
				break						
			elif c == ':' and stage == 2:
				stage = 3
				obj_written.write(c)
				continue
			elif c == '{' and stage == 1 and skip == 0:
				skip = 1
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
			elif stage == 2:
				obj_written.write(c)
			elif c == '{' and stage == 3 and skip == 0:
				skip = 1
				obj_written.write(c)
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
				obj_written.write(c)
			elif stage == 3:
				obj_written.write(c)
				
		obj_written.written('\n')
		skip = 0
		stage = 0	

f.close()
