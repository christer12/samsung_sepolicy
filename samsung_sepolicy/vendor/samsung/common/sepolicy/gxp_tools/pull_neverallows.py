import os

neverallows = open("../../gxp_neverallow/neverallows.out", "w")

for root, dirs, files in os.walk('../'):
     for file in files:
	#print(os.path.join(root, file))
        with open(os.path.join(root, file), "r") as auto:	
	 	for line in auto:
			if line.startswith("neverallow "):
				neverallows.write(line)
