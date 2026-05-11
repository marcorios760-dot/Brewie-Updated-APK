import asyncio, json, socket, time
from abc import ABC, abstractmethod
from datetime import datetime
import httpx
import serial
from .config import settings, COMMANDS
from .models import BrewStatus

class BrewieTransport(ABC):
    @abstractmethod
    async def send(self, command: str, payload=None): ...
    @abstractmethod
    async def status(self) -> BrewStatus: ...

class MockTransport(BrewieTransport):
    def __init__(self):
        self.started = time.time()
        self.mode = 'idle'
        self.paused = False
    async def send(self, command: str, payload=None):
        if command == 'start': self.mode = 'brewing'; self.paused = False; self.started = time.time()
        if command == 'pause': self.paused = True; self.mode = 'paused'
        if command == 'resume': self.paused = False; self.mode = 'brewing'
        if command == 'stop': self.mode = 'idle'
        return {'ok': True, 'command': command, 'payload': payload or {}}
    async def status(self):
        elapsed = int((time.time() - self.started) / 60) if self.mode in ('brewing','paused') else 0
        progress = min(100, elapsed * 2) if self.mode in ('brewing','paused') else 0
        temp = 20 + min(48, progress * 0.55) if self.mode in ('brewing','paused') else 20
        return BrewStatus(
            connected=True, mode=self.mode, phase='Mash schedule' if self.mode != 'idle' else 'Ready',
            progress=progress, temperature_c=round(temp, 1), target_c=68 if self.mode != 'idle' else 0,
            elapsed_min=elapsed, remaining_min=max(0, 120 - elapsed), heaters=self.mode == 'brewing',
            pumps={'mash': self.mode == 'brewing', 'sparge': False}, firmware='mock-rebrewie-0.1',
            last_update=datetime.utcnow().isoformat() + 'Z'
        )

class TCPTransport(BrewieTransport):
    async def send(self, command: str, payload=None):
        wire = COMMANDS.get(command, command)
        if payload: wire += ' ' + json.dumps(payload)
        def call():
            with socket.create_connection((settings.brewie_host, settings.brewie_port), timeout=5) as s:
                s.sendall((wire + '\n').encode())
                return s.recv(8192).decode(errors='replace').strip()
        return {'ok': True, 'response': await asyncio.to_thread(call)}
    async def status(self):
        reply = await self.send('status')
        return parse_status(reply.get('response',''), True)

class HTTPTransport(BrewieTransport):
    async def send(self, command: str, payload=None):
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.post(f'{settings.brewie_http_base.rstrip("/")}/command', json={'command': command, 'payload': payload or {}})
            r.raise_for_status()
            return r.json()
    async def status(self):
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(f'{settings.brewie_http_base.rstrip("/")}/status')
            r.raise_for_status()
            return parse_status(r.json(), True)

class SerialTransport(BrewieTransport):
    async def send(self, command: str, payload=None):
        wire = COMMANDS.get(command, command)
        if payload: wire += ' ' + json.dumps(payload)
        def call():
            with serial.Serial(settings.brewie_serial_port, settings.brewie_serial_baud, timeout=5) as ser:
                ser.write((wire + '\n').encode())
                return ser.readline().decode(errors='replace').strip()
        return {'ok': True, 'response': await asyncio.to_thread(call)}
    async def status(self):
        reply = await self.send('status')
        return parse_status(reply.get('response',''), True)

def parse_status(data, connected=False) -> BrewStatus:
    try:
        obj = json.loads(data) if isinstance(data, str) else data
        return BrewStatus(connected=connected, raw=obj, **{k:v for k,v in obj.items() if k in BrewStatus.model_fields})
    except Exception:
        return BrewStatus(connected=connected, phase='Raw status', raw={'response': str(data)})

def get_transport() -> BrewieTransport:
    t = settings.brewie_transport.lower()
    if t == 'tcp': return TCPTransport()
    if t == 'http': return HTTPTransport()
    if t == 'serial': return SerialTransport()
    return MockTransport()
