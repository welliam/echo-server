# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import socket
import string
import utils
import io
import os
import cgi
import mimetypes
from gevent.server import StreamServer


ROOT_DIR = '../webroot'


class HTTPException(Exception):
    """Custom exception class"""
    def __init__(self, code, reason):
        self.http_error = code
        self.message = reason


HTTP_BAD_REQUEST = '400 Bad Request'
HTTP_NOT_FOUND = '404 Not Found'
HTTP_UNSUPPORTED_METHOD = '405 Method not allowed'


def format_response(status_line, headers):
    """Building HTTP protocol-compliant response."""
    return '{}\r\n{}\r\n\r\n'.format(
        status_line,
        format_headers(headers)
    )


def format_headers(headers):
    """Builds headers as a string from headers dict."""
    return '\r\n'.join('{}: {}'.format(k, headers[k]) for k in headers)


def response_ok(uri):
    """Returns formatted 200 response."""
    verify_path(uri)
    path = '{}{}'.format(ROOT_DIR, uri)
    status_line = 'HTTP/1.1 200 OK'
    content = path_content(path)
    headers = generate_headers_from_path(path, content)
    return format_response(status_line, headers), content


def response_error(code, reason):
    """Returns formatted error response."""
    status_line = 'HTTP/1.1 {}'.format(code)
    content = '<h1>{}</h1>'.format(reason)
    headers = generate_headers(content, ('text/html', 'charset=UTF-8'))
    return format_response(status_line, headers), content.encode('utf8')


def split_head(request):
    """Split headers line from body."""
    splitted = request.split('\r\n\r\n', 1)
    return splitted[0], '' if len(splitted) == 1 else splitted


def combine_continued_headers(headers):
    """Fix for new lines that start with whitespace."""
    result = []
    for line in headers:
        if line and line[0] in string.whitespace:
            try:
                result[-1] += line.lstrip()
            except IndexError:
                raise HTTPException(
                    HTTP_BAD_REQUEST,
                    'First header line started with whitespace.'
                )
        else:
            result.append(line)
    return result


def parse_headers(header_lines):
    """Parse headers into a dictionary, split at colon."""
    headers = combine_continued_headers(header_lines)
    try:
        return {
            key.lower(): value for key, value in
            map(lambda s: s.split(':', 1), headers)
        }
    except ValueError:
        raise HTTPException(
            HTTP_BAD_REQUEST,
            'Header line has no colon'
        )


def verify_head(method, http_version, headers):
    """Raise exception based on error."""
    if method != 'GET':
        raise HTTPException(HTTP_UNSUPPORTED_METHOD, 'Method is not GET')
    if http_version != 'HTTP/1.1':
        raise HTTPException(HTTP_BAD_REQUEST, 'HTTP version is not 1.1')
    if 'host' not in headers:
        raise HTTPException(HTTP_BAD_REQUEST, 'Host not in header')


def parse_request(request):
    """Parse incoming request, return uri requested."""
    head, body = split_head(request)
    head_lines = list(filter(lambda x: x, head.split('\r\n')))
    try:
        status_line = head_lines[0]
    except IndexError:
        raise HTTPException(HTTP_BAD_REQUEST, 'Request is empty')
    headers = parse_headers(head_lines[1:])
    try:
        method, uri, http_version = status_line.split()
    except ValueError:
        raise HTTPException(HTTP_BAD_REQUEST, 'Invalid status line')
    verify_head(method, http_version, headers)
    return uri


def verify_path(path):
    """Sanitize path"""
    if '~' == path[0] or '//' in path or '..' in path:
        raise HTTPException(HTTP_NOT_FOUND, 'File not found')


def list_dir(path):
    """Get files and dirs in dir"""
    return format_dir(os.listdir(path))


def format_dir(paths):
    """Format to html"""
    html_list = [
        '<li><a href="{link}">{link}</a></li>'
        .format(link=cgi.escape(f)) if '.' in f
        else '<li><a href="{link}/">{link}</a></li>'
        .format(link=cgi.escape(f)) for f in paths
    ]
    return '<ul>{}</ul>'.format(''.join(html_list))


def path_content(path):
    """Check if dir or file"""
    if os.path.isdir(path):
        return list_dir(path).encode('utf8')
    elif os.path.isfile(path):
        return io.open(path, 'rb').read()
    else:
        raise HTTPException(HTTP_NOT_FOUND, 'File not found')


def generate_headers(content, mime_type):
    """Input content length, type, encoding to header"""
    mime, encoding = mime_type
    headers = {
        'Content-Length': len(content)
    }
    if mime:
        headers['Content-Type'] = mime
        if encoding:
            headers['Content-Type'] += '; charset={}'.format(encoding)
    else:
        headers['Content-Type'] = 'text/html'
    return headers


def generate_headers_from_path(path, content):
    """Return proper formatted header from requested path"""
    return generate_headers(content, mimetypes.guess_type(path))


def start_server():
    """Set up server socket."""
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    server_socket.bind(utils.address)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(1)
    return server_socket


def handle_connection(conn, addr):
    """Determines what to send back as response."""
    message = utils.recieve_message(conn)
    try:
        uri = parse_request(message.decode())
        header, content = response_ok(uri)
    except HTTPException as e:
        header, content = response_error(e.http_error, e.message)
    print(header.encode('utf8') + content)
    conn.sendall(header.encode('utf8') + content)
    conn.close()


def server():
    """Set up client socket"""
    StreamServer(utils.address, handle_connection).serve_forever()


if __name__ == '__main__':
    server()
