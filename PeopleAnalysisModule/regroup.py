f = open("Human_prop/groups")
f2 = open("Human_prop/groups2","w")
output=""
for line in f:
	if len(line)>2:
		output+=line[0]+"\n"
f2.write(output)
f.close()
f2.close()
