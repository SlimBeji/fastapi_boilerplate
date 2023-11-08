from urllib.parse import urlparse


class DomainNotValid(ValueError):
    pass


def domain_validation(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc
    scheme = parsed.scheme
    if not domain:
        raise DomainNotValid("'%s' does not contain a valid domain name." % url)

    if scheme:
        return f"{scheme}://{domain}"

    return domain
