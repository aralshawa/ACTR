import re
import csv
import itertools as IT

import AsteroidTypes

DATA_24 = "C:/Users/Developer/Desktop/EAR_A_DBP_3_RDR_24COLOR_V2_1/data/data0/"
DATA_52 = "C:/Users/Developer/Desktop/EAR_A_RDR_3_52COLOR_V2_1/data/data0/"

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

def differentiate(data):
	
	differentiated = []
	for i in range(len(data)-1):
		differentiated.append(data[i+1] - data[i])

	return data

def main():
	
	generate_csv(DATA_24,24)
	generate_csv(DATA_52,52)
	
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
					output_file.write('ASTER_CLASS,')
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

main()