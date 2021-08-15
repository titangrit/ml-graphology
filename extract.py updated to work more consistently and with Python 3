import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

# please don't worry about these variables now
ANCHOR_POINT = 6000
MIDZONE_THRESHOLD = 15000
MIN_HANDWRITING_HEIGHT_PIXEL = 20

# Features are defined here as global variables
BASELINE_ANGLE = 0.0
TOP_MARGIN = 0.0
LETTER_SIZE = 0.0
LINE_SPACING = 0.0
WORD_SPACING = 0.0
PEN_PRESSURE = 0.0
SLANT_ANGLE = 0.0

''' function for bilateral filtering '''
def bilateralFilter(image, d):
	image = cv2.bilateralFilter(image,d,50,50)
	return image

''' function for median filtering '''
def medianFilter(image, d):
	image = cv2.medianBlur(image,d)
	return image

''' function for INVERTED binary threshold '''
def threshold(image, t):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret,image = cv2.threshold(image,t,255,cv2.THRESH_BINARY_INV)
	return image

''' function for dilation of objects in the image '''
def dilate(image, kernalSize):
	kernel = np.ones(kernalSize, np.uint8)
	image = cv2.dilate(image, kernel, iterations=1)
	return image

''' function for erosion of objects in the image '''
def erode(image, kernalSize):
	kernel = np.ones(kernalSize, np.uint8)
	image = cv2.erode(image, kernel, iterations=1)
	return image

