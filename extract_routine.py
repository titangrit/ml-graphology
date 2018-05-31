import os
import extract

os.chdir("images");
files = [f for f in os.listdir('.') if os.path.isfile(f)]
os.chdir("..")

page_ids = []
if os.path.isfile("raw_feature_list"):
	print ("Info: raw_feature_list already exists.")
	with open("raw_feature_list", "r") as label:
		for line in label:
			content = line.split()
			page_id = content[-1]
			page_ids.append(page_id)
		
with open("raw_feature_list", "a") as label:
	count = len(page_ids)
	for file_name in files:
		if(file_name in page_ids):
			continue
		features = extract.start(file_name)
		features.append(file_name)
		for i in features:
			label.write("%s\t" % i)
		print>>label, ''
		count += 1
		progress = (count*100)/len(files)
		print str(count)+' '+file_name+' '+str(progress)+'%'
	print "Done!"