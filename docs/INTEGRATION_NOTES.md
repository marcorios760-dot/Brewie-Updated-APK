# Integration notes

The original APK was a Qt 5.x Android app for same-network Brewie B20/B20+ remote control. The modern replacement here does not depend on Android, Qt, APK signing, or Play services. It runs on Raspberry Pi and exposes only a local web UI.

## Mapping original app concepts

| Original app concept | ReBrewie Control Pi implementation |
|---|---|
| Same Wi-Fi discovery/use | Browser opens Pi IP on same LAN |
| Remote start/pause | `/api/command` start/pause/resume/stop |
| Live monitoring | `/api/status` polling and `/ws/status` |
| Recipe editor | JSON recipe editor/storage under `recipes/` |
| Android/Qt GUI | Static HTML/CSS/JS with Brewie-style dark/orange controls |

## Firmware command adaptation

Edit `app/config.py` `COMMANDS` to match your ReBrewie firmware. Keep the API command names stable so the UI does not need to change.

## Recommended first test

1. Keep `BREWIE_TRANSPORT=mock` and verify the UI.
2. Change to `tcp`, `http`, or `serial`.
3. Test `status` only.
4. Test non-heating controls.
5. Test start/pause with water only and physical supervision.
