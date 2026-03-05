import json
import os
import sqlite3
from datetime import datetime

DB_PATH = '/tmp/devflow_tasks.db'


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def handler(request):
    method = request.get('method', 'GET') if isinstance(request, dict) else getattr(request, 'method', 'GET')

    if method == 'GET':
        conn = _conn()
        rows = conn.execute('SELECT id, title, created_at FROM tasks ORDER BY id DESC').fetchall()
        conn.close()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json; charset=utf-8'},
            'body': json.dumps({'tasks': [dict(r) for r in rows]}, ensure_ascii=False),
        }

    if method == 'POST':
        body = request.get('body', '{}') if isinstance(request, dict) else '{}'
        if isinstance(body, (bytes, bytearray)):
            body = body.decode('utf-8', 'ignore')
        data = json.loads(body or '{}')
        title = (data.get('title') or '').strip()
        if not title:
            return {'statusCode': 400, 'body': json.dumps({'error': 'title required'})}

        conn = _conn()
        now = datetime.utcnow().isoformat() + 'Z'
        cur = conn.execute('INSERT INTO tasks(title, created_at) VALUES (?, ?)', (title, now))
        conn.commit()
        task_id = cur.lastrowid
        conn.close()

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json; charset=utf-8'},
            'body': json.dumps({'ok': True, 'id': task_id}, ensure_ascii=False),
        }

    return {'statusCode': 405, 'body': json.dumps({'error': 'method not allowed'})}
