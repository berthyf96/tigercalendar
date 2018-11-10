#!/usr/bin/python

import CASClient

C = CASClient.CASClient()
netid = C.Authenticate()
print "Content-Type: text/html"
print ""
#import os
#print "hello from the other side, " 
#print netid

print "Hello from the other side, %s\n" % netid

print "<p>Think of this as the main page of your application after %s has been authenticated." % netid