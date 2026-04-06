import string
import secrets
import redis
import validators


def generate_short_code(length=6):
    """Generate a cryptographically secure random alphanumeric short code."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def validate_url(url):
    """Return True if *url* is a valid HTTP/HTTPS URL, False otherwise."""
    if not url:
        return False
    return validators.url(url) is True


def get_redis_client(redis_url='redis://localhost:6379'):
    """Create and return a Redis client from the given URL."""
    return redis.Redis.from_url(redis_url, decode_responses=True)
