"""
PRAHARIX 3.0 - Load Testing with Locust
Item #72: Multiple-user load testing

Usage:
    pip install locust
    locust -f locustfile.py --host=http://localhost:5000
    # Then open http://localhost:8089 for the Locust web UI
"""
from locust import HttpUser, task, between


class PraharixUser(HttpUser):
    """Simulates a standard PRAHARIX dashboard user."""
    wait_time = between(1, 3)

    @task(3)
    def home_page(self):
        self.client.get('/')

    @task(5)
    def api_weather(self):
        self.client.get('/api/weather')

    @task(5)
    def api_earthquakes(self):
        self.client.get('/api/earthquakes')

    @task(4)
    def api_ai_summary(self):
        self.client.get('/api/ai/summary')

    @task(3)
    def api_ai_query(self):
        self.client.get('/api/ai/query?query=flood+risk+in+Kolhapur')

    @task(2)
    def api_v3_heatmap(self):
        self.client.get('/api/v3/risk/heatmap')

    @task(2)
    def api_v3_evacuation(self):
        self.client.get('/api/v3/evacuation/routes?district=Kolhapur')

    @task(2)
    def api_govt_incidents(self):
        self.client.get('/api/govt/incidents')

    @task(1)
    def api_global_countries(self):
        self.client.get('/api/global/countries')

    @task(1)
    def alerts_page(self):
        self.client.get('/alerts')


class PraharixOfficerUser(HttpUser):
    """Simulates a district officer user (admin role required)."""
    wait_time = between(2, 5)

    @task(3)
    def api_govt_data(self):
        self.client.get('/api/govt/data')

    @task(2)
    def api_v3_priorities(self):
        self.client.get('/api/v3/response/priorities')

    @task(2)
    def api_sitrep(self):
        self.client.get('/api/govt/sitrep?district=Kolhapur')

    @task(1)
    def api_v3_risk_explain(self):
        self.client.get('/api/v3/risk/explain?district=Kolhapur')
