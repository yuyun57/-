from flask import Blueprint, render_template, request, redirect, url_for, flash
# import app.models.product_model as product_model
# import app.models.merchant_model as merchant_model

consumer_bp = Blueprint('consumer', __name__)

@consumer_bp.route('/')
def root():
    """首頁重導向：將使用者引導至商品列表"""
    pass

@consumer_bp.route('/products')
def index():
    """處理搜查參數並渲染首頁的商品列表"""
    pass

@consumer_bp.route('/products/<int:id>')
def detail(id):
    """取得單獨商品詳細資訊並渲染"""
    pass
