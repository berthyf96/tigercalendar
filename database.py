from psycopg2 import connect
from sys import stderr

class Database:

 	def __init__(self):
 		self._connection = None

	def connect(self):  

		connect_string =  "host='localhost' dbname='events' user='bestteam' password='princeton'"

		try:
			self._connection = connect(connect_string)

		except Exception, e:
			print >>stderr, 'database not found'
			exit(1)
	         
	def disconnect(self):
	    self._connection.close()

	def getEvents(self):

	    cursor = self._connection.cursor()

	    stmtStr = 'SELECT * FROM events '
	    cursor.execute(stmtStr)

	    row = cursor.fetchone()
	    while row is not None: 
	    	print row
	    	row = cursor.fetchone() 

	    cursor.close()

	def getEventInstances(self):

	    cursor = self._connection.cursor()

	    stmtStr = 'SELECT * FROM event_instances '
	    cursor.execute(stmtStr)

	    row = cursor.fetchone()
	    while row is not None: 
	    	print row
	    	row = cursor.fetchone() 

	    cursor.close()

	def getEventOrgs(self):

	    cursor = self._connection.cursor()

	    stmtStr = 'SELECT * FROM event_orgs '
	    cursor.execute(stmtStr)

	    row = cursor.fetchone()
	    while row is not None: 
	    	print row
	    	row = cursor.fetchone() 

	    cursor.close()

	def getEventCategories(self):

	    cursor = self._connection.cursor()

	    stmtStr = 'SELECT * FROM event_categories '
	    cursor.execute(stmtStr)

	    row = cursor.fetchone()
	    while row is not None: 
	    	print row
	    	row = cursor.fetchone() 

	    cursor.close()

	def getOrgs(self):

	    cursor = self._connection.cursor()

	    stmtStr = 'SELECT * FROM orgs '
	    cursor.execute(stmtStr)

	    row = cursor.fetchone()
	    while row is not None: 
	    	print row
	    	row = cursor.fetchone() 

	    cursor.close()

	def getCategories(self):

	    cursor = self._connection.cursor()

	    stmtStr = 'SELECT * FROM categories '
	    cursor.execute(stmtStr)

	    row = cursor.fetchone()
	    while row is not None: 
	    	print row
	    	row = cursor.fetchone() 

	    cursor.close()

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    print 'EVENTS'
    database.getEvents()
    print
    print
    print 'EVENT INSTANCES'
    database.getEventInstances()
    print
    print
    print 'EVENT ORGS'
    database.getEventOrgs()
    print
    print
    print 'EVENT CATEGORIES'
    database.getEventCategories()
    print
    print
    print 'ORGS'
    database.getOrgs()
    print
    print
    print 'CATEGORIES'
    database.getCategories()
    database.disconnect()