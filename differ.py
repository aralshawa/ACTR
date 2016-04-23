import re

DATA_FILE = "C:/Users/ryanm/Desktop/spaceapps2016/spaceapps2016/parsed_file.csv"

NEW_FILE = "delta_file.csv"

def main():

	output_file = open(NEW_FILE, 'w')
	#tab file
	with open(DATA_FILE) as f:
		data_contents = f.readlines()
	delta_array = []

	#Forloop through each row
	for line in data_contents:
		#line = re.sub( '\s+', ' ', line ).strip()
		asteroid_data = line.split(",")

		index = 0
		#Forloop through each column
		#asteroid_data is column
		for data in asteroid_data:
			if(index < len(asteroid_data) - 1):
				if (len(asteroid_data) < 55):
					if (index == 1):
						output_file.write(data+" "+asteroid_data[index + 1])
					elif (index == 2):
						output_file.write(',')
					else:
						output_file.write(data+',')
				else:
					try:
						delta = float(asteroid_data[index + 1]) - float(data)
						delta_array.append(delta)
						output_file.write(str(delta) +',')
					except ValueError:
						output_file.write(data+',')
				index = index + 1
		output_file.write("\n")
	output_file.close();
	#print("length = ", len(asteroid_data))
	#print("index = ", index)
	#print("delta_array = ", delta_array)
	return delta_array
main()
