def recieve_message(conn):
    buffer_length = 8
    message_complete = False
    message = b''
    while not message_complete:
        part = conn.recv(buffer_length)
        message += part
        message_complete = len(part) < buffer_length or part[-1] == END
    return message[:-1]


END = chr(0).encode('utf8')


address = ('127.0.0.1', 5000)
