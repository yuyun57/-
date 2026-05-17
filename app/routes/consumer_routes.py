from flask import Blueprint, render_template, request, redirect, url_for, flash
import app.models.product_model as product_model
import app.models.merchant_model as merchant_model

consumer_bp = Blueprint('consumer', __name__)

@consumer_bp.route('/')
def root():
    """首頁重導向：將使用者引導至商品列表"""
    return redirect(url_for('consumer.index'))

@consumer_bp.route('/products')
def index():
    """處理搜查參數並渲染首頁的商品列表"""
    filters = {}
    max_price = request.args.get('max_price')
    type_filter = request.args.get('type')
    merchant_id = request.args.get('merchant_id')
    
    if max_price and max_price.isdigit():
        filters['max_price'] = max_price
    if type_filter:
        filters['type'] = type_filter
    if merchant_id and merchant_id.isdigit():
        filters['merchant_id'] = merchant_id
        
    products = product_model.get_all_products(filters)
    merchants = merchant_model.get_all_merchants()
    return render_template('consumer/index.html', products=products, merchants=merchants, filters=filters)

@consumer_bp.route('/products/<int:id>')
def detail(id):
    """取得單獨商品詳細資訊並渲染"""
    product = product_model.get_product_by_id(id)
    if not product:
        flash("找不到該商品")
        return redirect(url_for('consumer.index'))
    return render_template('consumer/detail.html', product=product)
