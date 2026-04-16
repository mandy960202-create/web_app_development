from flask import Blueprint

# 設定 Blueprint
bp = Blueprint('books', __name__)

@bp.route('/')
@bp.route('/books')
def list_books():
    """
    [GET] / 或 /books
    處理「書籍列表瀏覽」與「搜尋找書」功能。
    需根據 query 參數 search 傳遞過濾或全列出結果，渲染 list.html。
    """
    pass

@bp.route('/books', methods=['POST'])
def add_book():
    """
    [POST] /books
    處理「記錄新書籍」新增表單。
    驗證通過後從資料庫新增名單，成功即重導向至首頁。
    """
    pass

@bp.route('/books/<int:book_id>')
def book_detail(book_id):
    """
    [GET] /books/<int:book_id>
    顯示單一書籍的詳細頁面、心得、摘錄。
    如該書籍不存在，需回傳 HTTP 404，渲染 detail.html。
    """
    pass

@bp.route('/books/<int:book_id>/notes', methods=['POST'])
def update_notes_rating(book_id):
    """
    [POST] /books/<int:book_id>/notes
    更新或寫入某本書的長篇閱讀心得與 1~5 分評分狀態。
    最後重導回 /books/<book_id>。
    """
    pass

@bp.route('/books/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    [POST] /books/<int:book_id>/delete
    刪除整本書籍與關聯的摘錄資料庫屬性。
    刪除完畢回到首頁。
    """
    pass

@bp.route('/books/<int:book_id>/excerpts', methods=['POST'])
def add_excerpt(book_id):
    """
    [POST] /books/<int:book_id>/excerpts
    處理在選定書籍下的重點摘錄新增表單。
    寫入 DB 之後，返回該書的詳細分頁。
    """
    pass

@bp.route('/excerpts/<int:excerpt_id>/delete', methods=['POST'])
def delete_excerpt(excerpt_id):
    """
    [POST] /excerpts/<int:excerpt_id>/delete
    刪除對應的重點摘錄或金句。
    （為重導向便利，表單常送出隱藏的 book_id 來引導回原本詳情頁）
    """
    pass
