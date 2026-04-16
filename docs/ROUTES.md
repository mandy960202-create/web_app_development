# 路由與頁面設計 (API Design)

## 1. 路由總覽列表

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 瀏覽/搜尋書籍列表 | GET | `/` 或 `/books` | `list.html` | 首頁，顯示所有書籍，若帶有 `?search=` 則進行搜尋 |
| 記錄新書籍 | POST | `/books` | — | 接收表單並新增書名，完成後重導向至首頁 |
| 書籍詳細頁 | GET | `/books/<int:book_id>` | `detail.html` | 顯示書籍詳情、心得、評分以及重點摘錄 |
| 更新心得與評分 | POST | `/books/<int:book_id>/notes` | — | 更新特定書籍的心得與評分，完成後重導向至詳細頁 |
| 刪除書籍 | POST | `/books/<int:book_id>/delete`| — | 刪除整本書籍紀錄，完成後重導向至首頁 |
| 新增重點摘錄 | POST | `/books/<int:book_id>/excerpts`| — | 在特定書籍下新增摘錄，完成後重導向至詳細頁 |
| 刪除重點摘錄 | POST | `/excerpts/<int:excerpt_id>/delete` | — | 刪除特定摘錄，完成後重導向回原書籍詳細頁 |

## 2. 每個路由的詳細說明

### 2.1 瀏覽/搜尋書籍列表
- **路由**: `[GET] /` 或 `[GET] /books`
- **輸入**: URL 參數 `search`（可選）
- **處理邏輯**: 
  - 透過 `request.args.get('search')` 取得參數。
  - 若有值，則呼叫 `book.get_all(search)`，無值則呼叫 `book.get_all()`。
- **輸出**: 渲染 `list.html` 並將 `books` 與當前的 `search` 參數傳遞至前端。
- **錯誤處理**: 若資料庫發生錯誤可簡單呈現 500 系統錯誤。

### 2.2 記錄新書籍
- **路由**: `[POST] /books`
- **輸入**: 表單欄位 `title`（必填）
- **處理邏輯**: 
  - 透過 `request.form.get('title')` 取得輸入內容。
  - 驗證不可為空，調用 `book.create(title)`。
- **輸出**: 成功後使用 HTTP 302 重導向回 `[GET] /books`。
- **錯誤處理**: `title` 為空時，可於前端 flash 錯誤訊息提示使用者。

### 2.3 書籍詳細頁
- **路由**: `[GET] /books/<int:book_id>`
- **輸入**: URL 變數 `book_id`
- **處理邏輯**: 
  - 呼叫 `book.get_by_id(book_id)`。
  - 呼叫 `excerpt.get_all_by_book_id(book_id)` 取得列表。
- **輸出**: 渲染 `detail.html`，傳遞 `book` 物件與 `excerpts` 陣列給 Jinja2 顯示。
- **錯誤處理**: 利用 `abort(404)` 當書籍不存在時回報 HTTP Not Found。

### 2.4 更新心得與評分
- **路由**: `[POST] /books/<int:book_id>/notes`
- **輸入**: 表單欄位 `notes`（選填）、`rating`（選填，應為 1~5 數字）
- **處理邏輯**: 
  - 擷取回傳的資料與驗證欄位合法性。
  - 調用 `book.update(book_id, notes=..., rating=...)` 更新資料表。
- **輸出**: 成功後重導向至詳細頁面 `[GET] /books/<int:book_id>`。
- **錯誤處理**: 傳入違法選項資料可 flash 錯誤回首頁或重新導向回原頁。

### 2.5 刪除書籍
- **路由**: `[POST] /books/<int:book_id>/delete`
- **輸入**: URL 變數 `book_id`
- **處理邏輯**: 
  - 調用 `book.delete(book_id)`。透過底層的 CASCADE 會同步刪除摘錄。
- **輸出**: 成功刪除後重導向回首頁。
- **錯誤處理**: 查無檔案或刪除錯誤。

### 2.6 新增重點摘錄
- **路由**: `[POST] /books/<int:book_id>/excerpts`
- **輸入**: 表單欄位 `content`（必填）
- **處理邏輯**: 
  - 擷取 `content` 並調用 `excerpt.create(book_id, content)`。
- **輸出**: 重導向回目前的書籍詳細頁。
- **錯誤處理**: 欄位為空則重導向回詳細頁，不再寫入。

### 2.7 刪除重點摘錄
- **路由**: `[POST] /excerpts/<int:excerpt_id>/delete`
- **輸入**: 表單隱藏欄位 `book_id` (確保返回哪一面)
- **處理邏輯**: 
  - 調用 `excerpt.delete(excerpt_id)`。
- **輸出**: 重導向回 `[GET] /books/<int:book_id>` 返回對應的操作頁面。
- **錯誤處理**: 無法找到則 fallback 導向首頁。


## 3. Jinja2 模板清單

將會在 `app/templates` 資料夾中實作：

- `base.html`
  全站共用佈局 (Base template)，涵蓋了 HTML 開頭的 `<head>`，包含共用的自定義 CSS 樣式與可能的外掛字型，並且設計有一致的 Navigation 導覽列。
- `list.html`
  擴展自 `base.html`，做為主頁入口，會呈現包含「找書的搜尋列」、「新增書名的表單」與「所有書籍卡片並列展示的畫廊區域」。
- `detail.html`
  擴展自 `base.html`，顯示特定書籍的所有詳細資訊，區分成兩或多大塊區段：「心得與打分操作表單」以及「對應書籍的所有金句摘錄清單列表」。

