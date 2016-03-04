# Terrible, terrible code for extracting data from an en expanded
# fiddler saz and rewriting it to html content.
import re
import os
import gzip
from httplib import HTTPResponse
from StringIO import StringIO
import json
import cgi

BODY_SEP = '\r\n\r\n'

BINARY_TYPES = {
    "Content-Type: image/png": 'png',
    "Content-Type: image/jpeg": 'jpg',
    "Content-Type: image/gif": 'gif',
    "Content-Type: image/x-icon": 'xicon'
}

# http://stackoverflow.com/a/24729316/306149
class FakeSocket():
    def __init__(self, response_str):
        self._file = StringIO(response_str)
        
    def makefile(self, *args, **kwargs):
        return self._file

def process_http(raw):
    headers, body = raw.split(BODY_SEP, 1)
    if headers.startswith('CONNECT'):
        return None
    
    if not len(body):
         return {
            'headers': headers,
            'body':  None
        }
    
    source = FakeSocket(raw)
    response = HTTPResponse(source)
    response.begin()
    body = None
    if response.getheader('Content-Encoding') == 'gzip':
        buf = StringIO(response.read(len(raw)))
        f = gzip.GzipFile(fileobj=buf)
        body = f.read()
    else:
        body = response.read(len(raw))
    
    return {
        'headers': headers,
        'body': body if len(body) else None
    }

def process_body(name, pair, out_dir = 'out'):
    if pair is None:
        return None
    headers = pair['headers']
    body = pair['body']
    if body is not None:
        binary_type = None
        for k, v in BINARY_TYPES.iteritems():
            if k in headers:
                binary_type = v
                break
        if binary_type is not None:
            file = os.path.join(out_dir, name + '.' + binary_type)
            with open(file, 'wb') as f:
                f.write(body)
            body = { 'file': file }
        else:
            body = { 'content': body }
    return {
        'headers': headers,
        'body': body
    }

def process_file(name, request_file, response_file):
    with open(request_file, 'rb') as req:
        req_body = process_body(name, process_http(req.read()))
    
    if req_body is None:
        return None
    
    with open(response_file, 'rb') as res:
        res_body = process_body(name, process_http(res.read()))
    
    return {
        'request': req_body,
        'response': res_body
    }

def process_files(saz_dir):
    i = 1
    root = os.path.join(saz_dir, 'raw')
    results = []
    while True:
        print i
        name = "{0:03d}".format(i)
        request = name + '_c.txt'
        resp = name + '_s.txt'
        request_file = os.path.join(root, request)
        resp_file = os.path.join(root, resp)
        if not os.path.isfile(request_file) or not os.path.isfile(resp_file):
            return results
        result = process_file(str(i), request_file, resp_file)
        if result is not None:
            results.append(result)
        i = i + 1


def format_subsection(title, content):
    headers = content['headers']
    headers = '<pre><code class="http">' + headers + '</code></pre>'
    
    body = content['body']
    if body is None:
        body = ''
    elif 'file' in body:
        body = '<figure><img src="{0}" /></figure>'.format(body['file'])
    else:
        body = body['content']
        type = ''
        if '/css' in headers:
            type = 'css'
        elif '/javascript' in headers or '/x-javascript' in headers:
            type = 'javascript'
        
        body = '<pre><code class="' + type + ' body-code">' + cgi.escape(body) + '</code></pre>'

    return """<section><h2 class="subsection-title">{title}</h2>\n\n{headers}\n\n{body}</section>""".format(
        title=title, headers=headers, body=body)

def format_section(results):
    for r in results:
        req = r['request']
        res = r['response']
        section_title = req['headers'].splitlines()[0]
        section_title = "<br>".join(section_title.split(' ')[:2])
        
        req_section = format_subsection('Request', req)
        res_section = format_subsection('Response', res)
        yield """<section class="page"><h1 class="section-title">{section_title}</h1>\n{req}\n\n{res}</section>""".format(section_title = section_title, req = req_section, res = res_section)



results = process_files(os.path.join(os.getcwd(), 'sample-saz'))

with open('index.html', 'wb') as f:
    content = '\n\n'.join(format_section(results))
    content = content.replace('\r\n', '\n')
    content = """---
layout: default
---\n""" + content
    f.write(content)
