import asyncio

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, Field
from urllib.parse import urlparse
from pathlib import Path

app = FastAPI(title="RinkLess Link Checker")


def load_patterns(filename: str) -> list[str]:
    """Load domain patterns from file, one per line.
    
    Supports:
    - Comments starting with #
    - Empty lines (ignored)
    - Domain patterns like 'google.com' or '*.google.com'
    """
    path = Path(__file__).parent / filename
    if not path.exists():
        return []
    with open(path) as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def domain_matches(url: str, pattern: str) -> bool:
    """Check if URL's hostname matches the pattern.
    
    Pattern types:
    - 'google.com' matches google.com and all subdomains (*.google.com)
    - '*.google.com' matches only subdomains, not google.com itself
    """
    hostname = urlparse(url).hostname or ""
    hostname = hostname.lower()
    pattern = pattern.lower()

    if pattern.startswith("*."):
        # Wildcard: match subdomains only (not root domain)
        suffix = pattern[1:]  # ".google.com"
        return hostname.endswith(suffix) and hostname != pattern[2:]
    else:
        # Match domain exactly OR as subdomain
        return hostname == pattern or hostname.endswith("." + pattern)


# Load patterns at startup
WHITELIST = load_patterns("whitelist.txt")
BLACKLIST = load_patterns("blacklist.txt")


class LinkCheckRequest(BaseModel):
    url: HttpUrl
    delay: float | None = Field(default=None, description="Optional delay in seconds (for FE testing)")


class LinkCheckResponse(BaseModel):
    url: str
    status: str  # "safe" | "normal" | "unsafe"


@app.post("/check-link")
async def check_link(request: LinkCheckRequest) -> LinkCheckResponse:
    """Check a URL against whitelist and blacklist patterns.
    
    Returns:
    - 'safe' if URL matches a whitelist pattern
    - 'unsafe' if URL matches a blacklist pattern
    - 'normal' if URL matches neither
    
    Optional: pass 'delay' (seconds) to simulate network latency for FE testing.
    """
    # Optional delay for frontend testing
    if request.delay and request.delay > 0:
        await asyncio.sleep(request.delay)

    url = str(request.url)

    if any(domain_matches(url, p) for p in WHITELIST):
        return LinkCheckResponse(url=url, status="safe")
    elif any(domain_matches(url, p) for p in BLACKLIST):
        return LinkCheckResponse(url=url, status="unsafe")
    else:
        return LinkCheckResponse(url=url, status="normal")


@app.get("/health")
def health_check():
    """Health check endpoint for Railway."""
    return {"status": "ok"}
