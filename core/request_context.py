from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import generate_request_id, logger
import time

class RequestContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = generate_request_id()
        start_time = time.time()

        response = None
        try:
            response = await call_next(request)
            return response
        finally:
            latency = round((time.time() - start_time) * 1000, 2)

            logger.info(
                f"request_id={request_id} "
                f"path={request.url.path} "
                f"method={request.method} "
                f"status={response.status_code if response else 'error'} "
                f"latency_ms={latency}"
            )
