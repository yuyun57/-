from flask import Blueprint, render_template, request, redirect, url_for, flash
# import app.models.product_model as product_model
# import app.models.merchant_model as merchant_model

merchant_bp = Blueprint('merchant', __name__, url_prefix='/merchant')

@merchant_bp.route('/products')
def index():
    """列出商家目前的所有商品"""
    pass

@merchant_bp.route('/products/new')
def new():
    """渲染新增商品表單"""
    pass

@merchant_bp.route('/products', methods=['POST'])
def create():
    """接收表單參數，建立商品並寫入資料庫"""
    pass

@merchant_bp.route('/products/<int:id>/edit')
def edit(id):
    """查詢原資料並渲染編輯表單"""
    pass

@merchant_bp.route('/products/<int:id>/update', methods=['POST'])
def update(id):
    """處理修改資料的請求"""
    pass

@merchant_bp.route('/products/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除商品，並重導向回列表頁"""
    pass

@merchant_bp.route('/products/<int:id>/status', methods=['POST'])
def status(id):
    """切換商品狀態（上下架、已售完）"""
    pass
