from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def setup_function(): client.post('/lab/reset')
def test_system_baseline():
    r=client.get('/api/system'); assert r.status_code==200; assert r.json()['power_state']=='On'
def test_force_off_baseline():
    r=client.post('/api/reset',json={'reset_type':'ForceOff'}); assert r.status_code==200; assert r.json()['power_state']=='Off'
