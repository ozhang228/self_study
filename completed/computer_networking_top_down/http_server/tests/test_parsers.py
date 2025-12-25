from urllib.parse import urlparse

import pytest

from utils.parsers import parse_request_line


def test_get_requests():
    # GET /
    req, err = parse_request_line("GET / HTTP/1.1")
    assert err is None
    assert req["method"] == "GET"
    assert req["version"] == "HTTP/1.1"
    assert req["uri"] == urlparse("/")

    # GET /index.html
    req, err = parse_request_line("GET /index.html HTTP/1.1")
    assert err is None
    assert req["method"] == "GET"
    assert req["version"] == "HTTP/1.1"
    assert req["uri"] == urlparse("/index.html")


def test_head_request():
    req, err = parse_request_line("HEAD /status HTTP/1.1")
    assert err is None
    assert req["method"] == "HEAD"
    assert req["version"] == "HTTP/1.1"
    assert req["uri"] == urlparse("/status")


def test_post_and_put_requests():
    # POST
    req, err = parse_request_line("POST /submit-form HTTP/1.1")
    assert err is None
    assert req["method"] == "POST"
    assert req["uri"] == urlparse("/submit-form")

    # PUT
    req, err = parse_request_line("PUT /resource/123 HTTP/1.1")
    assert err is None
    assert req["method"] == "PUT"
    assert req["uri"] == urlparse("/resource/123")


def test_delete_and_trace_requests():
    # DELETE with query
    req, err = parse_request_line("DELETE /items?id=1 HTTP/1.1")
    assert err is None
    assert req["method"] == "DELETE"
    assert req["uri"] == urlparse("/items?id=1")

    # TRACE
    req, err = parse_request_line("TRACE /trace HTTP/1.1")
    assert err is None
    assert req["method"] == "TRACE"
    assert req["uri"] == urlparse("/trace")


def test_options_wildcard():
    req, err = parse_request_line("OPTIONS * HTTP/1.1")
    assert err is None
    assert req["method"] == "OPTIONS"
    assert req["uri"] == urlparse("*")
    assert req["version"] == "HTTP/1.1"


def test_invalid_http_versions():
    for version in ("HTTP/1.0", "HTTP/2.0"):
        line = f"GET / {version}"
        _, err = parse_request_line(line)
        assert err is not None


def test_wrong_number_of_parts():
    for line in ("GET /", "GET", "", "POST /path HTTP/1.1 extra"):
        _, err = parse_request_line(line)
        assert err is not None


def test_unsupported_or_miscased_methods():
    for line in ("get / HTTP/1.1", "UNKNOWN / HTTP/1.1"):
        _, err = parse_request_line(line)
        assert err is not None


def test_star_uri_rules():
    # non-OPTIONS cannot use '*'
    _, err = parse_request_line("GET * HTTP/1.1")
    assert err is not None

    _, err = parse_request_line("POST * HTTP/1.1")
    assert err is not None


def test_invalid_uris_and_whitespace():
    # space inside URI
    _, err = parse_request_line("GET /in valid HTTP/1.1")
    assert err is not None

    # tabs instead of spaces
    _, err = parse_request_line("GET\t/\tHTTP/1.1")
    assert err is not None
