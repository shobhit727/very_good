# Anonymous Q&A backend

This is a simple Flask + SQLite backend for consented analytics.

## Setup

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Linux/macOS

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The API is available at:

http://127.0.0.1:5000

Visitor records can be viewed at:

http://127.0.0.1:5000/api/visitors

The database is automatically created as `visitors.db`.

## What is collected

Only information explicitly sent by the consented frontend:

- Timestamp
- Browser user-agent
- Browser language
- Browser platform
- Screen width/height
- Browser timezone
- Referrer

This implementation deliberately does not collect passwords, files, camera/microphone
data, keystrokes, clipboard contents, precise location, or hidden browser fingerprinting
data.
