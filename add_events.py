from calendarapp.models import *
import csv
from sys import *

def add_event(name, org_name, categories, 
	start, end, location, website, description, free):

	orgs = Organization.objects.filter(name__exact=org_name)
	org = orgs[0] # Should only be one organization with that name

	# Parse category string into an array, then get the relevant category
	# objects
	cats = Category.objects.filter(name__in=categories)

	# Parse start and end date/times to the right format
	start_datetime = parse(start)
	end_datetime = parse(end)

	# Convert string to boolean
	if free == 'No': is_free = False
	else: is_free = True

	e = Event(org=org, name=name, start_datetime=start_datetime, \
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

	try:
		conn = psycopg2.connect()
		cur = conn.cursor()


		# execute the UPDATE  statement
		cur.execute(sql, (vendor_name, vendor_id))
		# Commit the changes to the database
		conn.commit()
		# Close communication with the PostgreSQL database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
 
	return

def main(argv):

	fname = "63ff5e9642709baf8e9c18047dbb2a8b.csv"

	with open(fname, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				line_count += 1

				name = {row["Title"]}
				if name == '': continue

				start = {row["Start"]}
				end = {row["End"]}
				location = {row["Where"]}

				print name, ' ', start, ' ', end, ' ', location, ' '
				

#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)