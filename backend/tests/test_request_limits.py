import asyncio

from app.request_limits import RequestSizeLimitMiddleware


def make_scope(headers=None, path="/api/test"):
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": headers or [],
        "client": ("testclient", 123),
        "server": ("testserver", 80),
    }


def run_asgi(app, scope, messages):
    sent = []
    queue = list(messages)

    async def receive():
        if queue:
            return queue.pop(0)
        return {"type": "http.disconnect"}

    async def send(message):
        sent.append(message)

    asyncio.run(app(scope, receive, send))
    return sent


def simple_app(scope, receive, send):
    async def run():
        chunks = []
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                break
            chunks.append(message.get("body", b""))
            if not message.get("more_body", False):
                break

        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"".join(chunks),
            "more_body": False,
        })

    return run()


def test_streamed_oversized_body_without_content_length_returns_413():
    middleware = RequestSizeLimitMiddleware(simple_app, max_body_size=5)
    sent = run_asgi(
        middleware,
        make_scope(),
        [
            {"type": "http.request", "body": b"123", "more_body": True},
            {"type": "http.request", "body": b"456", "more_body": False},
        ],
    )
    start = next(m for m in sent if m["type"] == "http.response.start")
    body = next(m for m in sent if m["type"] == "http.response.body")
    assert start["status"] == 413
    assert b"allowed size limit" in body["body"]


def test_declared_oversized_body_returns_413():
    middleware = RequestSizeLimitMiddleware(simple_app, max_body_size=5)
    sent = run_asgi(
        middleware,
        make_scope(headers=[(b"content-length", b"6")]),
        [{"type": "http.request", "body": b"123456", "more_body": False}],
    )
    start = next(m for m in sent if m["type"] == "http.response.start")
    assert start["status"] == 413


def test_body_under_limit_reaches_app_unchanged():
    middleware = RequestSizeLimitMiddleware(simple_app, max_body_size=5)
    sent = run_asgi(
        middleware,
        make_scope(),
        [{"type": "http.request", "body": b"12345", "more_body": False}],
    )
    start = next(m for m in sent if m["type"] == "http.response.start")
    body = next(m for m in sent if m["type"] == "http.response.body")
    assert start["status"] == 200
    assert body["body"] == b"12345"


def test_non_api_path_is_not_limited():
    middleware = RequestSizeLimitMiddleware(simple_app, max_body_size=5)
    sent = run_asgi(
        middleware,
        make_scope(path="/"),
        [{"type": "http.request", "body": b"123456", "more_body": False}],
    )
    start = next(m for m in sent if m["type"] == "http.response.start")
    assert start["status"] == 200
