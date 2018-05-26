from urllib.parse import urlsplit


def remove_url_schema(url):
    split_url = urlsplit(url)
    edited_url = split_url.netloc + split_url.path + split_url.query + split_url.fragment
    return edited_url