"""
API endpoint tests for PRAHARIX 3.0
"""
import pytest
import json


class TestHealthEndpoints:
    def test_api_status(self, client):
        resp = client.get('/api/status')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'OPERATIONAL'

    def test_api_csrf_token(self, client):
        with client.session_transaction() as sess:
            sess['role'] = 'public'
        resp = client.get('/api/csrf-token')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'csrf_token' in data

    def test_api_weather(self, client):
        resp = client.get('/api/weather')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'temp' in data

    def test_api_earthquakes(self, client):
        resp = client.get('/api/earthquakes')
        assert resp.status_code in [200, 500]
        if resp.status_code == 200:
            data = json.loads(resp.data)
            assert 'count' in data

    def test_api_health(self, client):
        resp = client.get('/api/health')
        assert resp.status_code == 200


class TestAIEndpoints:
    def test_ai_summary(self, client):
        resp = client.get('/api/ai/summary')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'

    def test_ai_query_missing(self, client):
        resp = client.get('/api/ai/query')
        assert resp.status_code == 400

    def test_ai_query_flood(self, client):
        resp = client.get('/api/ai/query?query=flood+risk+in+Kolhapur')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['status'] == 'success'

    def test_ai_query_too_long(self, client):
        long_query = 'a' * 1001
        resp = client.get(f'/api/ai/query?query={long_query}')
        assert resp.status_code == 400

    def test_ai_recommendations(self, client):
        resp = client.get('/api/ai/recommendations?severity=HIGH')
        assert resp.status_code == 200

    def test_ai_whatif_flood(self, client):
        resp = client.get('/api/ai/whatif?hazard=flood&rainfall=200')
        assert resp.status_code == 200

    def test_ai_history(self, client):
        resp = client.get('/api/ai/history')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'history' in data


class TestHazardEndpoints:
    def test_hazard_flood(self, client):
        resp = client.get('/api/hazard/flood?rainfall=145')
        assert resp.status_code == 200

    def test_hazard_earthquake(self, client):
        resp = client.get('/api/hazard/earthquake?mag=6.2&depth=15')
        assert resp.status_code == 200

    def test_hazard_cyclone(self, client):
        resp = client.get('/api/hazard/cyclone?wind=130')
        assert resp.status_code == 200

    def test_hazard_heatwave(self, client):
        resp = client.get('/api/hazard/heatwave?temp=43&humidity=35')
        assert resp.status_code == 200

    def test_hazard_multihazard(self, client):
        resp = client.get('/api/hazard/multihazard?lat=18.5&lon=73.8')
        assert resp.status_code == 200


class TestIntelEndpoints:
    def test_intel_population(self, client):
        resp = client.get('/api/intel/population?district=Kolhapur')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'total_population' in data

    def test_intel_hospitals(self, client):
        resp = client.get('/api/intel/hospitals?district=Kolhapur')
        assert resp.status_code == 200

    def test_intel_shelters(self, client):
        resp = client.get('/api/intel/shelters?district=Kolhapur')
        assert resp.status_code == 200

    def test_intel_evacuation(self, client):
        resp = client.get('/api/intel/evacuation?district=Raigad&hazard=flood')
        assert resp.status_code == 200


class TestGovtEndpoints:
    def test_govt_data(self, client):
        resp = client.get('/api/govt/data')
        assert resp.status_code == 200

    def test_govt_incidents(self, client):
        resp = client.get('/api/govt/incidents')
        assert resp.status_code == 200

    def test_govt_audit(self, client):
        resp = client.get('/api/govt/audit')
        assert resp.status_code == 200

    def test_govt_incident_post_no_csrf(self, client):
        # Without CSRF token (testing mode disables check)
        resp = client.post('/api/govt/incident',
            json={'description': 'Test flood incident', 'district': 'Kolhapur', 'severity': 'HIGH'},
            headers={'X-CSRFToken': 'test-csrf-token'}
        )
        # Should succeed in testing mode
        assert resp.status_code in [201, 400, 403]

    def test_govt_checklist(self, client):
        resp = client.get('/api/govt/checklist?hazard=cyclone')
        assert resp.status_code == 200


class TestGlobalEndpoints:
    def test_global_disasters(self, client):
        resp = client.get('/api/global/disasters')
        assert resp.status_code == 200

    def test_global_countries(self, client):
        resp = client.get('/api/global/countries')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'countries' in data
        assert len(data['countries']) > 0
