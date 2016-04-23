import re
import csv
import itertools as IT

import AsteroidTypes

DATA_24 = "C:/Users/Developer/Desktop/EAR_A_DBP_3_RDR_24COLOR_V2_1/data/data0/"
DATA_52 = "C:/Users/Developer/Desktop/EAR_A_RDR_3_52COLOR_V2_1/data/data0/"

known_asteroids = {}
asteroid_class_model = {}

test_data = [0.72,0.78,0.8,0.92,0.9,0.96,0.97,1.01,1,0.98,1.03,1.03,1.05,1.02,1.02,1,0.9821,0.9817,0.9814,0.9831,0.9649,0.967,0.9691,0.9663,0.9746,0.9642,0.979,0.9834,0.9611,0.9768,0.9666,0.9659,0.9601,0.9592,0.9679,0.9746,0.9706,0.9812,0.9772,0.9729,0.986,0.9865,0.9915,0.993,1.005,1.0122,1.003,1.0133,1.0051,0.9989,1.0054,1.022,1.0222,1.0216,1.0222,1.0393,1.0408,1.0515,1.0701,1.0844,1.0865,1.0911,1.0708,1.0879,1.099,1.0977,1.1003,1.0575]

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

def compare(input_data):

	len(test_data)

	input_diff = []

	for i in range(len(input_data)-1):
		input_diff.append(input_data[i+1]-input_data[i])

	scores = {}
	for asteroid_class in asteroid_class_model:
		score = 0
		print(len(input_diff))
		print(len(asteroid_class_model[asteroid_class]))
		print("\n")
		for i in range(len(input_diff)):
			score = score + (input_diff[i] - asteroid_class_model[asteroid_class][i])**2
		scores[asteroid_class] = score

	min_score = ''
	
	for c in scores:
		min_score = c
		break

	for c in scores:
		if (scores[c] < scores[min_score]):
			min_score = c

	print(c)


def build_asteroid_class_model():

	classes = []
	temp=""
	for asteroid_id in known_asteroids:
		temp = asteroid_id
		num_diff = len(known_asteroids[asteroid_id])-2
		if (not(known_asteroids[asteroid_id][0] in classes)):
			classes.append(known_asteroids[asteroid_id][0])

	print(known_asteroids[temp])

	i = 0
	for c in classes:
		diff = [0] * num_diff
		num_to_average = 0;
		for asteroid_id in known_asteroids:
			i = i + 1
			if (known_asteroids[asteroid_id][0] == c):
				num_to_average = num_to_average + 1
				print(len(known_asteroids[asteroid_id]))
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
	build_asteroid_class_model()
	compare(test_data)

main()