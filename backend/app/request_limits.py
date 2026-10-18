from starlette.responses import JSONResponse


class RequestSizeLimitMiddleware:
    """
    Enforce a maximum request-body size on /api/ requests.

    This middleware counts incoming body bytes without buffering or replaying
    the request. This avoids interfering with FastAPI multipart parsing.
    """

    def __init__(self, app, max_body_size: int):
        if max_body_size <= 0:
            raise ValueError("max_body_size must be positive")

        self.app = app
        self.max_body_size = max_body_size

    async def __call__(self, scope, receive, send):
        if (
            scope["type"] != "http"
            or not scope.get("path", "").startswith("/api/")
        ):
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        content_length = headers.get(b"content-length")

        if content_length is not None:
            try:
                declared_size = int(content_length)
            except (TypeError, ValueError):
                declared_size = -1

            if declared_size < 0:
                response = JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid Content-Length header."},
                )
                await response(scope, receive, send)
                return

            if declared_size > self.max_body_size:
                response = JSONResponse(
                    status_code=413,
                    content={
                        "detail": "Request body exceeds the allowed size limit."
                    },
                )
                await response(scope, receive, send)
                return

        total_size = 0
        response_started = False

        async def limited_receive():
            nonlocal total_size

            message = await receive()

            if message["type"] == "http.request":
                total_size += len(message.get("body", b""))

                if total_size > self.max_body_size:
                    raise RequestBodyTooLarge()

            return message

        async def limited_send(message):
            nonlocal response_started

            if message["type"] == "http.response.start":
                response_started = True

            await send(message)

        try:
            await self.app(scope, limited_receive, limited_send)

        except RequestBodyTooLarge:
            if response_started:
                # A response has already started; it cannot safely be replaced.
                raise

            response = JSONResponse(
                status_code=413,
                content={
                    "detail": "Request body exceeds the allowed size limit."
                },
            )
            await response(scope, receive, send)


class RequestBodyTooLarge(Exception):
    """Raised when a streamed request body exceeds the configured limit."""