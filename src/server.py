# -*- coding: utf-8 -*-

import socket
import string
from gevent.server import StreamServer
import utils


class HTTPException(Exception):
    """Custom exception class"""
    def __init__(self, code, reason):
        self.http_error = code
        self.message = reason


HTTP_BAD_REQUEST = '400 Bad Request'
HTTP_UNSUPPORTED_METHOD = '405 Method not allowed'


def format_response(status_line, headers, content):
    """Building HTTP protocol-compliant response."""
    return u'{}\r\n{}\r\n\r\n{}\r\n'.format(
        status_line,
        format_headers(headers),
        content
    )


def format_headers(headers):
    """Builds headers as a string from headers dict."""
    return u'\r\n'.join('{}: {}'.format(k, headers[k]) for k in headers)


def response_ok():
    """Returns formatted 200 response."""
    status_line = u'HTTP/1.1 200 OK'
    headers = {u'Content-Type': 'text/html; charset=UTF-8'}
    content = u'<h1>Hello world!</h1>'
    return format_response(status_line, headers, content)


def response_error(code, reason):
    """Returns formatted error response."""
    status_line = u'HTTP/1.1 {}'.format(code)
    headers = {u'Content-Type': 'text/html; charset=UTF-8'}
    content = u'<h1>{}</h1>'.format(reason)
    return format_response(status_line, headers, content)


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
    message = utils.recieve_message(conn)
    print(message)
    try:
        parse_request(message.decode())
        response = response_ok()
    except HTTPException as e:
        response = response_error(e.http_error, e.message)
    print('responding with', response.encode('utf8'))
    conn.sendall(response.encode('utf8'))
    conn.close()


def server():
    """Set up client socket"""
    StreamServer(utils.address, handle_connection).serve_forever()


if __name__ == '__main__':
    server()
