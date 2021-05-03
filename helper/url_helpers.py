from urllib.parse import urljoin, urlparse


def prune_query_string(url):
    return urljoin(url, urlparse(url).path)
