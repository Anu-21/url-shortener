import os
from flask import Flask
from .utils import get_redis_client


def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='../static'
    )

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379')

    # Attach Redis client to app
    app.redis = get_redis_client(app.config['REDIS_URL'])

    # Register routes blueprint
    from .routes import bp
    app.register_blueprint(bp)

    return app
