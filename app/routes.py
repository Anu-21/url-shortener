from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, redirect, render_template, current_app
from .utils import generate_short_code, validate_url

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Render the frontend UI."""
    return render_template('index.html')


@bp.route('/shorten', methods=['POST'])
def shorten():
    """Shorten a long URL and store it in Redis."""
    data = request.get_json(silent=True) or {}
    long_url = data.get('long_url', '').strip()

    if not long_url:
        return jsonify({'error': 'long_url is required'}), 400

    if not validate_url(long_url):
        return jsonify({'error': 'Invalid URL format'}), 400

    r = current_app.redis

    # Generate a unique short code
    short_code = generate_short_code()
    while r.exists(f'url:{short_code}'):
        short_code = generate_short_code()

    # Store mapping with no expiry
    r.set(f'url:{short_code}', long_url)

    # Increment global counter
    r.incr('total_urls')

    created_at = datetime.now(timezone.utc).isoformat()

    # Store creation timestamp
    r.set(f'created:{short_code}', created_at)

    short_url = f'{request.host_url}{short_code}'

    return jsonify({
        'short_url': short_url,
        'short_code': short_code,
        'long_url': long_url,
        'created_at': created_at
    }), 201


@bp.route('/stats', methods=['GET'])
def stats():
    """Return app stats — total URLs created and health status."""
    r = current_app.redis
    total = r.get('total_urls') or 0
    return jsonify({
        'total_urls': int(total),
        'status': 'healthy'
    }), 200


@bp.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Look up the short code in Redis and redirect, or return 404."""
    r = current_app.redis
    long_url = r.get(f'url:{short_code}')

    if not long_url:
        return jsonify({'error': 'Short URL not found'}), 404

    # Increment per-code click counter
    r.incr(f'clicks:{short_code}')

    return redirect(long_url, code=302)
