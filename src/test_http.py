# -*- coding: utf-8 -*-

"""Test HTTP functions."""
from __future__ import unicode_literals
import pytest


URIS = ['index', '/', '/foo/bar.php', '/test/test']


PATH_TABLE = [
    ('..', False),
    ('//', False),
    ('~', False),
    ('~/Desktop/file.txt', False),
    ('~//..file.txt', False),
    ('../../test.txt', False),
    ('file.txt', True),
    ('/about', True)
]


def test_format_response():
    from server import format_response
    response = format_response(
        'stats', {'header': 'etc', 'h': 'hi'}, 'content'
    )
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
    lines = response_error('500 Internal Server Error', 'hi').split('\r\n')
    assert '500 Internal Server Error' in lines[0]


def test_response_error_header():
    from server import response_error
    lines = response_error('500 Internal Server Error', 'hi').split('\r\n')
    assert any('content-type:' in line.lower() for line in lines)


def test_parse_method():
    from server import parse_request, HTTPException
    request = 'HEAD /index HTTP/1.1\r\nHost: 127.0.0.1'
    with pytest.raises(HTTPException):
        parse_request(request)


def test_parse_version():
    from server import parse_request, HTTPException
    request = 'GET /index HTTP/1.2\r\nHost: 127.0.0.1'
    with pytest.raises(HTTPException):
        parse_request(request)


def test_parse_host():
    from server import parse_request, HTTPException
    request = 'GET /index HTTP/1.2\r\n'
    with pytest.raises(HTTPException):
        parse_request(request)


def test_empty_request():
    from server import parse_request, HTTPException
    request = ''
    with pytest.raises(HTTPException):
        parse_request(request)


def test_parse_proper_status():
    from server import parse_request, HTTPException
    request = 'GET/index HTTP/1.2\r\n'
    with pytest.raises(HTTPException):
        parse_request(request)


def test_combined_headers():
    from server import combine_continued_headers
    headers = [
        'hello: wor',
        ' ld',
        'test: test',
        'test: test'
    ]
    assert 'hello: world' in combine_continued_headers(headers)


def test_combined_headers_error():
    from server import combine_continued_headers, HTTPException
    headers = [
        '  hello: wor',
        ' ld',
        'test: test',
        'test: test'
    ]
    with pytest.raises(HTTPException):
        combine_continued_headers(headers)


def test_combine_header():
    from server import combine_continued_headers
    headers = [
        'hello: wor',
        '    \tld',
        'test: test',
        'test: test'
    ]
    assert 'hello: world' in combine_continued_headers(headers)


def test_parse_headers():
    from server import parse_headers
    headers = parse_headers([
        'hello: world',
        'test: ',
        ' test'
    ])
    assert 'test' in headers
    assert 'hello' in headers


def test_parse_header_error():
    from server import parse_headers, HTTPException
    with pytest.raises(HTTPException):
        parse_headers(['hello world', 'test: ', ' test'])


@pytest.mark.parametrize('uri', URIS)
def test_parse_uri(uri):
    from server import parse_request
    request = 'GET {} HTTP/1.1\r\nHost: www.example.org\r\n'.format(uri)
    assert parse_request(request) == uri


@pytest.mark.parametrize('path, result', PATH_TABLE)
def test_valid_path(path, result):
    from server import valid_path
    assert valid_path(path) == result
