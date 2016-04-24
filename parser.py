import math
import re
import csv
import itertools as IT
import collections

# import numpy

import AsteroidTypes

DATA_24 = "C:/Users/Developer/Desktop/EAR_A_DBP_3_RDR_24COLOR_V2_1/data/data0/"
DATA_52 = "C:/Users/Developer/Desktop/EAR_A_RDR_3_52COLOR_V2_1/data/data0/"

known_asteroids = {}
asteroid_class_model = {}

#C
test_data = [0.72,0.78,0.8,0.92,0.9,0.96,0.97,1.01,1,0.98,1.03,1.03,1.05,1.02,1.02,1,0.9821,0.9817,0.9814,0.9831,0.9649,0.967,0.9691,0.9663,0.9746,0.9642,0.979,0.9834,0.9611,0.9768,0.9666,0.9659,0.9601,0.9592,0.9679,0.9746,0.9706,0.9812,0.9772,0.9729,0.986,0.9865,0.9915,0.993,1.005,1.0122,1.003,1.0133,1.0051,0.9989,1.0054,1.022,1.0222,1.0216,1.0222,1.0393,1.0408,1.0515,1.0701,1.0844,1.0865,1.0911,1.0708,1.0879,1.099,1.0977,1.1003,1.0575]
#M
#test_data = [.87,.86,.86,.90,.94,.95,.99,.96,1.02,1.01,1.08,1.09,1.12,1.10,1.14,1.13,1.1136,1.1273,1.1516,1.1544,1.1497,1.1748,1.1804,1.2191,1.2437,1.2348,1.2557,1.2585,1.2454,1.2615,1.2792,1.2653,1.2698,1.2637,1.2956,1.2868,1.2743,1.2971,1.3220,1.3304,1.3133,1.3159,1.3113,1.3305,1.3314,1.3363,1.3442,1.3328,1.3359,1.3236,1.3322,1.3396,1.3415,1.3502,1.3548,1.3660,1.3760,1.3778,1.3911,1.3952,1.3953,1.3937,1.4074,1.4188,1.4462,1.4422,1.4569,1.4223]
#A
#test_data = [.40,-9.99,.46,.60,.67,.79,.86,.94,.97,1.08,1.13,1.26,1.28,1.26,1.33,1.23,1.2577,1.2503,1.2761,1.2520,-.9999,1.2284,1.2129,1.1465,1.1310,1.1739,1.1242,1.1420,1.2184,1.2449,1.2459,1.2884,1.3317,1.3243,1.3333,1.4185,1.4443,1.4536,1.5049,1.5981,1.7001,1.6675,1.7188,1.7449,1.7875,1.8136,1.8649,1.8743,1.7614,1.8059,1.8414,1.8356,1.8462,1.8314,1.8588,1.8947,1.8885,1.9076,1.8931,1.8782,1.8973,1.9160,1.9350,1.9792,1.9644,2.0080,2.1363,1.9451]

def generate_csv(path,color):

	output_file = open('spectrum_'+str(color)+'.csv', 'w')

	with open(path+str(color)+"color.tab") as f:
		data_contents = f.readlines()

	with open(path+str(color)+"color.lbl") as f:
		info_contents = f.readlines()

	column_list = []
	num_columns = 0;
	state = "search"

	for line in info_contents:

		if (line.find("INTERCHANGE_FORMAT") > 0):
			state = "column number"

		if (state == "column number"):
			if (line.find("COLUMNS") > 0):
				line = re.sub( '\s+', '', line ).strip()
				num_columns = int(re.sub( 'COLUMNS=', '', line ).strip())

		if (line.find("OBJECT") > 0):
			state = "column found"

		if (state == "column found"):
			if (line.find("NAME") > 0):
				state = "search"
				column_list.append( line.split('= "',1)[1].replace(" ","").replace("\"","").replace("\n",""))

	for column_index in range(len(column_list)):
		output_file.write(column_list[column_index])
		if (column_index < len(column_list)-1):
			output_file.write(',')

	output_file.write("\n")

	for line in data_contents:
		line = re.sub( '\s+', ' ', line ).strip()
		asteroid_data = line.split(" ")

		index = 0
		for data in asteroid_data:
			if (len(asteroid_data) > num_columns):
				if (index == 1):
					output_file.write(data+" "+asteroid_data[index + 1])
				elif (index == 2):
					output_file.write(',')
				else:
					output_file.write(data)
					if (index < len(asteroid_data)-1):
						output_file.write(',')
			else:
				output_file.write(data)
				if (index < len(asteroid_data)-1):
					output_file.write(',')
			index = index + 1

		output_file.write("\n")

	output_file.close();

def query(file,asteroid):
	with open(file, 'r') as f:
		reader = csv.DictReader(f)
		rows = [row for row in reader if row['AST_NUMBER'] == asteroid]

	return rows

