# -*- coding: utf-8 -*-

"""Test HTTP functions."""
import pytest


def test_build_response():
    from server import build_response
    response = build_response('stats', ['header', 'etc'], 'content')
    assert 'stats\r\n' in response
    assert 'header\r\n' in response
    assert 'content' in response
    assert '\r\n\r\n' in response


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


def test_parse_method():
    from server import parse_request, HTTPException
    request = 'HEAD /index HTTP/1.1\r\nHost: 127.0.0.1'
    with pytest.raises(HTTPException):
        parse_request(request)
