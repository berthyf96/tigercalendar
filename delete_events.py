from calendarapp.models import *
import csv
from sys import *
import xlrd 


def delete_event(name):

	e = Event.objects.filter(name__iexact = name)
	e.delete()

	return

def main(argv):

	# fname = "jan7to21v3.xslx"

	# with open(fname, mode='r') as csv_file:

	# 	csv_reader = csv.DictReader(csv_file)
	# 	line_count = 0
	# 	MAX = 10
	# 	for row in csv_reader:
	# 		if line_count > MAX: break
	# 		if line_count == 0:
	# 			line_count += 1
	# 		else:
	# 			line_count += 1

	# 			name = str(row["Title"])
	# 			if name is None: continue
	# 			if name == '': continue

	# 			start = str(row["Start"])
	# 			end = str(row["End"])
	# 			location = str(row["Where"])
	# 			cats = str(row["Categories"])
	# 			description = str(row["Description"])

	# 			print(name, ' ', start, ' ', end, ' ', location, ' ', description)

	# 			add_event(name, cats, start, end, '', '', '', True)

	# loc = ("jan22tofeb20.xlsx") 

	# wb = xlrd.open_workbook(loc) 
	# sheet = wb.sheet_by_index(0) 

	# NUM_LINES = 24

	# NAME_COL = 0

	# for row in range(1, NUM_LINES):

	# 	name = str(sheet.cell_value(row, NAME_COL))
	# 	if name is None: continue
	# 	if name == '': continue

	# 	delete_event(name)

	NUM_EVENTS = 1000
	for i in range(1, NUM_EVENTS):
		name = 'test' + str(i)
		delete_event(name)
		print(i)

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)