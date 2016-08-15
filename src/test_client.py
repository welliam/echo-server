import pytest

CLIENT_MESSAGES = [
    'hello',
    'flajkdsfkladsfjkaslkjfaslkjdfjkasdjkfajskldfjklasdfkjlajskldf',
    'ສະ​ບາຍ​ດີ​ຊາວ​ໂລກ',
    '1234567812345678',
    '12345678',
    ''
]

@pytest.mark.parametrize('message', CLIENT_MESSAGES)
def test_client(message):
    from client import client
    assert client(message) == message
