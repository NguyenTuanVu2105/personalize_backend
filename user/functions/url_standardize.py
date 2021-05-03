def url_standardize(save_url):
    url = save_url
    if "http" not in save_url:
        url = 'https://' + save_url
    if "127" in save_url or "localhost" in save_url:
        url = save_url.replace('https', 'http')
    return url
