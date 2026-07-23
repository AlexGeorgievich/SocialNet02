"""Optional Redis JSON cache with graceful fallback when Redis is unavailable."""

import json
import logging
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

from config import CACHE_TTL_SECONDS, REDIS_URL


logger = logging.getLogger(__name__)
redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=0.3,
    socket_timeout=0.5,
)


def cache_key(mode: str, namespace: str, *parts: Any) -> str:
    suffix = ":".join("" if part is None else str(part) for part in parts)
    return f"sart:{mode}:{namespace}:{suffix}"


def get_json(key: str):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value is not None else None
    except (RedisError, json.JSONDecodeError) as exc:
        logger.warning("Redis cache read skipped: %s", exc)
        return None


def set_json(key: str, value: Any, ttl: int = CACHE_TTL_SECONDS) -> None:
    try:
        redis_client.setex(
            key,
            ttl,
            json.dumps(value, ensure_ascii=False, default=str),
        )
    except RedisError as exc:
        logger.warning("Redis cache write skipped: %s", exc)


def invalidate_all() -> None:
    """Invalidate derived API data after any content-changing operation."""
    try:
        keys = list(redis_client.scan_iter(match="sart:*", count=200))
        if keys:
            redis_client.delete(*keys)
    except RedisError as exc:
        logger.warning("Redis cache invalidation skipped: %s", exc)


def cache_available() -> bool:
    try:
        return bool(redis_client.ping())
    except RedisError:
        return False
