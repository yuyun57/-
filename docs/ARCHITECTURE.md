# 系統架構文件 (Architecture) - 剩食商品上架與搜尋系統

## 1. 技術架構說明
本專案採用傳統的伺服器端渲染 (Server-Side Rendering) 架構，不進行前後端分離，藉此降低開發初期的複雜度與部署門檻。

- **後端 (Backend)**：採用 Python + Flask，輕量且適合快速開發。
- **模板引擎 (Template Engine)**：採用 Jinja2，由 Flask 在後端將資料與 HTML 模板結合後回傳給瀏覽器。
- **資料庫 (Database)**：採用 SQLite，以本機檔案形式儲存資料，不需要額外架架設資料庫伺服器。

**MVC 模式說明**：
- **Model**：負責與 SQLite 互動（如執行 SELECT 條件搜尋商品，或 INSERT 新增商品），處理所有的業務資料與查詢邏輯。
- **View**：即 Jinja2 模板，負責介面的展示，接收 Controller 傳來的資料並渲染成最終的網頁 (HTML)。
- **Controller**：即 Flask 的 Routes (路由)，負責接收前端請求 (如學生的查詢與篩選參數)，調用對應的 Model 取得資料，再交由 View 渲染。

## 2. 專案資料夾結構

```text
/
├── app/
│   ├── models/         # 資料庫模型與操作邏輯 (例如 product_model.py 包含搜尋、新增、修改功能)
│   ├── routes/         # Flask 路由控制器 (例如 merchant_routes.py, consumer_routes.py)
│   ├── templates/      # Jinja2 HTML 模板
│   │   ├── base.html         # 共用樣板 (定義 Navbar, Footer 等)
│   │   ├── merchant/         # 商家專用頁面 (如新增表單、列表)
│   │   └── consumer/         # 學生/消費者專用頁面 (如搜尋列表、商品詳細)
│   └── static/         # CSS、JavaScript 與上傳的商品圖片
│       ├── css/
│       ├── js/
│       └── uploads/          # 儲存商家上傳的實體圖片
├── instance/
│   └── database.db     # SQLite 資料庫檔案
├── docs/               # 開發文件 (PRD, FLOWCHART, ARCHITECTURE 等)
└── app.py              # 程式入口，負責初始化 Flask 與載入路由
```

## 3. 元件關係圖

```mermaid
flowchart TD
    Browser[使用者的瀏覽器 (商家或學生)]
    subgraph Flask App
        Route[Flask Route / Controller]
        Model[Data Model 定義]
        Template[Jinja2 Template]
    end
    DB[(SQLite 資料庫)]
    
    Browser -- "HTTP GET / POST (帶查詢參數)" --> Route
    Route -- "調用 function 查詢或寫入" --> Model
    Model -- "執行 SQL 指令" --> DB
    DB -- "回傳資料" --> Model
    Model -- "回傳整理後的 Tuple/Dict" --> Route
    Route -- "傳送變數" --> Template
    Template -- "渲染 HTML 模板" --> Route
    Route -- "回傳 Response (HTML)" --> Browser
```

## 4. 關鍵設計決策

1. **不採用前後端分離 (全端開發)**：
   為了快速驗證產品概念並完成 MVP，使用 Flask + Jinja2 能夠避免初期管理兩個獨立專案（如 Vue/React + Flask API）與跨域設定（CORS）的複雜度，使專案結構簡單集中。

2. **採用 SQLite 作為資料庫**：
   對於學區範圍內小型商家與學生的初期流量，SQLite 的效能足以應付中小型網站，且不需設定 PostgreSQL 或 MySQL 授權、使用者帳密等伺服器設定，降低部署難度。

3. **使用者權限與路由分離 (Consumer vs Merchant)**：
   在資料夾與路由規劃上，將消費者 (Student/Consumer) 與商家 (Merchant) 的邏輯獨立區分開來（分別設置 `consumer` 與 `merchant` 路由和樣板）。這樣一來若未來要為商家實作專屬登入認證，將比較安全且容易維護，避免功能互相干擾。

4. **圖片直接儲存於本地檔案系統**：
   商家上傳的餐點圖片將儲存於伺服器上的 `static/uploads/` 資料夾中，並在資料庫記錄該圖片的相對路徑。這樣做能省去初期串接 AWS S3 或外部圖床 API 的複雜成本。
