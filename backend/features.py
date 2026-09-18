from urllib.parse import urlparse

TRUSTED_DOMAINS = [
    "google.com", "github.com", "wikipedia.org", "microsoft.com",
    "amazon.com", "linkedin.com", "youtube.com", "facebook.com",
    "apple.com", "netflix.com", "weather.com", "cnn.com", "bbc.com",
    "nytimes.com", "reddit.com", "stackoverflow.com", "spotify.com",
    "dropbox.com", "twitter.com", "x.com", "instagram.com",
    "yahoo.com", "bing.com", "office.com", "adobe.com", "paypal.com",
    "ebay.com", "walmart.com", "target.com", "indeed.com", "zoom.us",
    "salesforce.com", "wordpress.com", "medium.com", "quora.com",
]

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "free", "bonus",
    "account", "confirm", "password", "signin", "banking",
]


def extract_features(url: str) -> dict:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    domain = parsed.netloc.replace("www.", "")
    path_and_query = (parsed.path + "?" + parsed.query).lower()

    is_https = 1 if parsed.scheme == "https" else 0

    is_trusted = 1 if any(
        domain == d or domain.endswith("." + d) for d in TRUSTED_DOMAINS
    ) else 0

    is_ip_domain = 1 if domain.replace(".", "").isdigit() else 0

    url_length = len(url)

    keyword_count = sum(
        1 for kw in SUSPICIOUS_KEYWORDS if kw in path_and_query or kw in domain
    )

    subdomain_count = domain.count(".")
    hyphen_count = domain.count("-")
    digit_ratio = (sum(c.isdigit() for c in domain) / len(domain)) if domain else 0
    at_symbol = 1 if "@" in url else 0

    return {
        "is_https": is_https,
        "is_trusted": is_trusted,
        "is_ip_domain": is_ip_domain,
        "url_length": url_length,
        "keyword_count": keyword_count,
        "subdomain_count": subdomain_count,
        "hyphen_count": hyphen_count,
        "digit_ratio": digit_ratio,
        "at_symbol": at_symbol,
    }


FEATURE_ORDER = [
    "is_https", "is_trusted", "is_ip_domain", "url_length",
    "keyword_count", "subdomain_count", "hyphen_count",
    "digit_ratio", "at_symbol",
]


def features_to_vector(feat: dict) -> list:
    return [feat[k] for k in FEATURE_ORDER]