def recieve_message(conn):
    buffer_length = 8
    message_complete = False
    message = b''
    while not message_complete:
        part = conn.recv(buffer_length)
        message += part

        print('part', part)
        print('message', message)
        message_complete = len(part) < buffer_length
    return message


address = ('127.0.0.1', 5002)
