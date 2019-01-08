from calendarapp.models import *
import csv
from sys import *

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

	fname = "jan7to21v3.csv"

	with open(fname, mode='r') as csv_file:

		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				line_count += 1

				name = str(row["Title"])
				if name is None: continue
				if name == '': continue

				start = str(row["Start"])
				end = str(row["End"])
				location = str(row["Where"])
				cats = str(row["Categories"])
				description = str(row["Description"])

				print(name, ' ', start, ' ', end, ' ', location, ' ', description)

				add_event(name, cats, start, end, '', '', '', True)
				

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)