from .db_manager import get_db_connection

def create(book_id, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO excerpt (book_id, content) VALUES (?, ?)', (book_id, content))
    conn.commit()
    excerpt_id = cursor.lastrowid
    conn.close()
    return excerpt_id

def get_all_by_book_id(book_id):
    conn = get_db_connection()
    excerpts = conn.execute('SELECT * FROM excerpt WHERE book_id = ? ORDER BY created_at DESC', (book_id,)).fetchall()
    conn.close()
    return [dict(ix) for ix in excerpts]

def delete(excerpt_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM excerpt WHERE id = ?', (excerpt_id,))
    conn.commit()
    conn.close()
