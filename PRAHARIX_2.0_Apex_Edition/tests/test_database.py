"""
Database tests for PRAHARIX 3.0
"""
import pytest
import sqlite3
import os


class TestDatabaseSchema:
    def test_db_exists(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        assert os.path.exists(db_path), 'praharix.db should exist after init_db()'

    def test_incidents_table_exists(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
        result = cur.fetchone()
        conn.close()
        assert result is not None

    def test_user_incidents_table_exists(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_incidents'")
        result = cur.fetchone()
        conn.close()
        assert result is not None

    def test_audit_log_table_exists(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_log'")
        result = cur.fetchone()
        conn.close()
        assert result is not None

    def test_incidents_columns(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('PRAGMA table_info(incidents)')
        cols = [row[1] for row in cur.fetchall()]
        conn.close()
        for col in ['event_id', 'place', 'magnitude', 'latitude', 'longitude', 'risk', 'threat_level']:
            assert col in cols

    def test_seed_incidents_exist(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM user_incidents')
        count = cur.fetchone()[0]
        conn.close()
        assert count >= 1

    def test_parameterized_insert(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'praharix.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        test_id = 'TEST-INJECT-001'
        # Test SQL injection safety via parameterized query
        malicious_input = "'; DROP TABLE user_incidents; --"
        cur.execute(
            'INSERT OR IGNORE INTO user_incidents (incident_id, incident_type, district, severity, description, reported_by) VALUES (?, ?, ?, ?, ?, ?)',
            (test_id, 'TEST', malicious_input, 'LOW', 'SQL injection safety test', 'pytest')
        )
        conn.commit()
        # Verify table still exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_incidents'")
        assert cur.fetchone() is not None
        # Cleanup
        cur.execute('DELETE FROM user_incidents WHERE incident_id = ?', (test_id,))
        conn.commit()
        conn.close()