def combine():

	columns_written = False

	output_file = open('combined.csv', 'w')

	for asteroid_class in AsteroidTypes.AsteroidsOfType:
		asteroid_numbers = AsteroidTypes.AsteroidsOfType[asteroid_class]
		for asteroid in asteroid_numbers:

			s24 = query('spectrum_24.csv',str(asteroid))
			s52 = query('spectrum_52.csv',str(asteroid))

			if (len(s24) > 0 and len(s52) > 0):

				row = []
				
				combined_columns = [];

				with open('spectrum_24.csv') as f:
					contents = f.readlines()
					combined_columns = contents[0].split(',')[:34]
				
				for line_index in range(len(contents)):
					values = contents[line_index].split(',')
					if (values[0] == str(asteroid)):
						row = values[:34]
						break

				f.close()

				with open('spectrum_52.csv') as f:
					contents = f.readlines()
					combined_columns = combined_columns + contents[0].split(',')[3:]
				
				for line_index in range(len(contents)):
					values = contents[line_index].split(',')
					if (values[0] == str(asteroid)):
						row = row + values[3:]
						break

				f.close()
				
				if (columns_written == False):
					columns_written = True
					output_file.write('AST_CLASS,')
					for index in range(len(combined_columns)):
						output_file.write(combined_columns[index])
						if (index < len(combined_columns)-1):
							output_file.write(",")

				output_file.write(asteroid_class+",")
				for index in range(len(row)):
					output_file.write(row[index])
					if (index < len(row)-1):
						output_file.write(",")

	output_file.close()

	with open("combined.csv","r") as f:
		contents = f.readlines()
		for i in range(1,len(contents)):
			r = contents[i].split(",")
			data = [r[0], r[1], r[3], r[5], r[7], r[9], r[11], r[13], r[15], r[17], r[19], r[21], r[23], r[25], r[27], r[29], r[31], r[33], r[35]]
			
			for i in range(36,87):
				data.append(r[i].replace("\n",""))
			
			known_asteroids[data[1]] = [data[0]]+data[2:len(data)]

def compare_diff(input_data):

	input_diff = []
	confidence = {}

	for i in range(len(input_data)-1):
		input_diff.append(input_data[i+1]-input_data[i])

	scores = {}
	for asteroid_class in asteroid_class_model:
		score = 0
		for i in range(len(input_diff)):
			score = score + (input_diff[i] - asteroid_class_model[asteroid_class][i])**2
		scores[asteroid_class] = score

	min_score = ''
	
	for c in scores:
		min_score = c
		break

	for c in scores:
		confidence[c] = round(1000*math.exp(-scores[c]),3)
		if (scores[c] < scores[min_score]):
			min_score = c

	print("ASTEROID CLASS: "+min_score)
	print("CONFIDENCE:")
	for c in confidence:
		print(c+" --- "+str(confidence[c]))

# def compare_corrcoeff(input_data):
# 	scores = {}
# 	for asteroid_class in asteroid_class_model:
# 		score = numpy.corrcoef(input_data,asteroid_class_model[asteroid_class])
# 		scores[asteroid_class] = score[0][1]

# 	max_score = ''
	
# 	for c in scores:
# 		max_score = c
# 		break

# 	for c in scores:
# 		if (scores[c] > scores[max_score]):
# 			max_score = c

# 	print(max_score)


# def build_asteroid_class_model():

# 	classes = []
# 	for asteroid_id in known_asteroids:
# 		if (not(known_asteroids[asteroid_id][0] in classes)):
# 			classes.append(known_asteroids[asteroid_id][0])

# 	for c in classes:
# 		data = [0] * (len(known_asteroids[asteroid_id])-1)
# 		num_to_average = 0;
# 		for asteroid_id in known_asteroids:
# 			if (known_asteroids[asteroid_id][0] == c):
# 				num_to_average = num_to_average + 1
# 				for i in range(1,len(known_asteroids[asteroid_id])):
# 					data[i-1] = data[i-1] + (float(known_asteroids[asteroid_id][i]))

# 		if (num_to_average > 0):
# 			for i in range(len(known_asteroids[asteroid_id])-1): 
# 				data[i] = data[i]/num_to_average

# 		asteroid_class_model[c] = data

def build_asteroid_class_model_diff():

	classes = []
	for asteroid_id in known_asteroids:
		num_diff = len(known_asteroids[asteroid_id])-2
		if (not(known_asteroids[asteroid_id][0] in classes)):
			classes.append(known_asteroids[asteroid_id][0])

	i = 0
	for c in classes:
		diff = [0] * num_diff
		num_to_average = 0;
		for asteroid_id in known_asteroids:
			i = i + 1
			if (known_asteroids[asteroid_id][0] == c):
				num_to_average = num_to_average + 1
				for i in range(1,num_diff+1):
					diff[i-1] = diff[i-1] + (float(known_asteroids[asteroid_id][i+1])-float(known_asteroids[asteroid_id][i]))

		if (num_to_average > 0):
			for i in range(len(diff)): 
				diff[i] = diff[i]/num_to_average

		asteroid_class_model[c] = diff

def main():
	
	generate_csv(DATA_24,24)
	generate_csv(DATA_52,52)
	combine()
	build_asteroid_class_model_diff()
	compare_diff(test_data)
	
main()