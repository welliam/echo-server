# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest


CLIENT_MESSAGES = [
    'GET / HTTP/1.1\r\nHost: foo.bar',
    'GET / HTTP/1.1\r\nHost:\r\n   foo.bar',
    'GET / HTTP/1.1\r\nHost: foo.bar\r\n\r\nhello world!\r\n\r\nhi!',
]


CLIENT_ERROR_MESSAGES = [
    'hello',
    'GET / HTTP/1.1\r\n',
    'GET / HTTP/1.1\r\nHost foo.bar\r\n\r\n',
    'GET / HTTP/1.1\r\nHost: foo.bar\r\nhello hello hello',
]


SERVER_ERROR_MESSAGES = [
    'GET / HTTP/1.0\r\nHost: foo.bar',
    'HEAD / HTTP/1.1\r\nHost:\r\n   foo.bar',
]


@pytest.mark.parametrize('message', CLIENT_MESSAGES)
def test_client(message):
    from client import client
    lines = client(message).split('\r\n')
    assert '200 OK' in lines[0]
    assert any('content-type' in line.lower() for line in lines)


@pytest.mark.parametrize('message', CLIENT_ERROR_MESSAGES)
def test_client_error(message):
    from client import client
    lines = client(message).split('\r\n')
    assert '400' in lines[0]
    assert any('content-type' in line.lower() for line in lines)


@pytest.mark.parametrize('message', SERVER_ERROR_MESSAGES)
def test_server_error(message):
    from client import client
    lines = client(message).split('\r\n')
    assert '400' in lines[0] or '405' in lines[0]
    assert any('content-type' in line.lower() for line in lines)
