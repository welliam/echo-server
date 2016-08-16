# -*- coding: utf-8 -*-

import socket
import utils


def start_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    )
    server_socket.bind(utils.address)
    server_socket.listen(1)
    return server_socket


def server(socket):
    while True:
        conn, addr = server_socket.accept()
        message = utils.recieve_message(conn)
        print(message)
        conn.sendall(message + utils.END)
        conn.close()


if __name__ == '__main__':
    server_socket = start_server()
    try:
        server(server_socket)
    except KeyboardInterrupt:
        server_socket.close()
