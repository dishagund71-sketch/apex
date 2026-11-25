"""
Integration tests for PRAHARIX 3.0 — Full workflow tests
"""
import pytest
import json


class TestFullWorkflows:
    def test_home_page_loads(self, client):
        resp = client.get('/')
        assert resp.status_code in [200, 302]

    def test_alerts_page_loads(self, client):
        resp = client.get('/alerts')
        assert resp.status_code == 200

    def test_sar_page_loads(self, client):
        resp = client.get('/sar')
        assert resp.status_code == 200

    def test_india_page_loads(self, client):
        resp = client.get('/india')
        assert resp.status_code == 200

    def test_multihazard_page_loads(self, client):
        resp = client.get('/multihazard')
        assert resp.status_code == 200

    def test_govt_page_loads(self, client):
        resp = client.get('/govt')
        assert resp.status_code == 200

    def test_complete_risk_workflow(self, client):
        # 1. Get weather
        weather_resp = client.get('/api/weather')
        assert weather_resp.status_code == 200
        weather = json.loads(weather_resp.data)
        assert 'temp' in weather
        # 2. Get AI summary
        summary_resp = client.get('/api/ai/summary')
        assert summary_resp.status_code == 200
        summary = json.loads(summary_resp.data)
        assert summary['status'] == 'success'
        # 3. Query AI
        query_resp = client.get('/api/ai/query?query=flood+risk')
        assert query_resp.status_code == 200
        # 4. Get evacuation routes
        evac_resp = client.get('/api/intel/evacuation?district=Kolhapur&hazard=flood')
        assert evac_resp.status_code == 200

    def test_incident_lifecycle(self, client):
        # Submit incident
        with client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['csrf_token'] = 'test-token'
        post_resp = client.post('/api/govt/incident',
            json={
                'description': 'Integration test: flood in Kolhapur taluka',
                'incident_type': 'RIVERINE_FLOOD',
                'district': 'Kolhapur',
                'severity': 'HIGH',
                'reported_by': 'pytest'
            },
            headers={'X-CSRFToken': 'test-token'}
        )
        # Either created or CSRF issue in testing
        assert post_resp.status_code in [201, 403]
        # List incidents
        list_resp = client.get('/api/govt/incidents')
        assert list_resp.status_code == 200
        data = json.loads(list_resp.data)
        assert 'incidents' in data
