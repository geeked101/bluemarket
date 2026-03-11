from flask import Blueprint, jsonify
from backend.db import session
import uuid

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    if not session:
        return jsonify({"error": "Cassandra session not available"}), 500

    rows = session.execute("SELECT * FROM products")
    products = []
    for r in rows:
        products.append({
            "id": str(r['id']),
            "name": r['name'],
            "description": r['description'],
            "price": float(r['price']) if r['price'] is not None else 0.0,
            "stock": r['stock'] if r['stock'] is not None else 0,
            "image_url": r['image_url'],
            "category": r['category'],
            "rating": r['rating'] if r['rating'] is not None else 0.0,
            "review_count": r['review_count'] if r['review_count'] is not None else 0,
            "verified_seller": bool(r['verified_seller']),
            "created_at": r['created_at'].isoformat() if r['created_at'] else None
        })
    return jsonify(products)

@products_bp.route("/products/<id>")
def get_product(id):
    try:
        # Check if the id is a valid UUID
        product_uuid = uuid.UUID(id)
        row = session.execute(
            "SELECT * FROM products WHERE id=%s", (product_uuid,)
        ).one()
        
        if not row:
            return jsonify({"error": "Product not found"}), 404
            
        return jsonify({
            "id": str(row['id']),
            "name": row['name'],
            "description": row['description'],
            "price": float(row['price']) if row['price'] is not None else 0.0,
            "stock": row['stock'] if row['stock'] is not None else 0,
            "image_url": row['image_url'],
            "category": row['category'],
            "rating": row['rating'] if row['rating'] is not None else 0.0,
            "review_count": row['review_count'] if row['review_count'] is not None else 0,
            "verified_seller": bool(row['verified_seller']),
            "created_at": row['created_at'].isoformat() if row['created_at'] else None
        })

    except ValueError:
        return jsonify({"error": "Invalid product ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

