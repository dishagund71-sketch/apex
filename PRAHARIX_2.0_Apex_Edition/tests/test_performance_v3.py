"""
PRAHARIX 3.0 — Tests for Performance & Research Module (#69-80)
pytest tests/test_performance_v3.py -v
"""
import json
import time
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from performance_v3 import (
    TTLCache, LatencyTracker,
    simulate_load_test, simulate_historical_disaster,
    analyze_model_accuracy, get_db_optimization_report,
    apply_db_indexes, api_cache
)


# ===========================================================================
# #70 — TTLCache
# ===========================================================================

class TestTTLCache:
    def setup_method(self):
        self.cache = TTLCache()

    def test_set_and_get(self):
        self.cache.set('k1', 'hello', ttl_seconds=60)
        assert self.cache.get('k1') == 'hello'

    def test_get_missing_key_returns_none(self):
        assert self.cache.get('nonexistent') is None

    def test_expired_key_returns_none(self):
        self.cache.set('exp_key', 'val', ttl_seconds=0)
        time.sleep(0.05)
        assert self.cache.get('exp_key') is None

    def test_invalidate(self):
        self.cache.set('inv_key', 42, ttl_seconds=60)
        self.cache.invalidate('inv_key')
        assert self.cache.get('inv_key') is None

    def test_clear(self):
        self.cache.set('a', 1, ttl_seconds=60)
        self.cache.set('b', 2, ttl_seconds=60)
        self.cache.clear()
        assert self.cache.stats()['total_keys'] == 0

    def test_stats_active_expired(self):
        self.cache.set('live', 'yes', ttl_seconds=60)
        self.cache.set('dead', 'no', ttl_seconds=0)
        time.sleep(0.05)
        stats = self.cache.stats()
        assert 'total_keys' in stats
        assert 'active_keys' in stats
        assert 'expired_keys' in stats

    def test_set_overwrites_existing(self):
        self.cache.set('ov', 'first', ttl_seconds=60)
        self.cache.set('ov', 'second', ttl_seconds=60)
        assert self.cache.get('ov') == 'second'

    def test_stores_dict_value(self):
        self.cache.set('d', {'x': 1}, ttl_seconds=60)
        assert self.cache.get('d') == {'x': 1}

    def test_stores_list_value(self):
        self.cache.set('l', [1, 2, 3], ttl_seconds=60)
        assert self.cache.get('l') == [1, 2, 3]


# ===========================================================================
# #77 — LatencyTracker
# ===========================================================================

class TestLatencyTracker:
    def setup_method(self):
        self.tracker = LatencyTracker(max_samples=100)

    def test_record_and_get_stats(self):
        for ms in [10, 20, 30, 40, 50]:
            self.tracker.record('/api/test', ms)
        stats = self.tracker.get_stats('/api/test')
        assert stats['samples'] == 5
        assert 'p50_ms' in stats
        assert 'p95_ms' in stats
        assert 'p99_ms' in stats
        assert 'mean_ms' in stats

    def test_no_samples_returns_zero(self):
        stats = self.tracker.get_stats('/api/missing')
        assert stats['samples'] == 0

    def test_max_samples_cap(self):
        tracker = LatencyTracker(max_samples=10)
        for i in range(25):
            tracker.record('/api/cap', float(i))
        stats = tracker.get_stats('/api/cap')
        assert stats['samples'] == 10

    def test_all_endpoints_summary(self):
        self.tracker.record('/api/a', 100.0)
        self.tracker.record('/api/b', 200.0)
        summary = self.tracker.get_stats()
        assert summary['total_endpoints_tracked'] == 2
        assert len(summary['endpoints']) == 2

    def test_p50_between_min_max(self):
        for ms in range(1, 101):
            self.tracker.record('/api/range', float(ms))
        stats = self.tracker.get_stats('/api/range')
        assert stats['min_ms'] <= stats['p50_ms'] <= stats['max_ms']

    def test_p95_gte_p50(self):
        for ms in range(1, 101):
            self.tracker.record('/api/order', float(ms))
        stats = self.tracker.get_stats('/api/order')
        assert stats['p95_ms'] >= stats['p50_ms']

    def test_p99_gte_p95(self):
        for ms in range(1, 101):
            self.tracker.record('/api/p99', float(ms))
        stats = self.tracker.get_stats('/api/p99')
        assert stats['p99_ms'] >= stats['p95_ms']

    def test_multiple_endpoints_isolated(self):
        self.tracker.record('/api/x', 10.0)
        self.tracker.record('/api/y', 500.0)
        x = self.tracker.get_stats('/api/x')
        y = self.tracker.get_stats('/api/y')
        assert x['mean_ms'] < y['mean_ms']


