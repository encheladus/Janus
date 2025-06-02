import re
import requests
from ..spoof_useragent import get_random_useragent, make_request_with_useragent

def test_get_random_useragent_returns_string_success():
    """
    Test that get_random_useragent() returns a non-empty string
    that contains 'Mozilla', which is typical for modern browsers.
    """
    ua = get_random_useragent()
    assert isinstance(ua, str)
    assert len(ua) > 10
    assert "Mozilla" in ua

def test_useragent_format_success():
    """
    Test that the returned User-Agent follows a basic 'Mozilla/5.0 (...)' format.
    This ensures the output matches the general structure of valid user agents.
    """
    ua = get_random_useragent()
    assert re.match(r"Mozilla\/5\.0 \(.+\)", ua)

def test_make_request_with_useragent_success():
    """
    Test that make_request_with_useragent() sends a successful request
    to httpbin.org and that the 'User-Agent' is present in the response headers.
    """
    url = "https://httpbin.org/headers"
    response = make_request_with_useragent(url)
    assert response is not None
    assert response.status_code == 200
    data = response.json()
    assert "User-Agent" in data["headers"]

def test_make_request_with_custom_useragent_success():
    """
    Test that a custom User-Agent string is properly used in the request,
    and that it appears in the HTTP response from httpbin.org.
    """
    url = "https://httpbin.org/headers"
    fake_ua = "MyCustomUserAgent/1.0"
    response = make_request_with_useragent(url, user_agent=fake_ua)
    assert response is not None
    assert fake_ua in response.text

def test_make_request_with_invalid_url():
    """
    Test that make_request_with_useragent() handles an invalid URL gracefully
    and returns None instead of raising an exception.
    """
    invalid_url = "http://nonexistent.localhost"
    response = make_request_with_useragent(invalid_url)
    assert response is None