''' function for finding contours and straightening them horizontally. Straightened lines will give better result with horizontal projections. '''
def straighten(image):

	global BASELINE_ANGLE

	angle = 0.0
	angle_sum = 0.0
	contour_count = 0

	# these four variables are not being used, please ignore
	positive_angle_sum = 0.0 #downward
	negative_angle_sum = 0.0 #upward
	positive_count = 0
	negative_count = 0

	# apply bilateral filter
	filtered = bilateralFilter(image, 3)
	#cv2.imshow('filtered',filtered)

	# convert to grayscale and binarize the image by INVERTED binary thresholding
	thresh = threshold(filtered, 120)
	#cv2.imshow('thresh',thresh)

	# dilate the handwritten lines in image with a suitable kernel for contour operation
	dilated = dilate(thresh, (5 ,100))
	#cv2.imshow('dilated',dilated)

	ctrs,hier = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# line called im2,ctrs,hier before

	for i, ctr in enumerate(ctrs):
		x, y, w, h = cv2.boundingRect(ctr)

		# We can be sure the contour is not a line if height > width or height is < 20 pixels. Here 20 is arbitrary.
		if h>w or h<MIN_HANDWRITING_HEIGHT_PIXEL:
			continue

		# We extract the region of interest/contour to be straightened.
		roi = image[y:y+h, x:x+w]
		#rows, cols = ctr.shape[:2]

		# If the length of the line is less than one third of the document width, especially for the last line,
		# ignore because it may yeild inacurate baseline angle which subsequently affects proceeding features.

		if w < image.shape[1]/2 :
			roi = 255
			image[y:y+h, x:x+w] = roi
			continue

		# minAreaRect is necessary for straightening
		rect = cv2.minAreaRect(ctr)
		center = rect[0]
		angle = rect[2]
		#print "original: "+str(i)+" "+str(angle)
		# I actually gave a thought to this but hard to remember anyway!
		if angle < -45.0:
			angle += 90.0;
		#print "+90 "+str(i)+" "+str(angle)

		rot = cv2.getRotationMatrix2D(((x+w)/2,(y+h)/2), angle, 1)
		#extract = cv2.warpAffine(roi, rot, (w,h), borderMode=cv2.BORDER_TRANSPARENT)
		extract = cv2.warpAffine(roi, rot, (w,h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
		#cv2.imshow('warpAffine:'+str(i),extract)

		# image is overwritten with the straightened contour
		image[y:y+h, x:x+w] = extract
		'''
		# Please Ignore. This is to draw visual representation of the contour rotation.
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(display,[box],0,(0,0,255),1)
		cv2.rectangle(display,(x,y),( x + w, y + h ),(0,255,0),1)
		'''
		#print angle
		angle_sum += angle
		contour_count += 1
	'''
		# sum of all the angles of downward baseline
		if(angle>0.0):
			positive_angle_sum += angle
			positive_count += 1
		# sum of all the angles of upward baseline
		else:
			negative_angle_sum += angle
			negative_count += 1

	if(positive_count == 0): positive_count = 1
	if(negative_count == 0): negative_count = 1
	average_positive_angle = positive_angle_sum / positive_count
	average_negative_angle = negative_angle_sum / negative_count
	print "average_positive_angle: "+str(average_positive_angle)
	print "average_negative_angle: "+str(average_negative_angle)

	if(abs(average_positive_angle) > abs(average_negative_angle)):
		average_angle = average_positive_angle
	else:
		average_angle = average_negative_angle

	print "average_angle: "+str(average_angle)
	'''
	#cv2.imshow('contours', display)

	# mean angle of the contours (not lines) is found
	if contour_count == 0.0:
		mean_angle = angle_sum
	else:
		mean_angle = angle_sum / contour_count

	BASELINE_ANGLE = mean_angle
	#print ("Average baseline angle: "+str(mean_angle))
	return image

''' function to calculate horizontal projection of the image pixel rows and return it '''
def horizontalProjection(img):
    # Return a list containing the sum of the pixels in each row
    (h, w) = img.shape[:2]
    sumRows = []
    for j in range(h):
        row = img[j:j+1, 0:w] # y1:y2, x1:x2
        sumRows.append(np.sum(row))
    return sumRows

''' function to calculate vertical projection of the image pixel columns and return it '''
def verticalProjection(img):
    # Return a list containing the sum of the pixels in each column
    (h, w) = img.shape[:2]
    sumCols = []
    for j in range(w):
        col = img[0:h, j:j+1] # y1:y2, x1:x2
        sumCols.append(np.sum(col))
    return sumCols

''' function to extract lines of handwritten text from the image using horizontal projection '''
def extractLines(img):

	global LETTER_SIZE
	global LINE_SPACING
	global TOP_MARGIN

	# apply bilateral filter
	filtered = bilateralFilter(img, 5)

	# convert to grayscale and binarize the image by INVERTED binary thresholding
	# it's better to clear unwanted dark areas at the document left edge and use a high threshold value to preserve more text pixels
	thresh = threshold(filtered, 160)
	#cv2.imshow('thresh', lthresh)

	# extract a python list containing values of the horizontal projection of the image into 'hp'
	hpList = horizontalProjection(thresh)

	# Extracting 'Top Margin' feature.
	topMarginCount = 0
	for sum in hpList:
		# sum can be strictly 0 as well. Anyway we take 0 and 255.
		if(sum<=255):
			topMarginCount += 1
		else:
			break

	#print "(Top margin row count: "+str(topMarginCount)+")"

	# FIRST we extract the straightened contours from the image by looking at occurance of 0's in the horizontal projection.
	lineTop = 0
	lineBottom = 0
	spaceTop = 0
	spaceBottom = 0
	indexCount = 0
	setLineTop = True
	setSpaceTop = True
	includeNextSpace = True
	space_zero = [] # stores the amount of space between lines
	lines = [] # a 2D list storing the vertical start index and end index of each contour

	# we are scanning the whole horizontal projection now
	for i, sum in enumerate(hpList):
		# sum being 0 means blank space
		if(sum==0):
			if(setSpaceTop):
				spaceTop = indexCount
				setSpaceTop = False # spaceTop will be set once for each start of a space between lines
			indexCount += 1
			spaceBottom = indexCount
			if(i<len(hpList)-1): # this condition is necessary to avoid array index out of bound error
				if(hpList[i+1]==0): # if the next horizontal projectin is 0, keep on counting, it's still in blank space
					continue
			# we are using this condition if the previous contour is very thin and possibly not a line
			if(includeNextSpace):
				space_zero.append(spaceBottom-spaceTop)
			else:
				if (len(space_zero)==0):
					previous = 0
				else:
					previous = space_zero.pop()
				space_zero.append(previous + spaceBottom-lineTop)
			setSpaceTop = True # next time we encounter 0, it's begining of another space so we set new spaceTop

		# sum greater than 0 means contour
		if(sum>0):
			if(setLineTop):
				lineTop = indexCount
				setLineTop = False # lineTop will be set once for each start of a new line/contour
			indexCount += 1
			lineBottom = indexCount
			if(i<len(hpList)-1): # this condition is necessary to avoid array index out of bound error
				if(hpList[i+1]>0): # if the next horizontal projectin is > 0, keep on counting, it's still in contour
					continue

				# if the line/contour is too thin <10 pixels (arbitrary) in height, we ignore it.
				# Also, we add the space following this and this contour itself to the previous space to form a bigger space: spaceBottom-lineTop.
				if(lineBottom-lineTop<20):
					includeNextSpace = False
					setLineTop = True # next time we encounter value > 0, it's begining of another line/contour so we set new lineTop
					continue
			includeNextSpace = True # the line/contour is accepted, new space following it will be accepted

			# append the top and bottom horizontal indices of the line/contour in 'lines'
			lines.append([lineTop, lineBottom])
			setLineTop = True # next time we encounter value > 0, it's begining of another line/contour so we set new lineTop

	'''
	# Printing the values we found so far.
	for i, line in enumerate(lines):
		print
		print i
		print line[0]
		print line[1]
		print len(hpList[line[0]:line[1]])
		print hpList[line[0]:line[1]]

	for i, line in enumerate(lines):
		cv2.imshow("line "+str(i), img[line[0]:line[1], : ])
	'''

	# SECOND we extract the very individual lines from the lines/contours we extracted above.
	fineLines = [] # a 2D list storing the horizontal start index and end index of each individual line
	for i, line in enumerate(lines):

		anchor = line[0] # 'anchor' will locate the horizontal indices where horizontal projection is > ANCHOR_POINT for uphill or < ANCHOR_POINT for downhill(ANCHOR_POINT is arbitrary yet suitable!)
		anchorPoints = [] # python list where the indices obtained by 'anchor' will be stored
		upHill = True # it implies that we expect to find the start of an individual line (vertically), climbing up the histogram
		downHill = False # it implies that we expect to find the end of an individual line (vertically), climbing down the histogram
		segment = hpList[line[0]:line[1]] # we put the region of interest of the horizontal projection of each contour here

		for j, sum in enumerate(segment):
			if(upHill):
				if(sum<ANCHOR_POINT):
					anchor += 1
					continue
				anchorPoints.append(anchor)
				upHill = False
				downHill = True
			if(downHill):
				if(sum>ANCHOR_POINT):
					anchor += 1
					continue
				anchorPoints.append(anchor)
				downHill = False
				upHill = True

		#print anchorPoints

		# we can ignore the contour here
		if(len(anchorPoints)<2):
			continue

		'''
		# the contour turns out to be an individual line
		if(len(anchorPoints)<=3):
			fineLines.append(line)
			continue
		'''
		# len(anchorPoints) > 3 meaning contour composed of multiple lines
		lineTop = line[0]
		for x in range(1, len(anchorPoints)-1, 2):
			# 'lineMid' is the horizontal index where the segmentation will be done
			lineMid = (anchorPoints[x]+anchorPoints[x+1])/2
			lineBottom = lineMid
			# line having height of pixels <20 is considered defects, so we just ignore it
			# this is a weakness of the algorithm to extract lines (anchor value is ANCHOR_POINT, see for different values!)
			if(lineBottom-lineTop < 20):
				continue
			fineLines.append([lineTop, lineBottom])
			lineTop = lineBottom
		if(line[1]-lineTop < 20):
			continue
		fineLines.append([lineTop, line[1]])

	# LINE SPACING and LETTER SIZE will be extracted here
	# We will count the total number of pixel rows containing upper and lower zones of the lines and add the space_zero/runs of 0's(excluding first and last of the list ) to it.
	# We will count the total number of pixel rows containing midzones of the lines for letter size.
	# For this, we set an arbitrary (yet suitable!) threshold MIDZONE_THRESHOLD = 15000 in horizontal projection to identify the midzone containing rows.
	# These two total numbers will be divided by number of lines (having at least one row>MIDZONE_THRESHOLD) to find average line spacing and average letter size.
	space_nonzero_row_count = 0
	midzone_row_count = 0
	lines_having_midzone_count = 0
	flag = False
	for i, line in enumerate(fineLines):
		segment = hpList[line[0]:line[1]]
		for j, sum in enumerate(segment):
			if(sum<MIDZONE_THRESHOLD):
				space_nonzero_row_count += 1
			else:
				midzone_row_count += 1
				flag = True

		# This line has contributed at least one count of pixel row of midzone
		if(flag):
			lines_having_midzone_count += 1
			flag = False

	# error prevention ^-^
	if(lines_having_midzone_count == 0): lines_having_midzone_count = 1


	total_space_row_count = space_nonzero_row_count + np.sum(space_zero[1:-1]) #excluding first and last entries: Top and Bottom margins
	# the number of spaces is 1 less than number of lines but total_space_row_count contains the top and bottom spaces of the line
	average_line_spacing = float(total_space_row_count) / lines_having_midzone_count
	average_letter_size = float(midzone_row_count) / lines_having_midzone_count
	# letter size is actually height of the letter and we are not considering width
	LETTER_SIZE = average_letter_size
	# error prevention ^-^
	if(average_letter_size == 0): average_letter_size = 1
	# We can't just take the average_line_spacing as a feature directly. We must take the average_line_spacing relative to average_letter_size.
	# Let's take the ratio of average_line_spacing to average_letter_size as the LINE SPACING, which is perspective to average_letter_size.
	relative_line_spacing = average_line_spacing / average_letter_size
	LINE_SPACING = relative_line_spacing

	# Top marging is also taken relative to average letter size of the handwritting
	relative_top_margin = float(topMarginCount) / average_letter_size
	TOP_MARGIN = relative_top_margin

	'''
	# showing the final extracted lines
	for i, line in enumerate(fineLines):
		cv2.imshow("line "+str(i), img[line[0]:line[1], : ])
	'''

	#print space_zero
	#print lines
	#print fineLines
	#print midzone_row_count
	#print total_space_row_count
	#print len(hpList)
	#print average_line_spacing
	#print lines_having_midzone_count
	#print i
	'''
	print ("Average letter size: "+str(average_letter_size))
	print ("Top margin relative to average letter size: "+str(relative_top_margin))
	print ("Average line spacing relative to average letter size: "+str(relative_line_spacing))
	'''
	return fineLines

''' function to extract words from the lines using vertical projection '''
def extractWords(image, lines):

	global LETTER_SIZE
	global WORD_SPACING

	# apply bilateral filter
	filtered = bilateralFilter(image, 5)

	# convert to grayscale and binarize the image by INVERTED binary thresholding
	thresh = threshold(filtered, 180)
	#cv2.imshow('thresh', wthresh)

	# Width of the whole document is found once.
	width = thresh.shape[1]
	space_zero = [] # stores the amount of space between words
	words = [] # a 2D list storing the coordinates of each word: y1, y2, x1, x2

	# Isolated words or components will be extacted from each line by looking at occurance of 0's in its vertical projection.
	for i, line in enumerate(lines):
		extract = thresh[line[0]:line[1], 0:width] # y1:y2, x1:x2
		vp = verticalProjection(extract)
		#print i
		#print vp

		wordStart = 0
		wordEnd = 0
		spaceStart = 0
		spaceEnd = 0
		indexCount = 0
		setWordStart = True
		setSpaceStart = True
		includeNextSpace = True
		spaces = []

		# we are scanning the vertical projection
		for j, sum in enumerate(vp):
			# sum being 0 means blank space
			if(sum==0):
				if(setSpaceStart):
					spaceStart = indexCount
					setSpaceStart = False # spaceStart will be set once for each start of a space between lines
				indexCount += 1
				spaceEnd = indexCount
				if(j<len(vp)-1): # this condition is necessary to avoid array index out of bound error
					if(vp[j+1]==0): # if the next vertical projectin is 0, keep on counting, it's still in blank space
						continue

				# we ignore spaces which is smaller than half the average letter size
				if((spaceEnd-spaceStart) > int(LETTER_SIZE/2)):
					spaces.append(spaceEnd-spaceStart)

				setSpaceStart = True # next time we encounter 0, it's begining of another space so we set new spaceStart

			# sum greater than 0 means word/component
			if(sum>0):
				if(setWordStart):
					wordStart = indexCount
					setWordStart = False # wordStart will be set once for each start of a new word/component
				indexCount += 1
				wordEnd = indexCount
				if(j<len(vp)-1): # this condition is necessary to avoid array index out of bound error
					if(vp[j+1]>0): # if the next horizontal projectin is > 0, keep on counting, it's still in non-space zone
						continue

				# append the coordinates of each word/component: y1, y2, x1, x2 in 'words'
				# we ignore the ones which has height smaller than half the average letter size
				# this will remove full stops and commas as an individual component
				count = 0
				for k in range(line[1]-line[0]):
					row = thresh[line[0]+k:line[0]+k+1, wordStart:wordEnd] # y1:y2, x1:x2
					if(np.sum(row)):
						count += 1
				if(count > int(LETTER_SIZE/2)):
					words.append([line[0], line[1], wordStart, wordEnd])

				setWordStart = True # next time we encounter value > 0, it's begining of another word/component so we set new wordStart

		space_zero.extend(spaces[1:-1])

	#print space_zero
	space_columns = np.sum(space_zero)
	space_count = len(space_zero)
	if(space_count == 0):
		space_count = 1
	average_word_spacing = float(space_columns) / space_count
	if LETTER_SIZE == 0.0:
		relative_word_spacing = average_word_spacing
	else:
		relative_word_spacing = average_word_spacing / LETTER_SIZE
	#used to be divideed but LETTER_SIZE
	WORD_SPACING = relative_word_spacing
	#print "Average word spacing: "+str(average_word_spacing)
	#print ("Average word spacing relative to average letter size: "+str(relative_word_spacing))

	return words

''' function to determine the average slant of the handwriting '''
def extractSlant(img, words):

	global SLANT_ANGLE
	'''
	0.01 radian = 0.5729578 degree :: I had to put this instead of 0.0 becuase there was a bug yeilding inacurate value which I could not figure out!
	5 degree = 0.0872665 radian :: Hardly noticeable or a very little slant
	15 degree = 0.261799 radian :: Easily noticeable or average slant
	30 degree = 0.523599 radian :: Above average slant
	45 degree = 0.785398 radian :: Extreme slant
	'''
	# We are checking for 9 different values of angle
	theta = [-0.785398, -0.523599, -0.261799, -0.0872665, 0.01, 0.0872665, 0.261799, 0.523599, 0.785398]
	#theta = [-0.785398, -0.523599, -0.436332, -0.349066, -0.261799, -0.174533, -0.0872665, 0, 0.0872665, 0.174533, 0.261799, 0.349066, 0.436332, 0.523599, 0.785398]

	# Corresponding index of the biggest value in s_function will be the index of the most likely angle in 'theta'
	s_function = [0.0] * 9
	count_ = [0]*9

	# apply bilateral filter
	filtered = bilateralFilter(img, 5)

	# convert to grayscale and binarize the image by INVERTED binary thresholding
	# it's better to clear unwanted dark areas at the document left edge and use a high threshold value to preserve more text pixels
	thresh = threshold(filtered, 180)
	#cv2.imshow('thresh', lthresh)

	# loop for each value of angle in theta
	for i, angle in enumerate(theta):
		s_temp = 0.0 # overall sum of the functions of all the columns of all the words!
		count = 0 # just counting the number of columns considered to contain a vertical stroke and thus contributing to s_temp

		#loop for each word
		for j, word in enumerate(words):
			original = thresh[word[0]:word[1], word[2]:word[3]] # y1:y2, x1:x2

			height = word[1]-word[0]
			width = word[3]-word[2]

			# the distance in pixel we will shift for affine transformation
			# it's divided by 2 because the uppermost point and the lowermost points are being equally shifted in opposite directions
			shift = (math.tan(angle) * height) / 2

			# the amount of extra space we need to add to the original image to preserve information
			# yes, this is adding more number of columns but the effect of this will be negligible
			pad_length = abs(int(shift))

			# create a new image that can perfectly hold the transformed and thus widened image
			blank_image = np.zeros((height,width+pad_length*2,3), np.uint8)
			new_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
			new_image[:, pad_length:width+pad_length] = original

			# points to consider for affine transformation
			(height, width) = new_image.shape[:2]
			x1 = width/2
			y1 = 0
			x2 = width/4
			y2 = height
			x3 = 3*width/4
			y3 = height

			pts1 = np.float32([[x1,y1],[x2,y2],[x3,y3]])
			pts2 = np.float32([[x1+shift,y1],[x2-shift,y2],[x3-shift,y3]])
			M = cv2.getAffineTransform(pts1,pts2)
			deslanted = cv2.warpAffine(new_image,M,(width,height))

			# find the vertical projection on the transformed image
			vp = verticalProjection(deslanted)

			# loop for each value of vertical projection, which is for each column in the word image
			for k, sum in enumerate(vp):
				# the columns is empty
				if(sum == 0):
					continue

				# this is the number of foreground pixels in the column being considered
				num_fgpixel = sum / 255

				# if number of foreground pixels is less than onethird of total pixels, it is not a vertical stroke so we can ignore
				if(num_fgpixel < int(height/3)):
					continue

				# the column itself is extracted, and flattened for easy operation
				column = deslanted[0:height, k:k+1]
				column = column.flatten()

				# now we are going to find the distance between topmost pixel and bottom-most pixel
				# l counts the number of empty pixels from top until and upto a foreground pixel is discovered
				for l, pixel in enumerate(column):
					if(pixel==0):
						continue
					break
				# m counts the number of empty pixels from bottom until and upto a foreground pixel is discovered
				for m, pixel in enumerate(column[::-1]):
					if(pixel==0):
						continue
					break

				# the distance is found as delta_y, I just followed the naming convention in the research paper I followed
				delta_y = height - (l+m)

				# please refer the research paper for more details of this function, anyway it's nothing tricky
				h_sq = (float(num_fgpixel)/delta_y)**2

				# I am multiplying by a factor of num_fgpixel/height to the above function to yeild better result
				# this will also somewhat negate the effect of adding more columns and different column counts in the transformed image of the same word
				h_wted = (h_sq * num_fgpixel) / height

				'''
				# just printing
				if(j==0):
					print column
					print str(i)+' h_sq='+str(h_sq)+' h_wted='+str(h_wted)+' num_fgpixel='+str(num_fgpixel)+' delta_y='+str(delta_y)
				'''

				# add up the values from all the loops of ALL the columns of ALL the words in the image
				s_temp += h_wted

				count += 1

			'''
			if(j==0):
				#plt.subplot(),plt.imshow(deslanted),plt.title('Output '+str(i))
				#plt.show()
				cv2.imshow('Output '+str(i)+str(j), deslanted)
				#print vp
				#print 'line '+str(i)+' '+str(s_temp)
				#print
			'''

		s_function[i] = s_temp
		count_[i] = count

	# finding the largest value and corresponding index
	max_value = 0.0
	max_index = 4
	for index, value in enumerate(s_function):
		#print str(index)+" "+str(value)+" "+str(count_[index])
		if(value > max_value):
			max_value = value
			max_index = index

	# We will add another value 9 manually to indicate irregular slant behaviour.
	# This will be seen as value 4 (no slant) but 2 corresponding angles of opposite sign will have very close values.
	if(max_index == 0):
		angle = 45
		result =  " : Extremely right slanted"
	elif(max_index == 1):
		angle = 30
		result = " : Above average right slanted"
	elif(max_index == 2):
		angle = 15
		result = " : Average right slanted"
	elif(max_index == 3):
		angle = 5
		result = " : A little right slanted"
	elif(max_index == 5):
		angle = -5
		result = " : A little left slanted"
	elif(max_index == 6):
		angle = -15
		result = " : Average left slanted"
	elif(max_index == 7):
		angle = -30
		result = " : Above average left slanted"
	elif(max_index == 8):
		angle = -45
		result = " : Extremely left slanted"
	elif(max_index == 4):
		if s_function[3] == 0.0:
			p = s_function[4] # / s_function[3]
			q = s_function[4] # / s_function[5]
		else:
			p = s_function[4] / s_function[3]
			q = s_function[4] / s_function[5]
		#print 'p='+str(p)+' q='+str(q)
		# the constants here are abritrary but I think suits the best
		if((p <= 1.2 and q <= 1.2) or (p > 1.4 and q > 1.4)):
			angle = 0
			result = " : No slant"
		elif((p <= 1.2 and q-p > 0.4) or (q <= 1.2 and p-q > 0.4)):
			angle = 0
			result = " : No slant"
		else:
			max_index = 9
			angle = 180
			result =  " : Irregular slant behaviour"


		if angle == 0:
			print ("\n************************************************")
			print ("Slant determined to be straight.")
		else:
			print ("\n************************************************")
			print ("Slant determined to be irregular.")
		cv2.imshow("Check Image", img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		type = input("Press enter if okay, else enter c to change: ")
		if type=='c':
			if angle == 0:
				angle = 180
				result =  " : Irregular Slant"
				print ("Set as"+result)
				print ("************************************************\n")
			else:
				angle = 0
				result = " : Straight/No Slant"
				print ("Set as"+result)
				print ("************************************************\n")
		else:
			print ("No Change!")
			print ("************************************************\n")

	SLANT_ANGLE = angle
	#print ("Slant angle(degree): "+str(SLANT_ANGLE)+result)
	return

''' function to extract average pen pressure of the handwriting '''
def barometer(image):

	global PEN_PRESSURE

	# it's extremely necessary to convert to grayscale first
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# inverting the image pixel by pixel individually. This costs the maximum time and processing in the entire process!
	h, w = image.shape[:]
	inverted = image
	for x in range(h):
		for y in range(w):
			inverted[x][y] = 255 - image[x][y]

	#cv2.imshow('inverted', inverted)

	# bilateral filtering
	filtered = bilateralFilter(inverted, 3)

	# binary thresholding. Here we use 'threshold to zero' which is crucial for what we want.
	# If src(x,y) is lower than threshold=100, the new pixel value will be set to 0, else it will be left untouched!
	ret, thresh = cv2.threshold(filtered, 100, 255, cv2.THRESH_TOZERO)
	#cv2.imshow('thresh', thresh)

	# add up all the non-zero pixel values in the image and divide by the number of them to find the average pixel value in the whole image
	total_intensity = 0
	pixel_count = 0
	for x in range(h):
		for y in range(w):
			if(thresh[x][y] > 0):
				total_intensity += thresh[x][y]
				pixel_count += 1

	average_intensity = float(total_intensity) / pixel_count
	PEN_PRESSURE = average_intensity
	#print total_intensity
	#print pixel_count
	#print ("Average pen pressure: "+str(average_intensity))

	return

''' main '''
def start(file_name):

	global BASELINE_ANGLE
	global TOP_MARGIN
	global LETTER_SIZE
	global LINE_SPACING
	global WORD_SPACING
	global PEN_PRESSURE
	global SLANT_ANGLE

	# read image from disk
	image = cv2.imread('images/'+file_name)
	#cv2.imshow(file_name,image)

	# Extract pen pressure. It's such a cool function name!
	barometer(image)

	# apply contour operation to straighten the contours which may be a single line or composed of multiple lines
	# the returned image is straightened version of the original image without filtration and binarization
	straightened = straighten(image)
	#cv2.imshow('straightened',straightened)

	# extract lines of handwritten text from the image using the horizontal projection
	# it returns a 2D list of the vertical starting and ending index/pixel row location of each line in the handwriting
	lineIndices = extractLines(straightened)
	#print lineIndices
	#print

	# extract words from each line using vertical projection
	# it returns a 4D list of the vertical starting and ending indices and horizontal starting and ending indices (in that order) of each word in the handwriting
	wordCoordinates = extractWords(straightened, lineIndices)

	#print wordCoordinates
	#print len(wordCoordinates)
	#for i, item in enumerate(wordCoordinates):
	#	cv2.imshow('item '+str(i), straightened[item[0]:item[1], item[2]:item[3]])

	# extract average slant angle of all the words containing a long vertical stroke
	extractSlant(straightened, wordCoordinates)

	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	BASELINE_ANGLE = round(BASELINE_ANGLE, 2)
	TOP_MARGIN = round(TOP_MARGIN, 2)
	LETTER_SIZE = round(LETTER_SIZE, 2)
	LINE_SPACING = round(LINE_SPACING, 2)
	WORD_SPACING = round(WORD_SPACING, 2)
	PEN_PRESSURE = round(PEN_PRESSURE, 2)
	SLANT_ANGLE = round(SLANT_ANGLE, 2)

	return [BASELINE_ANGLE, TOP_MARGIN, LETTER_SIZE, LINE_SPACING, WORD_SPACING, PEN_PRESSURE, SLANT_ANGLE]
