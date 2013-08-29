import datetime, subprocess, os
path ="7.pgm"
txt_url =path+ ".txt"
size= (92, 112)
a = datetime.datetime.now()
command="./Recognizer2 "+"fisherfaces_position.yml "+path+ " "+str(size[0])+" "+str(size[1])
for i in range(10):
	os.system(command)
	position = eval(open(txt_url).read()) 
	 	
b= datetime.datetime.now()

for i in range(10):
    proc = subprocess.Popen(command,  stdout = subprocess.PIPE)
    a = proc.communicate()	
    
c = detetime.datetime.now()
t1 = a-b
t2 = b-c

print a
print b
