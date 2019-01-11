def filter_none(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}


def urljoin(url: str, *parts: str) -> str:
    return "/".join(
        (url.rstrip("/"), *(p.strip("/") for p in parts[:-1]), (parts[-1]).lstrip("/"))
    )
