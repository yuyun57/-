# 系統架構文件 (Architecture)

## 1. 技術架構說明

本專案採用傳統的伺服器端渲染 (Server-Side Rendering) 架構。

**選用技術與原因：**
- **後端：Python + Flask**
  - **原因**：Flask 輕量、學習曲線平緩，非常適合 MVP 開發與小型專案，能快速建立 API 與頁面路由。
- **模板引擎：Jinja2**
  - **原因**：內建於 Flask，可直接在後端將資料注入 HTML 模板，不需設定複雜的前端框架 (不需要前後端分離)，降低開發門檻。
- **資料庫：SQLite (使用 sqlite3)**
  - **原因**：採用本地檔案形式儲存資料，不需要額外架設資料庫伺服器，方便初期開發、測試與輕量部署。

**Flask MVC 模式說明：**
- **Model (模型)**：負責與 SQLite 資料庫互動（如執行 SELECT 或 INSERT），處理所有與資料相關的運算與封裝。
- **View (視圖)**：由 Jinja2 HTML 模板負責。它負責接收 Controller 傳來的資料並渲染成最終呈現給用戶的網頁。
- **Controller (控制器)**：由 Flask 的 Routes (路由) 負責。負責接收前端請求 (如表單提交或網址跳轉)、呼叫 Model 取得資料，最後把資料交給 View 渲染。

---

## 2. 專案資料夾結構

以下為本專案的完整資料夾樹狀圖與用途說明：

```text
/
├── app/
│   ├── __init__.py     ← 將 app 宣告為 Python 模組
│   ├── models/         ← 資料庫模型 (存放與 DB 操作相關的程式)
│   │   ├── product_model.py
│   │   └── merchant_model.py
│   ├── routes/         ← Flask 路由 (Controller)，處理邏輯轉發
│   │   ├── consumer_routes.py
│   │   └── merchant_routes.py
│   ├── templates/      ← Jinja2 HTML 模板 (View)
│   │   ├── base.html
│   │   ├── consumer/
│   │   └── merchant/
│   └── static/         ← CSS / JS 等網頁靜態資源
│       └── uploads/    ← 儲存商家上傳的商品圖片
├── instance/
│   └── database.db     ← SQLite 資料庫實體檔案
├── docs/               ← 存放 PRD、流程圖、架構設計等技術文件
├── app.py              ← 專案入口點，負責初始化 Flask 與藍圖註冊
└── requirements.txt    ← Python 依賴套件清單
```

---

## 3. 元件關係圖

透過以下的流程圖，可以了解使用者（瀏覽器）的操作是如何一路傳到資料庫再回傳畫面的：

```mermaid
flowchart TD
    Browser[瀏覽器 (Browser)]
    
    subgraph Flask 應用程式
        Route[Flask Route (Controller)]
        Template[Jinja2 Template (View)]
        Model[Data Model]
    end
    
    DB[(SQLite 資料庫)]
    
    Browser -- "1. 發送 GET/POST 請求" --> Route
    Route -- "2. 呼叫方法與傳遞參數" --> Model
    Model -- "3. 執行 SQL (例如 SELECT)" --> DB
    DB -- "4. 回傳實體資料" --> Model
    Model -- "5. 整理資料給路由" --> Route
    Route -- "6. 傳遞參數給模板" --> Template
    Template -- "7. 渲染完成 HTML" --> Route
    Route -- "8. 回傳 HTTP Response" --> Browser
```

---

## 4. 關鍵設計決策

1. **不採用前後端分離：**
   - **原因**：為了在短時間內完成 MVP，使用全端架構可以避免處理前端框架與後端 API 之間的 CORS 設定及 API 文件溝通成本。
2. **採用藍圖 (Blueprints) 隔離路由：**
   - **原因**：雖然專案規模小，但將消費者 (Consumer) 與商家 (Merchant) 的路由分開寫入不同檔案，能大幅減少 `app.py` 的擁擠，後續若是加上權限驗證也能分開處理。
3. **圖片以實體檔案儲存：**
   - **原因**：上傳的圖片儲存於 `static/uploads/` 而非資料庫中，一方面資料庫只記錄路徑，避免資料庫過度肥大；另一方面初期不使用外部 S3，省去雲端配置負擔。
