"""
Liste statique de domaines légitimes bien connus, utilisée comme classe
"non-malveillante" pour entraîner le classifieur de phishing.

Ces domaines sont volontairement des sites mondiaux très établis, peu
susceptibles de changer ou de poser un doute quelconque sur leur légitimité.
"""

BENIGN_DOMAINS = [
    "google.com", "youtube.com", "wikipedia.org", "amazon.com", "microsoft.com",
    "apple.com", "github.com", "stackoverflow.com", "linkedin.com", "reddit.com",
    "netflix.com", "twitter.com", "x.com", "instagram.com", "facebook.com",
    "office.com", "live.com", "yahoo.com", "bing.com", "adobe.com",
    "mozilla.org", "python.org", "npmjs.com", "docker.com", "wordpress.com",
    "cloudflare.com", "digitalocean.com", "gitlab.com", "bitbucket.org", "atlassian.com",
    "salesforce.com", "oracle.com", "ibm.com", "intel.com", "nvidia.com",
    "spotify.com", "dropbox.com", "zoom.us", "slack.com", "notion.so",
    "paypal.com", "stripe.com", "visa.com", "mastercard.com", "americanexpress.com",
    "bbc.com", "cnn.com", "nytimes.com", "reuters.com", "lemonde.fr",
    "wikipedia.fr", "gouv.fr", "service-public.fr", "impots.gouv.fr", "ameli.fr",
    "un.org", "who.int", "europa.eu", "worldbank.org", "imf.org",
    "harvard.edu", "mit.edu", "stanford.edu", "ox.ac.uk", "cam.ac.uk",
    "ensa.ac.ma", "um5.ac.ma", "uh2c.ac.ma", "emi.ac.ma", "enim.ac.ma",
    "booking.com", "airbnb.com", "tripadvisor.com", "expedia.com", "uber.com",
    "ebay.com", "etsy.com", "aliexpress.com", "shopify.com", "walmart.com",
    "samsung.com", "sony.com", "lg.com", "huawei.com", "xiaomi.com",
    "wix.com", "squarespace.com", "canva.com", "figma.com", "trello.com",
    "asana.com", "monday.com", "hubspot.com", "mailchimp.com", "zendesk.com",
    "coursera.org", "udemy.com", "khanacademy.org", "edx.org", "duolingo.com",
    "medium.com", "quora.com", "pinterest.com", "tumblr.com", "discord.com",
    "telegram.org", "whatsapp.com", "signal.org", "protonmail.com", "gmail.com",
]

# Modèles de chemins réalistes (pas juste des racines de domaine "https://site.com/").
# Volontairement variés : certains courts, d'autres longs, avec paramètres, chiffres,
# voire des pages de connexion légitimes ("/account/login") — pour forcer le modèle à
# ne pas se reposer uniquement sur "présence d'un chemin" ou "mot-clé login" comme
# signal trivial de phishing.
PATH_TEMPLATES = [
    "",
    "/about",
    "/contact",
    "/products",
    "/search?q=machine+learning",
    "/blog/2026/08/05/annual-report",
    "/docs/api/v2/reference",
    "/user/settings/profile",
    "/news/technology/2026/latest-innovations",
    "/support/faq",
    "/careers/openings",
    "/watch?v=dQw4w9WgXcQ",
    "/wiki/Artificial_intelligence",
    "/article/2026/economy-outlook-morocco",
    "/store/category/electronics",
    "/account/login",
]


def generate_benign_urls():
    """Génère plusieurs URLs réalistes par domaine, avec des chemins variés,
    de façon déterministe (reproductible d'une exécution à l'autre)."""
    urls = []
    for i, domain in enumerate(BENIGN_DOMAINS):
        chosen_paths = [PATH_TEMPLATES[(i + j) % len(PATH_TEMPLATES)] for j in range(3)]
        for path in chosen_paths:
            urls.append(f"https://{domain}{path}")
    return urls


BENIGN_URLS = generate_benign_urls()