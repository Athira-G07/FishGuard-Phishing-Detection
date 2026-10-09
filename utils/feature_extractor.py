from urllib.parse import urlparse
import re


def extract_url_features(url):
    parsed = urlparse(url)

    domain = parsed.netloc
    hostname = parsed.hostname or ""

    features = {}

    features["URLLength"] = len(url)-1
    features["DomainLength"] = len(domain)

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    features["IsDomainIP"] = int(bool(re.match(ip_pattern, hostname)))

    domain_parts = hostname.split(".")
    features["NoOfSubDomain"] = max(0, len(domain_parts) - 2)

    features["IsHTTPS"] = int(parsed.scheme.lower() == "https")

    features["NoOfEqualsInURL"] = url.count("=")
    features["NoOfQMarkInURL"] = url.count("?")
    features["NoOfAmpersandInURL"] = url.count("&")
    features["NoOfDegitsInURL"] = sum(c.isdigit() for c in url)

    return features