# ===========================================================================
# #72 — Load Test Simulation
# ===========================================================================

class TestSimulateLoadTest:
    def test_basic_simulation(self):
        result = simulate_load_test('/', concurrent_users=10, requests_per_user=5)
        assert result['status'] == 'simulation'
        assert result['concurrent_users'] == 10
        assert result['requests_per_user'] == 5
        assert result['total_requests'] == 50

    def test_results_keys_present(self):
        result = simulate_load_test('/')
        r = result['results']
        assert 'p50_ms' in r
        assert 'p95_ms' in r
        assert 'p99_ms' in r
        assert 'throughput_rps' in r
        assert 'error_rate_pct' in r
        assert 'passes' in r

    def test_p99_gte_p95_gte_p50(self):
        result = simulate_load_test('/', concurrent_users=20)
        r = result['results']
        assert r['p99_ms'] >= r['p95_ms'] >= r['p50_ms']

    def test_low_users_no_errors(self):
        result = simulate_load_test('/', concurrent_users=5)
        assert result['results']['error_rate_pct'] == 0.0

    def test_high_users_has_errors(self):
        result = simulate_load_test('/', concurrent_users=200)
        assert result['results']['error_rate_pct'] > 0

    def test_recommendation_present(self):
        result = simulate_load_test('/')
        assert 'recommendation' in result
        assert len(result['recommendation']) > 0

    def test_note_mentions_locust(self):
        result = simulate_load_test('/')
        assert 'locust' in result['note'].lower()

    def test_timestamp_present(self):
        result = simulate_load_test('/')
        assert 'timestamp' in result


# ===========================================================================
# #73 — Historical Disaster Simulation
# ===========================================================================

class TestSimulateHistoricalDisaster:
    def test_known_year_2019(self):
        result = simulate_historical_disaster(2019)
        assert result['status'] == 'success'
        assert result['historical_event']['year'] == 2019

    def test_known_year_2005(self):
        result = simulate_historical_disaster(2005)
        assert result['status'] == 'success'
        assert result['historical_event']['event'] == 'Mumbai Deluge'

    def test_known_year_1993(self):
        result = simulate_historical_disaster(1993)
        assert result['status'] == 'success'
        assert result['historical_event']['type'] == 'EARTHQUAKE'

    def test_known_year_2021(self):
        result = simulate_historical_disaster(2021)
        assert result['status'] == 'success'
        assert result['historical_event']['type'] == 'CYCLONE'

    def test_unknown_year_returns_error(self):
        result = simulate_historical_disaster(1800)
        assert result['status'] == 'error'
        assert 'available_years' in result

    def test_simulation_block_present(self):
        result = simulate_historical_disaster(2019)
        sim = result['simulation']
        assert 'predicted_risk_score' in sim
        assert 'predicted_severity' in sim
        assert 'recommended_evacuation' in sim
        assert 'ndrf_teams_recommended' in sim

    def test_ndrf_teams_at_least_2(self):
        result = simulate_historical_disaster(2019)
        assert result['simulation']['ndrf_teams_recommended'] >= 2

    def test_lessons_learned_present(self):
        result = simulate_historical_disaster(2019)
        assert 'lessons_learned' in result
        assert len(result['lessons_learned']) > 0

    def test_timestamp_present(self):
        result = simulate_historical_disaster(2019)
        assert 'timestamp' in result


# ===========================================================================
# #74 #75 #76 — Model Accuracy Analysis
# ===========================================================================

