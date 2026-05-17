# API Design Document - 路由與頁面設計

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁 (跳轉)** | GET | `/` | — | 跳轉至 `/products` |
| **全站商品列表** | GET | `/products` | `consumer/index.html` | 消費者檢視或篩選商品 |
| **商品詳細資訊** | GET | `/products/<id>` | `consumer/detail.html` | 消費者查看單一商品的剩餘數量與領取時間 |
| **商家管理列表** | GET | `/merchant/products` | `merchant/index.html` | 商家檢視自己上架的所有庫存商品 |
| **新增商品表單** | GET | `/merchant/products/new`| `merchant/new.html` | 顯示讓商家填寫新商品的表單介面 |
| **儲存新商品** | POST| `/merchant/products` | — | 接收新增表單參數，儲存資料庫並重導向 |
| **修改商品表單** | GET | `/merchant/products/<id>/edit`| `merchant/edit.html`| 顯示編輯商品的表單，並預載入舊資料 |
| **儲存商品變更** | POST| `/merchant/products/<id>/update`| — | 處理編輯表單送出的變更並重導向 |
| **下架/切換狀態**| POST| `/merchant/products/<id>/status`| — | 快速切換商品的上下架狀態 |
| **刪除商品** | POST| `/merchant/products/<id>/delete`| — | 確認刪除指定商品並重導向 |

## 2. 每個路由的詳細說明

- **消費者路由 (Consumer)**：
  - 輸入：利用 URL parameters (如 `?type=便當&max_price=100`) 接收消費者查詢條件。
  - 邏輯：呼叫 `product_model.get_all_products(filters)` 來取得商品字典陣列。
  - 輸出：透過 Jinja2 將陣列與 `index.html` 渲染合併後回傳給前端。如果有單獨查看需求則渲染 `detail.html`，若找不到商品顯示 `404` 或 Flash 錯誤。
  
- **商家路由 (Merchant)**：
  - 輸入：利用表單欄位 (`request.form.get`) 接收 `name`, `discount_price` 等詳細資訊。
  - 邏輯：檢查必填是否為空，若無誤則呼叫 `create_product` 或 `update_product`，錯誤則回傳前端頁面顯示 `flash message`。
  - 輸出：若所有修改操作成功皆會透過 `redirect(url_for('merchant.index'))` 回到管理列表避免表單重複提交，而 `edit`/`new` 行為將返回對應模板。且因為純 HTML 限制，更新與刪除必須使用 `POST` 方法。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates`：
- `base.html`：**這是全站基礎**，需搭載 Bootstrap，並包含導覽列與提示訊息區塊 (`{% block content %}`)。
- **Consumer**：
  - `consumer/index.html`：繼承 base，左邊為過濾器、右邊呈現商品卡。
  - `consumer/detail.html`：繼承 base，顯示大型商品標示與領取地點時間。
- **Merchant**：
  - `merchant/index.html`：繼承 base，以表格條列專屬商品與控制按鈕。
  - `merchant/new.html`：繼承 base，提供輸入欄位。
  - `merchant/edit.html`：繼承 base，回填 `value="{{ product.x }}"` 給商家編輯。

## 4. 路由骨架程式碼

路由骨架建立於 `app/routes/consumer_routes.py` 以及 `app/routes/merchant_routes.py` 內。
