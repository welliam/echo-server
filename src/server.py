# -*- coding: utf-8 -*-

import socket
import utils


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
    """Returns formatted 200 response"""
    status_line = "HTTP/1.1 200 OK"
    headers = {u'Content-Type': 'text/html; charset=UTF-8'}
    content = u'<h1>Hello world!</h1>'
    return format_response(status_line, headers, content)


def response_error():
    """Returns formatted 500 response"""
    status_line = u'HTTP/1.1 500 Internal Server Error'
    headers = {u'Content-Type': 'text/html; charset=UTF-8'}
    content = u'Internal server error.'
    return format_response(status_line, headers, content)


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


def server(server_socket):
    """Set up client socket"""
    while True:
        conn, addr = server_socket.accept()
        message = utils.recieve_message(conn)
        print(message)
        conn.sendall(response_ok().encode('utf8'))
        conn.close()


if __name__ == '__main__':
    server_socket = start_server()
    try:
        server(server_socket)
    except KeyboardInterrupt:
        server_socket.close()
