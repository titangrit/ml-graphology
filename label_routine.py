# This file is not supposed to be here.
# But we used this anyway for labeling! ¯\_(ツ)_/¯
#

import os

def determine_trait_1(baseline_angle, slant_angle):
	# trait_1 = emotional stability | 1 = stable, 0 = not stable
	if (slant_angle == 0 or slant_angle == 4 or slant_angle == 6 or baseline_angle == 0):
		return 0
	else:
		return 1
	
def determine_trait_2(letter_size, pen_pressure):
	# trait_2 = mental energy or will power | 1 = high or average, 0 = low
	if ((pen_pressure == 0 or pen_pressure == 2) or (letter_size == 1 or letter_size == 2)):
		return 1
	else:
		return 0
	
def determine_trait_3(top_margin, letter_size):
	# trait_3 = modesty | 1 = observed, 0 = not observed (not necessarily the opposite)
	if (top_margin == 0 or  letter_size == 1):
		return 1
	else:
		return 0
	
def determine_trait_4(line_spacing, word_spacing):
	# trait_4 = personal harmony and flexibility | 1 = harmonious, 0 = non harmonious
	if (line_spacing == 2 and word_spacing == 2):
		return 1
	else:
		return 0
	
def determine_trait_5(top_margin, slant_angle):
	# trait_5 = lack of discipline | 1 = observed, 0 = not observed (not necessarily the opposite)
	if (top_margin == 1 and slant_angle == 6):
		return 1
	else:
		return 0
	
def determine_trait_6(letter_size, line_spacing):
	# trait_6 = poor concentration power | 1 = observed, 0 = not observed (not necessarily the opposite)
	if (letter_size == 0 and line_spacing == 1):
		return 1
	else:
		return 0
	
def determine_trait_7(letter_size, word_spacing):
	# trait_7 = non communicativeness | 1 = observed, 0 = not observed (not necessarily the opposite)
	if (letter_size == 1 and word_spacing == 0):
		return 1
	else:
		return 0
	
def determine_trait_8(line_spacing, word_spacing):
	# trait_8 = social isolation | 1 = observed, 0 = not observed (not necessarily the opposite)
	if (word_spacing == 0 or line_spacing == 0):
		return 1
	else:
		return 0


if os.path.isfile("label_list"):
	print ("Error: label_list already exists.")

elif os.path.isfile("feature_list"):
	print ("Info: feature_list found.")
	with open("feature_list", "r") as features, open("label_list", "a") as labels:
		for line in features:
			content = line.split()
			
			baseline_angle = float(content[0])
			top_margin = float(content[1])
			letter_size = float(content[2])
			line_spacing = float(content[3])
			word_spacing = float(content[4])
			pen_pressure = float(content[5])
			slant_angle = float(content[6])
			page_id = content[7]
			
			# trait_1 = emotional stability | 1 = stable, 0 = not stable
			trait_1 = determine_trait_1(baseline_angle, slant_angle)
			
			# trait_2 = mental energy or will power | 1 = high or average, 0 = low
			trait_2 = determine_trait_2(letter_size, pen_pressure)
			
			# trait_3 = modesty | 1 = observed, 0 = not observed (not necessarily the opposite)
			trait_3 = determine_trait_3(top_margin, letter_size)
			
			# trait_4 = personal harmony and flexibility | 1 = harmonious, 0 = non harmonious
			trait_4 = determine_trait_4(line_spacing, word_spacing)
			
			# trait_5 = lack of discipline | 1 = observed, 0 = not observed (not necessarily the opposite)
			trait_5 = determine_trait_5(top_margin, slant_angle)
			
			# trait_6 = poor concentration power | 1 = observed, 0 = not observed (not necessarily the opposite)
			trait_6 = determine_trait_6(letter_size, line_spacing)
			
			# trait_7 = non communicativeness | 1 = observed, 0 = not observed (not necessarily the opposite)
			trait_7 = determine_trait_7(letter_size, word_spacing)
			
			# trait_8 = social isolation | 1 = observed, 0 = not observed (not necessarily the opposite)
			trait_8 = determine_trait_8(line_spacing, word_spacing)
			
			labels.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (str(baseline_angle), str(top_margin), str(letter_size), str(line_spacing), str(word_spacing), str(pen_pressure), str(slant_angle)))
			labels.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (str(trait_1), str(trait_2), str(trait_3), str(trait_4), str(trait_5), str(trait_6), str(trait_7), str(trait_8)))
			labels.write("%s" % str(page_id))
			print>>labels, ''
	print "Done!"
	
else:
	print ("Error: feature_list file not found.")