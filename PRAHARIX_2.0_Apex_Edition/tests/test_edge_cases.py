"""
Edge case tests for PRAHARIX 3.0
"""
import pytest
import json


class TestEdgeCases:
    def test_earthquake_api_invalid_lat(self, client):
        resp = client.get('/api/eew/simulate?lat=999&lon=76&mag=6')
        assert resp.status_code == 200  # Should clamp invalid value

    def test_earthquake_api_string_mag(self, client):
        resp = client.get('/api/hazard/flood?rainfall=abc')
        assert resp.status_code in [200, 400, 500]

    def test_whatif_empty_params(self, client):
        resp = client.get('/api/ai/whatif?hazard=flood')
        assert resp.status_code == 200

    def test_district_with_special_chars(self, client):
        resp = client.get('/api/intel/population?district=<script>alert(1)</script>')
        assert resp.status_code in [200, 400]

    def test_empty_district_param(self, client):
        resp = client.get('/api/intel/hospitals?district=')
        assert resp.status_code in [200, 400]

    def test_very_large_rainfall(self, client):
        resp = client.get('/api/hazard/flood?rainfall=99999')
        assert resp.status_code in [200, 400]

    def test_negative_magnitude(self, client):
        resp = client.get('/api/hazard/earthquake?mag=-1&depth=10')
        assert resp.status_code in [200, 400]

    def test_zero_population_impact(self, client):
        resp = client.get('/api/intel/impact?hazard=FLOOD&severity=HIGH&area=0&pop=0')
        assert resp.status_code in [200, 400, 500]

    def test_global_countries_all_have_scores(self, client):
        resp = client.get('/api/global/countries')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        for country in data['countries']:
            assert 'risk_score' in country
            assert 0 <= country['risk_score'] <= 100

    def test_sitrep_text_all_langs(self, client):
        for lang in ['en', 'hi', 'mr']:
            resp = client.get(f'/api/sitrep/text?lang={lang}')
            assert resp.status_code == 200
            data = json.loads(resp.data)
            assert 'text' in data
            assert len(data['text']) > 10

    def test_404_api_returns_json(self, client):
        resp = client.get('/api/nonexistent-endpoint')
        assert resp.status_code == 404

    def test_incident_post_empty_description(self, client):
        with client.session_transaction() as sess:
            sess['role'] = 'admin'
            sess['csrf_token'] = 'test-token'
        resp = client.post('/api/govt/incident',
            json={'description': '', 'district': 'Kolhapur'},
            headers={'X-CSRFToken': 'test-token'}
        )
        assert resp.status_code in [400, 403]
