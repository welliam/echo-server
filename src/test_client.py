# -*- coding: utf-8 -*-

import pytest


CLIENT_MESSAGES = [
    u'GET / HTTP/1.1\r\nHost: foo.bar',
    u'GET / HTTP/1.1\r\nHost:\r\n   foo.bar',
    u'GET / HTTP/1.1\r\nHost: foo.bar\r\n\r\nhello world!\r\n\r\nhi!',
]


CLIENT_ERROR_MESSAGES = [
    u'hello',
    u'GET / HTTP/1.1\r\n',
    u'GET / HTTP/1.1\r\nHost foo.bar\r\n\r\n',
    u'GET / HTTP/1.1\r\nHost: foo.bar\r\nhello hello hello',
]


SERVER_ERROR_MESSAGES = [
    u'GET / HTTP/1.0\r\nHost: foo.bar',
    u'HEAD / HTTP/1.1\r\nHost:\r\n   foo.bar',
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
