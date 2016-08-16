# -*- coding: utf-8 -*-

"""Test HTTP functions."""


def test_response_ok_1():
    from server import response_ok
    lines = response_ok().split('\r\n')
    assert '200 OK' in lines[0]


def test_response_ok_2():
    from server import response_ok
    lines = response_ok().split('\r\n')
    assert any('content-type:' in line.lower() for line in lines)
