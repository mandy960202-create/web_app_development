from .db_manager import get_db_connection

def create(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO book (title) VALUES (?)', (title,))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id

def get_all(search_keyword=None):
    conn = get_db_connection()
    if search_keyword:
        query = "SELECT * FROM book WHERE title LIKE ? ORDER BY created_at DESC"
        books = conn.execute(query, (f'%{search_keyword}%',)).fetchall()
    else:
        books = conn.execute('SELECT * FROM book ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(ix) for ix in books]

def get_by_id(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM book WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    return dict(book) if book else None

def update(book_id, title=None, notes=None, rating=None):
    conn = get_db_connection()
    updates = []
    params = []
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if notes is not None:
        updates.append("notes = ?")
        params.append(notes)
    if rating is not None:
        updates.append("rating = ?")
        params.append(rating)
        
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(book_id)
        query = f"UPDATE book SET {', '.join(updates)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()
    conn.close()

def delete(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM book WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
