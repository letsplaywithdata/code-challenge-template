import pytest
from flask import url_for
from api.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_weather_data(client):
    response = client.get('/api/weather?station_id=STN001&date=2021-01-01&offset=1&limit=10')
    assert response.status_code == 200
    assert response.is_json
    data = response.json
    assert isinstance(data, list)
    assert len(data) <= 10
    for record in data:
        assert 'station_id' in record
        assert 'date' in record
        assert 'min_temp' in record
        assert 'max_temp' in record
        assert 'precipitation' in record

def test_get_weather_stats(client):
    response = client.get('/api/weather/stats?station_id=STN001&year=2021&offset=1&limit=10')
    assert response.status_code == 200
    assert response.is_json
    data = response.json
    assert isinstance(data, list)
    assert len(data) <= 10
    for record in data:
        assert 'station_id' in record
        assert 'year' in record
        assert 'avg_min_temp' in record
        assert 'avg_max_temp' in record
        assert 'avg_precipitation' in record
