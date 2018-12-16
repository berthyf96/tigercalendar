import sys, os, cgi, urllib.parse, re, urllib.request
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
import xml.etree.ElementTree as ET
from django.contrib.sessions.backends.db import SessionStore

form = cgi.FieldStorage()

CAS_URL = 'https://fed.princeton.edu/cas/'
class CASClient:
    def __init__(self, request):
        self.request = request
        self.uri = request.build_absolute_uri()

    def Authenticate(self):
        
        # return_url = 'http://localhost:3000/calendar'
        return_url = 'http://whatsroaring.herokuapp.com/calendar'
        # if self.request.session.get('netid'):
        #     print("got here")
        #     return redirect(return_url)
        ticket = self.request.GET.get('ticket')
        if ticket != None:
            netid = self.Validate(ticket)
        # if 'ticket' in form:
        #     netid = self.Validate(form['ticket'].value)
            if netid != None:
                print("netid in /login: " + netid)
                # self.response.set_cookie('netid', netid)
                # return self.response
                self.request.session['netid'] = netid
                self.request.session.modified = True
                self.request.session.save()
                return redirect(return_url)
                # return HttpResponse(netid)#redirect('/netid?netid=' + netid)
                # return redirect('/?ticket=' 
                #                 + urllib.parse.quote(form['ticket'].value))
        # No valid ticket; redirect the browser to the login page to get one
        login_url = (CAS_URL + 'login' \
            + '?service=' + urllib.parse.quote(self.ServiceURL()))
        print('Location: ' + login_url)
        print('Status-line: HTTP/1.1 307 Temporary Redirect')
        print("")
        print(login_url)
        return redirect(login_url)

    def Validate(self, ticket):
        val_url = (CAS_URL + "validate" + \
            '?service=' + urllib.parse.quote(self.ServiceURL()) + \
            '&ticket=' + urllib.parse.quote(ticket))
        print("validate url = " + val_url)
        r = urllib.request.urlopen(val_url).readlines()   # returns 2 lines
        top = str(r[0].strip()).split("'")
        bottom = str(r[1].strip()).split("'")
        print(top[1])
        print(bottom[1])
        if len(r) == 2 and top[1].strip() == "yes":
            print("successful validation")
            return bottom[1]
        # lines = urllib.request.urlopen(val_url).readlines()
        # for line in lines:
        #     print(str(line))
        #     m = re.match(r'<cas:user>(?P<name>)</cas:user>', str(line))
        #     if m != None:
        #         return m.group('name')
        return None

    def ServiceURL(self):
        if self.request:
            # ret = "http://localhost:8000/login"
            ret = "http://whatsroaring-api.herokuapp.com/login"
            # ret = "http://localhost:3000/" #"http://whatsroaring.herokuapp.com/"#self.uri
            ret = re.sub(r'ticket=[^&]*&?', '', ret)
            ret = re.sub(r'\?&?$|&$', '', ret)
            print("value of ret is " + ret)
            return ret
            #$url = preg_replace('/ticket=[^&]*&?/', '', $url);
            #return preg_replace('/?&?$|&$/', '', $url);
        print("no request URI")
        return "something is badly wrong"

def main():
    print("CASClient does not run standalone")
if __name__ == '__main__':
    main()
