from flask import Blueprint, request, jsonify
from ..db import session
import uuid
from datetime import datetime

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/cart", methods=["POST"])
def save_cart():
    data = request.json

    items = [uuid.UUID(i) for i in data["items"]]

    session.execute("""
        INSERT INTO carts (user_id, items)
        VALUES (%s, %s)
    """, (uuid.UUID(data["user_id"]), items))

    return jsonify({"message": "Cart saved 🛒"})


@orders_bp.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    
    try:
        user_id = uuid.UUID(data["user_id"])
        item_ids = [uuid.UUID(i) for i in data["items"]]
        payment_method = data.get("payment_method", "mpesa")
        shipping_info = data.get("shipping_info", {})
        
        # 1. Server-side total verification
        total_price = 0
        if not item_ids:
            return jsonify({"error": "Cart is empty"}), 400
            
        for item_id in item_ids:
            row = session.execute("SELECT price FROM products WHERE id=%s", (item_id,)).one()
            if row:
                total_price += float(row['price'])
        
        # Add delivery fee (mock logic: 250 for outside Nairobi, 100 inside)
        delivery_fee = 250 if shipping_info.get("city", "").lower() != "nairobi" else 100
        total_with_delivery = total_price + delivery_fee
        
        # 2. Prevent tampering
        client_total = float(data.get("total", 0))
        if abs(total_with_delivery - client_total) > 1.0: # 1 unit tolerance for rounding
            return jsonify({"error": "Security Alert: Total mismatch. Calculation refreshed."}), 400

        # 3. Handle Payment Statuses
        payment_status = "Pending"
        if payment_method == "mpesa":
            # Simulate M-Pesa STK Push Success
            payment_status = "Paid (M-Pesa)"
        elif payment_method == "bitcoin":
            payment_status = "Awaiting Blockchain"
        else:
            payment_status = "Pending Confirmation"

        order_id = uuid.uuid4()
        created_at = datetime.utcnow()

        import json
        session.execute("""
            INSERT INTO orders (id, user_id, items, total, delivery_fee, shipping_info, payment_method, payment_status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (order_id, user_id, item_ids, total_with_delivery, delivery_fee, json.dumps(shipping_info), payment_method, payment_status, created_at))

        return jsonify({
            "success": True,
            "message": f"Order {str(order_id)[:8]} processed successfully.",
            "order_id": str(order_id),
            "status": payment_status,
            "total": total_with_delivery
        })

    except Exception as e:
        print(f"Checkout Error: {e}")
        return jsonify({"error": "Internal server error during checkout"}), 500
