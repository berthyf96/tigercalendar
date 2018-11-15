import sys, os, cgi, urllib.parse, re
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

form = cgi.FieldStorage()

CAS_URL = 'https://fed.princeton.edu/cas/'
class CASClient:
    def __init__(self, request):
        self.request = request
        self.uri = request.build_absolute_uri()

    def Authenticate(self):
        if 'ticket' in form:
            netid = self.Validate(form['ticket'].value)
            if netid != None:
                return redirect('/cal')
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
            '?service=' + urllib.quote(self.ServiceURL()) + \
            '&ticket=' + urllib.quote(ticket))
        r = urllib.urlopen(val_url).readlines()   # returns 2 lines
        if len(r) == 2 and re.match("yes", r[0]) != None:
            return r[1].strip()
        return None

    def ServiceURL(self):
        if self.request:
            ret = "http://whatsroaring.herokuapp.com/cal"#self.uri
            ret = re.sub(r'ticket=[^&]*&?', '', ret)
            ret = re.sub(r'\?&?$|&$', '', ret)
            return ret
            #$url = preg_replace('/ticket=[^&]*&?/', '', $url);
            #return preg_replace('/?&?$|&$/', '', $url);
        print("no request URI")
        return "something is badly wrong"

def main():
    print("CASClient does not run standalone")
if __name__ == '__main__':
    main()
