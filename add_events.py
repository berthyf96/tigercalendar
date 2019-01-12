from calendarapp.models import *
import csv
from sys import *
import xlrd 


def add_event(name, categories, 
	start_datetime, end_datetime, location, website, description, free):

	# Parse category string into an array, then get the relevant category
	# objects
	cats = Category.objects.filter(name__in=categories)

	# Convert string to boolean
	if free == 'No': is_free = False
	else: is_free = True

	e = Event(org=None, name=name, start_datetime=start_datetime, \
		end_datetime=end_datetime, is_free=is_free)
	e.save()

	e.category.set(cats) # Must set many-to-many field after the fact

	# Set non-required categories if they exist
	if location != '':
		e.location = location
	if description != '':
		e.description = description
	if website != '':
		e.website = website
	e.save()

	return

def main(argv):

	# loc = ("jan22tofeb20.xlsx") 

	# wb = xlrd.open_workbook(loc) 
	# sheet = wb.sheet_by_index(0) 

	# NUM_LINES = 85
	# # NUM_LINES = 24

	# NAME_COL = 0
	# START_COL = 1
	# END_COL = 2
	# DESC_COL = 4
	# LOC_COL = 5
	# CATS_COL = 6

	# for row in range(1, NUM_LINES):

	# 	name = str(sheet.cell_value(row, NAME_COL))
	# 	if name is None: continue
	# 	if name == '': continue

	# 	start = str(sheet.cell_value(row, START_COL))
	# 	end = str(sheet.cell_value(row, END_COL))
	# 	location = str(sheet.cell_value(row, LOC_COL))
	# 	description = str(sheet.cell_value(row, DESC_COL))
	# 	cats = str(sheet.cell_value(row, CATS_COL))

	# 	print(name, ' ', start, ' ', end, ' ', location)

	# 	add_event(name, cats, start, end, location, '', description, True)

	NUM_EVENTS = 1000
	for i in range(1, NUM_EVENTS):
		name = 'test' + str(i)
		start = '2019-02-21 10:00'
		end =  '2019-02-21 12:00'
		print(i)

		add_event(name, [], start, end, '', '', '', True)

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)