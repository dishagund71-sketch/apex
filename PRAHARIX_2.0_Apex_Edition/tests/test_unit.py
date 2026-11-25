"""
Unit tests for PRAHARIX 3.0 — Core utility functions
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestCalculateThreat:
    def test_critical_threat(self, app):
        with app.app_context():
            import app as application
            risk, level, score = application.calculate_threat(7.5)
            assert level == 'CRITICAL'
            assert score == 100

    def test_high_threat(self, app):
        with app.app_context():
            import app as application
            risk, level, score = application.calculate_threat(6.2)
            assert level == 'HIGH'
            assert score == 80

    def test_medium_threat(self, app):
        with app.app_context():
            import app as application
            risk, level, score = application.calculate_threat(4.5)
            assert level == 'MEDIUM'
            assert score == 50

    def test_low_threat(self, app):
        with app.app_context():
            import app as application
            risk, level, score = application.calculate_threat(2.0)
            assert level == 'LOW'
            assert score == 20

    def test_invalid_magnitude(self, app):
        with app.app_context():
            import app as application
            risk, level, score = application.calculate_threat('invalid')
            assert level == 'LOW'

    def test_zero_magnitude(self, app):
        with app.app_context():
            import app as application
            risk, level, score = application.calculate_threat(0)
            assert level == 'LOW'


class TestPredictThreat:
    def test_empty_earthquakes(self, app):
        with app.app_context():
            import app as application
            result = application.predict_threat([])
            assert result['prediction'] == 'LOW'

    def test_critical_prediction(self, app):
        with app.app_context():
            import app as application
            eqs = [{'mag': 7.0, 'threat_level': 'CRITICAL', 'threat_score': 100}]
            result = application.predict_threat(eqs)
            assert result['prediction'] == 'CRITICAL'

    def test_none_magnitude_handled(self, app):
        with app.app_context():
            import app as application
            eqs = [{'mag': None, 'threat_level': 'LOW'}]
            result = application.predict_threat(eqs)
            assert 'prediction' in result


class TestAiSummary:
    def test_returns_dict(self, app):
        with app.app_context():
            import app as application
            result = application.ai_generate_summary([], {}, [])
            assert isinstance(result, dict)
            assert result['status'] == 'success'
            assert 'summary' in result

    def test_trilingual_summary(self, app):
        with app.app_context():
            import app as application
            result = application.ai_generate_summary([], {}, [])
            assert 'en' in result['summary']
            assert 'hi' in result['summary']
            assert 'mr' in result['summary']

    def test_critical_alert_code(self, app):
        with app.app_context():
            import app as application
            critical_eq = [{'threat_level': 'CRITICAL', 'mag': 7.5}]
            result = application.ai_generate_summary(critical_eq, {}, [])
            assert result['alert_code'] == 'RED'


class TestWhatIfSimulation:
    def test_flood_simulation(self, app):
        with app.app_context():
            import app as application
            result = application.ai_whatif_simulation('flood', {'rainfall': 200})
            assert result['status'] == 'success'
            assert 'primary_impact' in result

    def test_earthquake_simulation(self, app):
        with app.app_context():
            import app as application
            result = application.ai_whatif_simulation('earthquake', {'mag': 6.5, 'depth': 10})
            assert result['status'] == 'success'

    def test_cyclone_simulation(self, app):
        with app.app_context():
            import app as application
            result = application.ai_whatif_simulation('cyclone', {'wind': 150})
            assert result['status'] == 'success'

    def test_default_simulation(self, app):
        with app.app_context():
            import app as application
            result = application.ai_whatif_simulation('unknown_type', {})
            assert 'primary_impact' in result


class TestDegreesToCardinal:
    def test_north(self, app):
        with app.app_context():
            import app as application
            assert application.degrees_to_cardinal(0) == 'N'

    def test_east(self, app):
        with app.app_context():
            import app as application
            assert application.degrees_to_cardinal(90) == 'E'

    def test_south(self, app):
        with app.app_context():
            import app as application
            assert application.degrees_to_cardinal(180) == 'S'
