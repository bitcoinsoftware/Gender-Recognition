f = open("results")
i=0
femail_numb = 0
age =0
for line in f:
    result = eval(line)
    try:
        femail_numb+=result["gender"]
        age += result["age"]
        i+=1
    except:
        pass

print "gender" , femail_numb , i , femail_numb/float(i)
print "age" , age/float(i)
    
