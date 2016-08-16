# -*- coding: utf-8 -*-

"""Test server.py and client.py."""

import pytest

CLIENT_MESSAGES = [
    u'hello',
    u'flajkdsfkladsfjkaslkjfaslkjdfjkasdjkfajskldfjklasdfkjlajskldf',
    u'ສະ​ບາຍ​ດີ​ຊາວ​ໂລກ',
    u'1234567812345678',
    u'12345678',
    u''
]


@pytest.mark.parametrize('message', CLIENT_MESSAGES)
def test_client(message):
    """Test that the echo server is working correctly."""
    from client import client
    assert client(message) == message
