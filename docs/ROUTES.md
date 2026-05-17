# API Design Document - 路由與頁面設計

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁 (跳轉)** | GET | `/` | — | 跳轉至 `/products` |
| **首頁/所有商品** | GET | `/products` | `consumer/index.html` | 學生檢視與搜尋商品列表 |
| **商品詳情** | GET | `/products/<id>` | `consumer/detail.html` | 學生查看單筆商品詳細資訊 |
| **商家商品列表** | GET | `/merchant/products` | `merchant/index.html` | 商家檢視自己上架的商品 |
| **新增商品頁面** | GET | `/merchant/products/new`| `merchant/new.html` | 顯示新增商品的表單 |
| **建立商品** | POST| `/merchant/products` | — | 儲存至 DB 並重導至列表 |
| **編輯商品頁面** | GET | `/merchant/products/<id>/edit`| `merchant/edit.html`| 顯示編輯商品的表單 |
| **更新商品** | POST| `/merchant/products/<id>/update`| — | 更新至 DB 並重導至列表 |
| **刪除商品**| POST| `/merchant/products/<id>/delete`| — | 從 DB 標記刪除，重導至列表 |
| **切換商品狀態**| POST| `/merchant/products/<id>/status`| — | 切換至已下架或已售完狀態，重導 |

## 2. 每個路由的詳細說明

- 透過 `consumer_routes` 與 `merchant_routes` 的 controller 將對應行為分離。
- 消費者方僅能讀取 (`GET`)，並透過 Query Parameters (`?max_price=100&merchant_id=2&type=便當`) 來篩選商品。
- 商家方包含完整的增刪改查 (`CRUD`) 以及表單的處理 (`POST`)。
- 網頁發生找不到商品時回傳 404，如果無商家的假登入驗證失敗則將路由限制 (目前 MVP 不做商家 auth)。

## 3. Jinja2 模板清單

- `templates/base.html`: 定義框架
- `templates/consumer/index.html`: 首頁列表支援卡片設計
- `templates/consumer/detail.html`: 商品詳情視圖
- `templates/merchant/index.html`: 後台管理資料表
- `templates/merchant/new.html`: 商家用來新增
- `templates/merchant/edit.html`: 商家用來修改

## 4. 路由骨架程式碼

已建立於 `app/routes/ consumer_routes.py`, `merchant_routes.py`。