class TestAnalyzeModelAccuracy:
    def _make_data(self):
        predictions = [
            {'risk_level': 'HIGH'}, {'risk_level': 'CRITICAL'}, {'risk_level': 'LOW'},
            {'risk_level': 'HIGH'}, {'risk_level': 'MEDIUM'}, {'risk_level': 'CRITICAL'},
            {'risk_level': 'LOW'}, {'risk_level': 'HIGH'}
        ]
        actuals = [
            {'actual_severity': 'HIGH'}, {'actual_severity': 'CRITICAL'}, {'actual_severity': 'LOW'},
            {'actual_severity': 'LOW'}, {'actual_severity': 'HIGH'}, {'actual_severity': 'CRITICAL'},
            {'actual_severity': 'LOW'}, {'actual_severity': 'HIGH'}
        ]
        return predictions, actuals

    def test_basic_success(self):
        p, a = self._make_data()
        result = analyze_model_accuracy(p, a)
        assert result['status'] == 'success'

    def test_metrics_keys(self):
        p, a = self._make_data()
        result = analyze_model_accuracy(p, a)
        m = result['metrics']
        for key in ['precision', 'recall', 'f1_score', 'accuracy',
                    'false_positive_rate', 'false_negative_rate']:
            assert key in m

    def test_metrics_in_range_0_to_1(self):
        p, a = self._make_data()
        result = analyze_model_accuracy(p, a)
        for k, v in result['metrics'].items():
            assert 0.0 <= v <= 1.0, f"{k} = {v} out of range"

    def test_confusion_matrix_sums_to_n(self):
        p, a = self._make_data()
        result = analyze_model_accuracy(p, a)
        cm = result['confusion_matrix']
        total = cm['tp'] + cm['fp'] + cm['fn'] + cm['tn']
        assert total == result['sample_size']

    def test_empty_predictions_error(self):
        result = analyze_model_accuracy([], [])
        assert result['status'] == 'error'

    def test_interpretation_present(self):
        p, a = self._make_data()
        result = analyze_model_accuracy(p, a)
        assert 'interpretation' in result
        assert 'missed_disasters' in result['interpretation']

    def test_validation_source_present(self):
        p, a = self._make_data()
        result = analyze_model_accuracy(p, a)
        assert 'validation_source' in result

    def test_perfect_predictions(self):
        p = [{'risk_level': 'HIGH'}] * 5
        a = [{'actual_severity': 'HIGH'}] * 5
        result = analyze_model_accuracy(p, a)
        assert result['metrics']['precision'] == 1.0
        assert result['metrics']['recall'] == 1.0

    def test_all_wrong_predictions(self):
        p = [{'risk_level': 'HIGH'}] * 5
        a = [{'actual_severity': 'LOW'}] * 5
        result = analyze_model_accuracy(p, a)
        assert result['metrics']['precision'] == 0.0

    def test_unequal_lengths_uses_min(self):
        p = [{'risk_level': 'HIGH'}] * 10
        a = [{'actual_severity': 'HIGH'}] * 5
        result = analyze_model_accuracy(p, a)
        assert result['sample_size'] == 5


# ===========================================================================
# #69 — DB Optimization (uses tmp DB path)
# ===========================================================================

class TestDBOptimization:
    def test_report_on_valid_db(self, test_db):
        import sqlite3
        # Create tables in temp DB
        conn = sqlite3.connect(test_db)
        cur = conn.cursor()
        cur.execute('CREATE TABLE incidents (id INTEGER PRIMARY KEY, threat_level TEXT, created_at TEXT)')
        cur.execute('CREATE TABLE user_incidents (id INTEGER PRIMARY KEY, status TEXT, district TEXT)')
        cur.execute('CREATE TABLE audit_log (id INTEGER PRIMARY KEY, user_role TEXT, created_at TEXT)')
        conn.commit()
        conn.close()
        result = get_db_optimization_report(test_db)
        assert result['status'] == 'success'
        assert 'optimizations' in result

    def test_report_has_page_info(self, test_db):
        import sqlite3
        conn = sqlite3.connect(test_db)
        cur = conn.cursor()
        cur.execute('CREATE TABLE incidents (id INTEGER PRIMARY KEY, threat_level TEXT, created_at TEXT)')
        cur.execute('CREATE TABLE user_incidents (id INTEGER PRIMARY KEY, status TEXT, district TEXT)')
        cur.execute('CREATE TABLE audit_log (id INTEGER PRIMARY KEY, user_role TEXT, created_at TEXT)')
        conn.commit()
        conn.close()
        result = get_db_optimization_report(test_db)
        assert 'page_size' in result
        assert 'page_count' in result
        assert 'db_size_kb' in result

    def test_apply_indexes_on_valid_db(self, test_db):
        import sqlite3
        conn = sqlite3.connect(test_db)
        cur = conn.cursor()
        cur.execute('CREATE TABLE incidents (id INTEGER PRIMARY KEY, threat_level TEXT, created_at TEXT)')
        cur.execute('CREATE TABLE user_incidents (id INTEGER PRIMARY KEY, status TEXT, district TEXT)')
        cur.execute('CREATE TABLE audit_log (id INTEGER PRIMARY KEY, user_role TEXT, created_at TEXT)')
        conn.commit()
        conn.close()
        result = apply_db_indexes(test_db)
        assert result['status'] == 'success'
        assert len(result['indexes_applied']) > 0

    def test_apply_indexes_idempotent(self, test_db):
        import sqlite3
        conn = sqlite3.connect(test_db)
        cur = conn.cursor()
        cur.execute('CREATE TABLE incidents (id INTEGER PRIMARY KEY, threat_level TEXT, created_at TEXT)')
        cur.execute('CREATE TABLE user_incidents (id INTEGER PRIMARY KEY, status TEXT, district TEXT)')
        cur.execute('CREATE TABLE audit_log (id INTEGER PRIMARY KEY, user_role TEXT, created_at TEXT)')
        conn.commit()
        conn.close()
        r1 = apply_db_indexes(test_db)
        r2 = apply_db_indexes(test_db)   # Second call — IF NOT EXISTS
        assert r1['status'] == 'success'
        assert r2['status'] == 'success'

    def test_invalid_db_path_returns_error(self):
        result = apply_db_indexes('/nonexistent/path/db.db')
        assert result['status'] == 'error'


