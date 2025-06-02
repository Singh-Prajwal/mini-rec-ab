import random
from fastapi import Request

def choose_variant(request: Request):
    """50/50 split stored in cookie."""
    cookie = request.cookies.get("variant")
    if cookie in ("A", "B"):
        return cookie
    variant = random.choice(["A", "B"])
    return variant

def log_event(user_ip: str, variant: str, query: str):
    # Real life: send to PostHog or Mixpanel
    print(f"EVENT | ip={user_ip} variant={variant} query='{query}'")