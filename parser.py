import re

DATA_FILE = "C:/Users/Developer/Desktop/EAR_A_DBP_3_RDR_24COLOR_V2_1/data/data0/24color.tab"
INFO_FILE = "C:/Users/Developer/Desktop/EAR_A_DBP_3_RDR_24COLOR_V2_1/data/data0/24color.lbl"

NEW_FILE = "parsed_file.csv"

def main():

	output_file = open(NEW_FILE, 'w')

	with open(DATA_FILE) as f:
		data_contents = f.readlines()

	with open(INFO_FILE) as f:
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

	for column in column_list:
		output_file.write(column+',')

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
					output_file.write(data+',')
			else:
				output_file.write(data+',')
			index = index + 1

		output_file.write("\n")

	output_file.close();


main()