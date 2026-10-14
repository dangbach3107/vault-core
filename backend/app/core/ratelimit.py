"""In-memory sliding-window limiter for failed logins (single-instance deployment)."""
import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import HTTPException

WINDOW_SECONDS = 15 * 60
LIMITS = {"user": 5, "ip": 30}


class LoginLimiter:
    def __init__(self) -> None:
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def _prune(self, key: str, now: float) -> deque[float]:
        events = self._events[key]
        while events and now - events[0] > WINDOW_SECONDS:
            events.popleft()
        return events

    def check(self, username: str, ip: str) -> None:
        now = time.monotonic()
        with self._lock:
            for kind, key in (("user", f"user:{username}"), ("ip", f"ip:{ip}")):
                events = self._prune(key, now)
                if len(events) >= LIMITS[kind]:
                    wait = int(WINDOW_SECONDS - (now - events[0])) + 1
                    raise HTTPException(429, "Đăng nhập sai quá nhiều lần. Hãy thử lại sau ít phút.", headers={"Retry-After": str(wait)})

    def failure(self, username: str, ip: str) -> None:
        now = time.monotonic()
        with self._lock:
            self._events[f"user:{username}"].append(now)
            self._events[f"ip:{ip}"].append(now)

    def success(self, username: str) -> None:
        with self._lock:
            self._events.pop(f"user:{username}", None)
