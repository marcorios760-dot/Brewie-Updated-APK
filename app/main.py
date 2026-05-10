import json, os, re
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import settings
from .models import Recipe, CommandRequest
from .transport import get_transport

app = FastAPI(title='ReBrewie Control Pi', version='0.1.0')
app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')
transport = get_transport()
Path(settings.recipe_dir).mkdir(exist_ok=True)

def safe_name(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_.-]+', '_', name).strip('_') or 'recipe'

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/api/status')
async def api_status():
    return (await transport.status()).model_dump()

@app.post('/api/command')
async def api_command(req: CommandRequest):
    allowed = {'status','start','pause','resume','stop','heat_on','heat_off','pump_mash_on','pump_mash_off','pump_sparge_on','pump_sparge_off','valves_close','firmware'}
    if req.command not in allowed:
        raise HTTPException(400, 'Unknown or disabled command')
    return await transport.send(req.command, req.payload)

@app.get('/api/recipes')
async def list_recipes():
    out = []
    for p in sorted(Path(settings.recipe_dir).glob('*.json')):
        try:
            data = json.loads(p.read_text())
            out.append({'id': p.stem, 'name': data.get('name', p.stem), 'batch_l': data.get('batch_l'), 'steps': len(data.get('steps', []))})
        except Exception:
            pass
    return out

@app.get('/api/recipes/{recipe_id}')
async def get_recipe(recipe_id: str):
    p = Path(settings.recipe_dir) / f'{safe_name(recipe_id)}.json'
    if not p.exists(): raise HTTPException(404, 'Recipe not found')
    return json.loads(p.read_text())

@app.post('/api/recipes')
async def save_recipe(recipe: Recipe):
    p = Path(settings.recipe_dir) / f'{safe_name(recipe.name)}.json'
    p.write_text(recipe.model_dump_json(indent=2))
    return {'ok': True, 'id': p.stem}

@app.post('/api/recipes/{recipe_id}/send')
async def send_recipe(recipe_id: str):
    recipe = await get_recipe(recipe_id)
    return await transport.send('recipe', recipe)

@app.websocket('/ws/status')
async def ws_status(ws: WebSocket):
    await ws.accept()
    import asyncio
    while True:
        await ws.send_json((await transport.status()).model_dump())
        await asyncio.sleep(2)
