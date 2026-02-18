from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.rate_limit import RateLimiter

rate_limiter = RateLimiter(limit=10, window_seconds=60)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(status_code=429, detail="Too many requests")

        return await call_next(request)
