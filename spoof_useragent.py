import requests
from random import choice

def get_random_useragent():
    """
    Returns a random User-Agent string.

    Attempts to use the `fake_useragent` library to generate a User-Agent.
    If unavailable, falls back to a static list of common User-Agents
    covering Chrome, Firefox, Safari, and Edge across Windows, macOS, and Linux.

    Returns:
        str: A random User-Agent string.
    """
    try:
        from fake_useragent import UserAgent
        ua = UserAgent()
        return ua.random
    except Exception:
        static_user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36 Edg/123.0.2420.81',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36 Edg/123.0.2420.81',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36 Edg/123.0.2420.81'
        ]
        return choice(static_user_agents)

def make_request_with_useragent(url, user_agent=None):
    """
    Sends a GET request to the specified URL using a custom or random User-Agent.

    Args:
        url (str): The target URL.
        user_agent (Optional[str]): A specific User-Agent string to use.
            If None, a random one is selected.

    Returns:
        Optional[requests.Response]: The HTTP response object, or None if an error occurs.
    """
    if user_agent is None:
        user_agent = get_random_useragent()
    print(user_agent)
    headers = {'User-Agent': user_agent}
    return requests.get(url, headers=headers, timeout=10)