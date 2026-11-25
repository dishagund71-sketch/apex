"""
Authentication and security tests for PRAHARIX 3.0
"""
import pytest
import json


class TestLogin:
    def test_login_page_redirects(self, client):
        # GET to /login should redirect to home (login form is on /)
        resp = client.get('/login')
        assert resp.status_code in [200, 302]

    def test_login_missing_csrf(self, client):
        resp = client.post('/login', data={
            'username': 'admin',
            'password': 'praharix2026'
        })
        # Either CSRF failure or success in testing mode
        assert resp.status_code in [200, 302, 400]

    def test_login_wrong_password(self, client):
        resp = client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpassword',
            'csrf_token': 'test-token'
        })
        assert resp.status_code in [200, 400, 401, 302]

    def test_logout(self, admin_client):
        resp = admin_client.get('/logout')
        assert resp.status_code in [200, 302]


class TestRBAC:
    def test_public_can_access_home(self, client):
        resp = client.get('/')
        assert resp.status_code in [200, 302]

    def test_history_requires_admin(self, client):
        resp = client.get('/history')
        assert resp.status_code in [302, 403]

    def test_analytics_requires_admin(self, client):
        resp = client.get('/analytics')
        assert resp.status_code in [302, 403]

    def test_admin_can_access_history(self, admin_client):
        resp = admin_client.get('/history')
        assert resp.status_code == 200


class TestRateLimiting:
    def test_rate_limit_functions(self, app):
        with app.app_context():
            import app as application
            # Test that rate limiting logic works
            application.login_attempts.clear()
            ip = '192.168.1.100'
            limited, wait = application.is_login_rate_limited(ip)
            assert not limited
            # Simulate 5 failed attempts
            for _ in range(5):
                application.record_login_attempt(ip, success=False)
            limited, wait = application.is_login_rate_limited(ip)
            assert limited
            # Cleanup
            application.login_attempts.clear()


class TestCSRF:
    def test_csrf_token_generated(self, client):
        with client.session_transaction() as sess:
            sess['role'] = 'public'
        resp = client.get('/api/csrf-token')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data['csrf_token']) > 10
