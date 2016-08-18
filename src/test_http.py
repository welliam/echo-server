# -*- coding: utf-8 -*-

"""Test HTTP functions."""


def test_format_response():
    from server import format_response
    response = format_response('stats', {'header': 'etc', 'h': 'hi'}, 'content')
    assert 'stats\r\n' in response
    assert 'header: etc\r\n' in response
    assert 'content' in response
    assert '\r\n\r\n' in response


def test_format_headers():
    from server import format_headers
    headers = format_headers({'header': 'etc', 'h': 'hi'})
    assert 'header: etc' in headers
    assert 'h: hi' in headers


def test_response_ok_status():
    from server import response_ok
    lines = response_ok().split('\r\n')
    assert '200 OK' in lines[0]


def test_response_ok_header():
    from server import response_ok
    lines = response_ok().split('\r\n')
    assert any('content-type:' in line.lower() for line in lines)


def test_response_error_status():
    from server import response_error
    lines = response_error().split('\r\n')
    assert '500 Internal Server Error' in lines[0]


def test_response_error_header():
    from server import response_error
    lines = response_error().split('\r\n')
    assert any('content-type:' in line.lower() for line in lines)
