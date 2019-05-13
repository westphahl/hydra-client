import urllib.parse


def filter_none(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}


def urljoin(base: str, *parts: str, query: dict = None) -> str:
    components = urllib.parse.urlparse(base)
    joined = '/'.join([components.path.rstrip('/'), *(part.strip('/') for part in parts)])
    if query is not None and isinstance(query, dict):
        url_query = urllib.parse.urlencode(dict(query))
    else:
        url_query = components.query
    result = urllib.parse.ParseResult(
        scheme=components.scheme,
        netloc=components.netloc,
        path=joined,
        params=components.params,
        query=url_query,
        fragment=components.fragment,
    )
    return urllib.parse.urlunparse(result)
