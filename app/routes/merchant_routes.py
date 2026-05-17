import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
import app.models.product_model as product_model

merchant_bp = Blueprint('merchant', __name__, url_prefix='/merchant')

# MVP Mock Data
CURRENT_MERCHANT_ID = 1

@merchant_bp.route('/products')
def index():
    """列出商家目前的所有商品"""
    # 這裡過濾出該商家的包含下架的商品，所以我們另外寫一個客製查詢
    conn = product_model.get_db_connection()
    products = conn.execute('SELECT * FROM product WHERE merchant_id = ? ORDER BY created_at DESC', (CURRENT_MERCHANT_ID,)).fetchall()
    conn.close()
    return render_template('merchant/index.html', products=[dict(row) for row in products])

@merchant_bp.route('/products/new')
def new():
    """渲染新增商品表單"""
    return render_template('merchant/new.html')

@merchant_bp.route('/products', methods=['POST'])
def create():
    """接收表單參數，建立商品並寫入資料庫"""
    name = request.form.get('name')
    ptype = request.form.get('type')
    original_price = request.form.get('original_price') or 0
    discount_price = request.form.get('discount_price')
    quantity = request.form.get('quantity')
    pickup_time = request.form.get('pickup_time')
    
    if not name or not ptype or not discount_price or not quantity or not pickup_time:
        flash("請填寫所有必填欄位")
        return redirect(url_for('merchant.new'))
        
    product_model.create_product(CURRENT_MERCHANT_ID, name, ptype, int(original_price), int(discount_price), int(quantity), "", pickup_time)
    flash("商品上架成功", "success")
    return redirect(url_for('merchant.index'))

@merchant_bp.route('/products/<int:id>/edit')
def edit(id):
    """查詢原資料並渲染編輯表單"""
    product = product_model.get_product_by_id(id)
    if not product:
        flash("找不到該商品")
        return redirect(url_for('merchant.index'))
    return render_template('merchant/edit.html', product=product)

@merchant_bp.route('/products/<int:id>/update', methods=['POST'])
def update(id):
    """處理修改資料的請求"""
    name = request.form.get('name')
    ptype = request.form.get('type')
    original_price = request.form.get('original_price') or 0
    discount_price = request.form.get('discount_price')
    quantity = request.form.get('quantity')
    pickup_time = request.form.get('pickup_time')
    
    product_model.update_product(id, name, ptype, int(original_price), int(discount_price), int(quantity), pickup_time)
    flash("商品已更新", "success")
    return redirect(url_for('merchant.index'))

@merchant_bp.route('/products/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除商品"""
    product_model.delete_product(id)
    flash("商品已刪除", "success")
    return redirect(url_for('merchant.index'))

@merchant_bp.route('/products/<int:id>/status', methods=['POST'])
def status(id):
    """切換商品狀態"""
    new_status = request.form.get('status')
    if new_status:
        product_model.update_product_status(id, new_status)
        flash(f"已更新為{new_status}", "success")
    return redirect(url_for('merchant.index'))
