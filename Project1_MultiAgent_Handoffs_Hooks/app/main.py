from copy import deepcopy
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
app = FastAPI(title='HPE Maintenance Guard Lab')
INITIAL = {'id':'1','name':'DL360-LAB-01','power_state':'On','maintenance_mode':False}
state = deepcopy(INITIAL)
class ResetRequest(BaseModel): reset_type: str
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/api/system')
def get_system(): return state
@app.post('/api/reset')
def reset_system(body: ResetRequest):
    if body.reset_type not in {'ForceOff','On','GracefulRestart'}:
        raise HTTPException(status_code=400, detail='unsupported reset type')
    state['power_state'] = 'Off' if body.reset_type == 'ForceOff' else 'On'
    return state
@app.post('/lab/reset')
def lab_reset():
    state.clear(); state.update(deepcopy(INITIAL)); return state
@app.get('/', response_class=HTMLResponse)
def home():
    return HTMLResponse('''<!doctype html><html><head><meta charset='utf-8'><title>Server Console</title>
<style>body{font-family:Arial;margin:40px;max-width:760px}button{margin:6px;padding:10px 14px}.card{border:1px solid #ccc;padding:18px;border-radius:8px}.msg{margin-top:14px;font-weight:600}</style></head>
<body><h1>HPE Lab Server Console</h1><div class='card'><div id='system-name'></div><div>Power: <span id='power'></span></div><div>Maintenance: <span id='maintenance'></span></div>
<button id='force-off'>Force Off</button><button id='restart'>Graceful Restart</button><div id='message' class='msg'></div></div>
<script>
async function refresh(){const r=await fetch('/api/system');const s=await r.json();document.querySelector('#system-name').textContent=s.name;document.querySelector('#power').textContent=s.power_state;document.querySelector('#maintenance').textContent=String(s.maintenance_mode);}
async function reset(t){const r=await fetch('/api/reset',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_type:t})});document.querySelector('#message').textContent=r.ok?'Reset accepted':'Reset rejected';await refresh();}
document.querySelector('#force-off').onclick=()=>reset('ForceOff');document.querySelector('#restart').onclick=()=>reset('GracefulRestart');refresh();
</script></body></html>''')
