# -*- coding: utf-8 -*-

import pytest

CLIENT_MESSAGES = [
    u'hello',
    u'flajkdsfkladsfjkaslkjfaslkjdfjkasdjkfajskldfjklasdfkjlajskldf',
    u'ສະ​ບາຍ​ດີ​ຊາວ​ໂລກ',
    u'1234567812345678',
    u'12345678',
    u'GET / HTTP/1.1\r\n\r\n',
]


@pytest.mark.parametrize('message', CLIENT_MESSAGES)
def test_client(message):
    from client import client
    lines = client(message).split('\r\n')
    assert '200 OK' in lines[0]
    assert any('content-type' in line.lower() for line in lines)
