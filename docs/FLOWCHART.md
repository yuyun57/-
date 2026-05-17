# Flowchart - 剩食商品上架與搜尋系統

## 1. 使用者流程圖 (User Flow)

### 商家端流程 (Merchant Flow)
```mermaid
flowchart LR
    A([商家存取系統]) --> B[登入或首頁]
    B --> C{選擇操作}
    C -->|新增| D[填寫新增商品表單]
    C -->|管理| E[進入商品列表頁]
    D --> F[提交並儲存]
    F --> E
    E --> G{選擇單一商品操作}
    G -->|編輯| H[填寫修改表單並儲存]
    G -->|刪除| I[確認並刪除商品]
    G -->|狀態切換| J[切換為上下架/已售完]
    H --> E
    I --> E
    J --> E
```

### 學生/消費者端流程 (Consumer Flow)
```mermaid
flowchart LR
    A([學生存取系統]) --> B[進入首頁/商品瀏覽頁]
    B --> C{選擇瀏覽或搜尋條件}
    C -->|直接瀏覽| D[查看所有商品列表]
    C -->|篩選價格| E[選取價格區間或排序]
    C -->|篩選類型| F[選擇便當/麵包等分類]
    C -->|搜尋商家| G[輸入商家名稱搜尋]
    E --> D
    F --> D
    G --> D
    D --> H[點擊欲購買的商品]
    H --> I[查看商品詳細資訊與領取時間]
    I --> J([前往實體店面購買])
```

## 2. 系統序列圖 (Sequence Diagram)

### 商家新增商品流程
```mermaid
sequenceDiagram
    actor Merchant as 商家
    participant Browser
    participant Flask
    participant DB as SQLite
    Merchant->>Browser: 填寫商品資訊並送出
    Browser->>Flask: POST /merchant/products
    Flask->>Flask: 驗證圖片與表單資料
    Flask->>DB: INSERT INTO products
    DB-->>Flask: 成功
    Flask-->>Browser: 重新導向至商品列表頁
```

### 學生搜尋與篩選流程
```mermaid
sequenceDiagram
    actor Student as 學生
    participant Browser
    participant Flask
    participant DB as SQLite
    Student->>Browser: 選擇條件(例如: 價格小於100)並送出
    Browser->>Flask: GET /products?max_price=100
    Flask->>DB: SELECT * FROM products WHERE price <= 100 AND status = '上架'
    DB-->>Flask: 回傳符合條件的資料
    Flask->>Flask: 透過 Jinja2 渲染畫面
    Flask-->>Browser: 回傳 HTML 頁面
```

## 3. 功能清單對照表

| 功能名稱 | 角色 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- | --- |
| 瀏覽所有商品 | 學生 | `/products` | GET | 列出所有上架的剩食商品，支援 query parameters 篩選 |
| 商品詳細資訊 | 學生 | `/products/<id>` | GET | 查看特定商品的詳細資訊 |
| 商家商品列表 | 商家 | `/merchant/products` | GET | 商家檢視自己上架的所有商品 |
| 新增商品畫面 | 商家 | `/merchant/products/new` | GET | 顯示新增表單 |
| 送出新增商品 | 商家 | `/merchant/products` | POST | 接收表單並存入資料庫 |
| 修改商品畫面 | 商家 | `/merchant/products/<id>/edit` | GET | 顯示預先填好資料的修改表單 |
| 送出修改商品 | 商家 | `/merchant/products/<id>/edit` | POST | 更新資料庫中的商品資訊 |
| 刪除商品 | 商家 | `/merchant/products/<id>/delete` | POST | 從資料庫刪除或標記為刪除 |