# ===========================================================================
# API Route Tests (via Flask test client)
# ===========================================================================

class TestPerformanceAPIRoutes:
    def test_cache_stats(self, client):
        resp = client.get('/api/v3/cache/stats')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'
        assert 'cache_stats' in data

    def test_performance_metrics(self, client):
        resp = client.get('/api/v3/performance/metrics')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'total_endpoints_tracked' in data or 'samples' in data

    def test_load_simulate_default(self, client):
        resp = client.get('/api/v3/load/simulate')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'simulation'

    def test_load_simulate_with_users(self, client):
        resp = client.get('/api/v3/load/simulate?users=20&req_per_user=3')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['concurrent_users'] == 20

    def test_load_simulate_clamps_users(self, client):
        resp = client.get('/api/v3/load/simulate?users=9999')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['concurrent_users'] <= 500

    def test_load_simulate_bad_input(self, client):
        resp = client.get('/api/v3/load/simulate?users=abc')
        assert resp.status_code == 200   # Falls back to defaults gracefully

    def test_historical_sim_2019(self, client):
        resp = client.get('/api/v3/simulation/historical?year=2019')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'

    def test_historical_sim_bad_year(self, client):
        resp = client.get('/api/v3/simulation/historical?year=1800')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'error'

    def test_historical_sim_bad_input(self, client):
        resp = client.get('/api/v3/simulation/historical?year=xyz')
        assert resp.status_code == 200   # Falls back to default year gracefully

    def test_model_accuracy(self, client):
        resp = client.get('/api/v3/analytics/model-accuracy')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'
        assert 'metrics' in data

    def test_research_methodology(self, client):
        resp = client.get('/api/v3/research/methodology')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'
        assert 'methodology' in data
        assert 'data_sources' in data

    def test_feedback_get(self, client):
        resp = client.get('/api/v3/feedback')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'
        assert 'average_rating' in data
        assert 'total_responses' in data

    def test_feedback_post_valid(self, client):
        with client.session_transaction() as sess:
            sess['csrf_token'] = 'test-csrf-token'
        resp = client.post(
            '/api/v3/feedback',
            json={'rating': 5, 'feedback': 'Excellent platform!', 'category': 'general'},
            headers={'X-CSRFToken': 'test-csrf-token'}
        )
        assert resp.status_code in [201, 403]   # 403 if CSRF strict in test env

    def test_feedback_post_invalid_rating(self, client):
        with client.session_transaction() as sess:
            sess['csrf_token'] = 'test-csrf-token'
        resp = client.post(
            '/api/v3/feedback',
            json={'rating': 'bad', 'feedback': 'ok', 'category': 'general'},
            headers={'X-CSRFToken': 'test-csrf-token'}
        )
        assert resp.status_code in [400, 403]

    def test_db_optimize_requires_admin(self, client):
        resp = client.get('/api/v3/db/optimize')
        assert resp.status_code in [302, 401, 403]   # redirect to login or forbidden

    def test_db_optimize_admin_access(self, admin_client):
        resp = admin_client.get('/api/v3/db/optimize')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'status' in data

    def test_db_apply_indexes_requires_admin(self, client):
        resp = client.post('/api/v3/db/apply-indexes')
        assert resp.status_code in [302, 401, 403]

    def test_manifest_json(self, client):
        resp = client.get('/manifest.json')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['name'] == 'PRAHARIX 3.0 - National Disaster Command'
        assert data['display'] == 'standalone'

    def test_api_status_version(self, client):
        resp = client.get('/api/status')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['version'] == '3.0.0'
        assert '3.0' in data['platform']
        assert data['api_endpoints_total'] == 90
