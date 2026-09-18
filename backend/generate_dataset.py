import random
import csv

random.seed(42)

LEGIT_DOMAINS = [
    "google.com", "github.com", "wikipedia.org", "microsoft.com",
    "amazon.com", "linkedin.com", "youtube.com", "facebook.com",
    "apple.com", "netflix.com", "nytimes.com", "bbc.com",
    "stackoverflow.com", "reddit.com", "spotify.com", "dropbox.com",
    "weather.com", "cnn.com", "indeed.com", "zoom.us", "quora.com",
    "medium.com", "coursera.org", "khanacademy.org", "airbnb.com",
    "booking.com", "irctc.co.in", "hdfcbank.com", "icicibank.com",
]

LEGIT_PATHS = [
    "", "/", "/search?q=news", "/watch?v=abc123", "/in/johndoe",
    "/questions/12345", "/r/technology", "/articles/2026/tech",
    "/products/laptop", "/docs/getting-started", "/blog/post-1",
]

PHISHING_BRAND_WORDS = [
    "paypal", "amazon", "netflix", "apple", "microsoft", "bank",
    "chase", "wellsfargo", "google", "facebook", "instagram",
]

PHISHING_KEYWORDS = [
    "login", "verify", "secure", "update", "free", "bonus",
    "account", "confirm", "password", "signin", "banking",
    "reward", "suspended", "unlock",
]

PHISHING_TLDS = [".xyz", ".top", ".info", ".online", ".click", ".site", ".tk"]


def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))


def make_legit_url():
    domain = random.choice(LEGIT_DOMAINS)
    path = random.choice(LEGIT_PATHS)
    scheme = "https"
    use_www = random.random() < 0.4
    host = f"www.{domain}" if use_www else domain
    return f"{scheme}://{host}{path}"


def make_phishing_url():
    style = random.choice(["ip", "keyword_subdomain", "typosquat", "long_suspicious"])
    scheme = random.choice(["http", "http", "https"])

    if style == "ip":
        return f"http://{random_ip()}/{random.choice(PHISHING_KEYWORDS)}"

    if style == "keyword_subdomain":
        brand = random.choice(PHISHING_BRAND_WORDS)
        kw1 = random.choice(PHISHING_KEYWORDS)
        kw2 = random.choice(PHISHING_KEYWORDS)
        tld = random.choice(PHISHING_TLDS)
        return f"{scheme}://{kw1}-{brand}-{kw2}{tld}/{random.choice(PHISHING_KEYWORDS)}"

    if style == "typosquat":
        brand = random.choice(PHISHING_BRAND_WORDS)
        suffix = random.choice(["-secure", "-verify", "-support", "1"])
        tld = random.choice(PHISHING_TLDS)
        return f"{scheme}://{brand}{suffix}{tld}/{random.choice(PHISHING_KEYWORDS)}"

    parts = random.sample(PHISHING_KEYWORDS, k=random.randint(3, 5))
    tld = random.choice(PHISHING_TLDS)
    return f"{scheme}://{'-'.join(parts)}{tld}/account/{random.choice(PHISHING_KEYWORDS)}?id=" + str(random.randint(1000, 99999))


def generate(n_per_class=1500):
    rows = []
    for _ in range(n_per_class):
        rows.append((make_legit_url(), 0))
    for _ in range(n_per_class):
        rows.append((make_phishing_url(), 1))
    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    rows = generate(1500)
    with open("dataset.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "label"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows -> dataset.csv")