import re
import sys
from httplib import HTTPSConnection, HTTPConnection
import urllib

URL_RE = re.compile(r"(https?)://([^/]*)(/.*)")

def iter_parameters():
    data = raw_input('... ')
    while data.strip():
        bits = data.strip().split(None, 1)
        if len(bits) == 2: 
            yield tuple(bits)
        data = raw_input('... ')

def loop(connection, base):

    while True:
        command = raw_input('>>> ')
        bits = command.split(None, 1)
        if len(bits) == 0:
            break
        if len(bits) == 1:
            bits.append("")
        method, path = bits
        
        params = urllib.urlencode(list(iter_parameters()))
        print method, base+path, params
        connection.request(method, base + path, params)
        
        resp = connection.getresponse()
        print resp.status, resp.reason
        print resp.read()
    
    connection.close()

def main():
    url = URL_RE.match(sys.argv[1])
    # httplib parses 'foo:443' port specs

    Proto = HTTPSConnection if url.group(1) == "https" else HTTPConnection
    connection = Proto(url.group(2))
        
    loop(connection, url.group(3))

if __name__ == '__main__':
    main()