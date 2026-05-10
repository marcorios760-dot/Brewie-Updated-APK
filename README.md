# ReBrewie Control Pi

A Raspberry Pi 4B local-only web controller for Brewie+/ReBrewie machines.

This project is a clean-room, Pi-native replacement for the old Brewie Control Android APK. It keeps the original app concepts: connect on the same Wi-Fi/LAN, monitor brew state, start/pause/resume/stop, manage recipes, and view progress. It adds ReBrewie-oriented extension hooks for newer firmware commands without exposing the controller to the public internet.

## What this ZIP includes

- FastAPI backend for local browser access
- Responsive dashboard styled after the original Android remote-control concept
- Recipe editor and JSON recipe storage
- Live status polling and optional WebSocket stream
- Pluggable TCP, HTTP, USB serial, and mock transports
- Raspberry Pi installer script
- systemd service file
- Config file for your Brewie/ReBrewie host/port/serial settings

## Quick install on Raspberry Pi OS

```bash
unzip rebrewie-control-pi.zip
cd rebrewie-control-pi
chmod +x install.sh
./install.sh
```

Then open:

```text
http://<raspberry-pi-ip>:8080
```

The app binds to `0.0.0.0` by default so other devices on the same LAN can use it. Do not port-forward this service.

## Configure machine connection

Edit `.env` after install:

```env
BREWIE_TRANSPORT=mock
BREWIE_HOST=192.168.1.50
BREWIE_PORT=8332
BREWIE_SERIAL_PORT=/dev/ttyUSB0
BREWIE_SERIAL_BAUD=115200
LOCAL_BIND=0.0.0.0
LOCAL_PORT=8080
```

Transport options:

- `mock`: safe demo mode; no hardware required
- `tcp`: raw line-oriented TCP command transport
- `http`: HTTP/JSON bridge transport
- `serial`: USB serial line-oriented command transport

Because community ReBrewie installations may differ, exact command strings are configured in `app/config.py` and sent through the selected transport. Update the command map there if your firmware uses different names.

## Safety note

This software is for same-LAN/local use with a machine you own. Brewing hardware includes heaters, pumps, valves, and moving liquid. Keep physical supervision for cleaning, heating, unclogging, and transfer steps.
