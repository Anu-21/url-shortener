import pytest
import fakeredis
from app import create_app


@pytest.fixture
def app():
    """Create Flask app with fakeredis for testing."""
    application = create_app()
    application.config['TESTING'] = True

    # Replace real Redis with fakeredis
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    application.redis = fake_redis

    yield application


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


# ─── Test 1: GET / returns 200 ──────────────────────────────────────
def test_homepage_returns_200(client):
    """GET / should return the homepage with status 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'QuickURL' in response.data


# ─── Test 2: POST /shorten with valid URL ───────────────────────────
def test_shorten_valid_url(client):
    """POST /shorten with a valid URL should return 201 with short_url."""
    response = client.post('/shorten', json={
        'long_url': 'https://www.google.com'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_url' in data
    assert 'short_code' in data
    assert 'long_url' in data
    assert data['long_url'] == 'https://www.google.com'


# ─── Test 3: POST /shorten with invalid URL ─────────────────────────
def test_shorten_invalid_url(client):
    """POST /shorten with an invalid URL should return 400."""
    response = client.post('/shorten', json={
        'long_url': 'not-a-valid-url'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


# ─── Test 4: GET /stats returns 200 with total_urls ─────────────────
def test_stats_returns_200(client):
    """GET /stats should return 200 with total_urls key."""
    response = client.get('/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_urls' in data
    assert 'status' in data
    assert data['status'] == 'healthy'


# ─── Test 5: GET /nonexistentcode returns 404 ───────────────────────
def test_nonexistent_code_returns_404(client):
    """GET /<nonexistent_code> should return 404."""
    response = client.get('/nonexistentcode')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
