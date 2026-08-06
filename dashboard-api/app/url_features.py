
import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm",
    "signin", "banking", "password", "webscr", "suspend", "urgent",
]

IP_ADDRESS_PATTERN = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def extract_features(url):
    """Retourne un dictionnaire de caractéristiques lexicales pour une URL donnée."""
    parsed = urlparse(url if "://" in url else f"http://{url}")
    netloc = parsed.netloc.split(":")[0]
    path = parsed.path or ""
    full = url.lower()

    return {
        "url_length": len(url),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": sum(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_subdomains": max(netloc.count(".") - 1, 0),
        "has_ip_address": int(bool(IP_ADDRESS_PATTERN.match(netloc))),
        "has_at_symbol": int("@" in url),
        "uses_https": int(url.lower().startswith("https")),
        "path_length": len(path),
        "suspicious_keyword_count": sum(keyword in full for keyword in SUSPICIOUS_KEYWORDS),
    }


FEATURE_NAMES = [
    "url_length", "num_digits", "num_special_chars", "num_dots", "num_hyphens",
    "num_subdomains", "has_ip_address", "has_at_symbol", "uses_https",
    "path_length", "suspicious_keyword_count",
]