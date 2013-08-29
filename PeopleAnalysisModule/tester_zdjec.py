import Image
file = open("training_data2.csv")
for line in file:
		url =line.split(";")[0]
		try:
			img = Image.open(url)
			if img.size!=(180,180):
				print img.size , url
		except:
			print "tego pliku nie dalo sie otworzyc"
			print url
