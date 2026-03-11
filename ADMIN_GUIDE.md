# 🛠️ Blue Market Admin Guide

This guide explains how to manage your marketplace content and implement payments.

## 📦 Managing Products & Categories

The marketplace content is stored in **Apache Cassandra**. You can manage it by editing and running Python scripts.

### 1. Adding/Editing Products
Open `seed_db.py` and modify the `products` list.
- **To Add**: Add a new dictionary object to the list.
- **To Remove**: Delete an object from the list.
- **To Update**: Change the values (price, name, etc.) of an existing object.

**To sync changes to the database:**
```powershell
python seed_db.py
```
*Note: The current script generates new UUIDs, so re-running it will create duplicates unless you add logic to empty the table first or use fixed IDs.*

### 2. Managing Categories
Categories are strings assigned to each product (e.g., `"Vehicles"`, `"Tactical"`).
- **To Add a Category**: Simply use a new category name in the `category` field of a product in `seed_db.py`.
- **To Update UI Filters**: Open `frontend/index.html` and update the `<select id="categoryFilter">` options to match your new categories.

---

## 📲 M-Pesa STK Push Integration (MTN/Airtel similar)

To trigger an actual STK Push prompt on a user's phone, you need to integrate with the **Safaricom Daraja API**.

### 1. Required Credentials
- **Consumer Key & Secret**: From [Daraja Portal](https://developer.safaricom.co.ke/).
- **Business Shortcode**: Your Paybill or Till Number.
- **Lipa Na M-Pesa Online Passkey**: Issued via email or the portal.

### 2. The STK Push Payload
You will need to send a POST request to `https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest` (use `api` for production) with this structure:

```json
{
    "BusinessShortCode": "174379",
    "Password": "BASE64_ENCODED_PASSWORD",
    "Timestamp": "20231027103015",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": "1",
    "PartyA": "2547XXXXXXXX",
    "PartyB": "174379",
    "PhoneNumber": "2547XXXXXXXX",
    "CallBackURL": "https://yourdomain.com/api/payment/callback",
    "AccountReference": "BlueMarket_Order_001",
    "TransactionDesc": "Payment for Tactical Gear"
}
```

### 3. Implementation Workflow
1.  **Backend**: Create a `/api/pay` endpoint in Flask.
2.  **Auth**: Generate an OAuth token using your Consumer Key/Secret.
3.  **Request**: Send the STK Push payload to Safaricom.
4.  **Callback**: Safaricom sends the result (Success/Fail) to your `CallBackURL`.
5.  **Update DB**: Your backend receives the callback and marks the order as "Paid" in Cassandra.
