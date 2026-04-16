import sqlite3
import os

# 根據架構設計取得 instance/database.db 路徑
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 開啟外鍵約束支援
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_script = f.read()
        conn = get_db_connection()
        conn.executescript(schema_script)
        conn.commit()
        conn.close()
