def recieve_message(conn):
    """Retuns message received."""
    buffer_length = 8
    message_complete = False
    message = b''
    while not message_complete:
        part = conn.recv(buffer_length)
        message += part
        message_complete = len(part) < buffer_length
    return message


address = ('127.0.0.1', 5000)
