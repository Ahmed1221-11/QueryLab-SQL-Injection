"""A loopback-only educational SQL injection lab. Python standard library only."""
import json
import sqlite3
import webbrowser
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST, PORT = '127.0.0.1', 8765
BASE = Path(__file__).resolve().parent


def make_database():
    # Recreated in memory per attempt: no real accounts or persistent changes.
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)')
    db.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', [
        (1, 'admin', 'AdminDemo42!', 'Administrator'),
        (2, 'student', 'StudyDemo42!', 'Student'),
    ])
    return db


def login(mode, username, password):
    if mode not in ('vulnerable', 'fixed'):
        raise ValueError('Unknown mode')
    db = make_database()
    try:
        if mode == 'vulnerable':
            # INTENTIONAL vulnerability: input becomes part of SQL syntax.
            query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
            parameters = None
            row = db.execute(query).fetchone()
        else:
            # Placeholders keep SQL structure separate from input values.
            query = 'SELECT id, username, role FROM users WHERE username = ? AND password = ?'
            parameters = [username, password]
            row = db.execute(query, parameters).fetchone()
        return {'accepted': row is not None, 'user': {'name': row[1], 'role': row[2]} if row else None,
                'query': query, 'parameters': parameters, 'error': None}
    except sqlite3.Error as error:
        return {'accepted': False, 'user': None, 'query': query, 'parameters': None,
                'error': str(error)}
    finally:
        db.close()


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.reply(404, b'Not found', 'text/plain')
            return
        self.reply(200, (BASE / 'index.html').read_bytes(), 'text/html; charset=utf-8')

    def do_POST(self):
        if self.path != '/api/login':
            self.reply(404, b'Not found', 'text/plain')
            return
        # Only the local page may send browser API requests.
        if self.headers.get('Origin') not in (None, f'http://{HOST}:{PORT}'):
            self.reply(403, b'Origin rejected', 'text/plain')
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 8192:
                raise ValueError('Request size invalid')
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError('Expected a JSON object')
            mode, username, password = [payload.get(k) for k in ('mode', 'username', 'password')]
            if not all(isinstance(v, str) and len(v) <= 500 for v in (mode, username, password)):
                raise ValueError('Expected text fields of at most 500 characters')
            result = login(mode, username, password)
        except (ValueError, TypeError, json.JSONDecodeError):
            self.reply(400, b'Invalid request', 'text/plain')
            return
        self.reply(200, json.dumps(result).encode('utf-8'), 'application/json; charset=utf-8')


def main():
    try:
        server = HTTPServer((HOST, PORT), Handler)
    except OSError:
        print(f'Cannot open port {PORT}. Close another running copy and try again.')
        return
    url = f'http://{HOST}:{PORT}'
    print(f'SQL Injection Lab running at {url}\nKeep this window open. Press Ctrl+C to stop.')
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nLab stopped.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
