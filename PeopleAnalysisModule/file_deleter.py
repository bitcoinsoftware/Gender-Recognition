import os
folder = "tmp"
files = os.listdir(folder)
for file in files: os.remove(folder+"/"+file)
