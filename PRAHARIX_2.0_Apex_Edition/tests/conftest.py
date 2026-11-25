import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def app():
    # Set env vars before import
    os.environ.setdefault('SECRET_KEY', 'test-secret-key-32-bytes-long!!!')
    os.environ.setdefault('ADMIN_USERNAME', 'admin')
    os.environ.setdefault('ADMIN_PASSWORD', 'praharix2026')
    os.environ.setdefault('USER_USERNAME', 'user')
    os.environ.setdefault('USER_PASSWORD', 'user2026')
    import app as application
    application.app.config['TESTING'] = True
    application.app.config['WTF_CSRF_ENABLED'] = False
    return application.app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_client(client):
    with client.session_transaction() as sess:
        sess['role'] = 'admin'
        sess['csrf_token'] = 'test-csrf-token'
    return client

@pytest.fixture
def user_client(client):
    with client.session_transaction() as sess:
        sess['role'] = 'user'
        sess['csrf_token'] = 'test-csrf-token'
    return client

@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / 'test.db'
    return str(db_path)
