import psycopg2
from config import config

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
        # connect to the PostgreSQL database
        conn = psycopg2.connect()
        # create a new cursor
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



	




#----------------------------------------------------------------------#	

if __name__ == '__main__':
	main(argv)