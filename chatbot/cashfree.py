import uuid
import requests
import os
from datetime import datetime, timedelta, timezone

def create_cashfree_payment_link(order_id, amount, name, phone, email="guest@example.com"):
    url = "https://sandbox.cashfree.com/pg/links"  # Use production URL for live

    expiry_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat().replace("+00:00", "+05:30")
    order_id = uuid.uuid4().hex[:8]  # 🔥 ensure unique link_id

    payload = {
        "customer_details": {
            "customer_email": email,
            "customer_name": name,
            "customer_phone": phone
        },
        "link_amount": float(amount),
        "link_currency": "INR",
        "link_purpose": f"Payment for Mango Order #{order_id}",
        "link_id": f"order_{order_id}",
        "link_notify": {
            "send_email": False,
            "send_sms": True
        },
        "link_auto_reminders": True,
        "link_expiry_time": '2025-10-14T15:04:05+05:30',
        "link_meta": {
            "notify_url": "https://yourdomain.com/payment-webhook",
            "return_url": "https://yourdomain.com/thank-you",
            "upi_intent": False
        },
    }

    headers = {
        "x-api-version": "2022-09-01",
        "x-client-id": 'TEST10561022ca7f6114400d5a18e29b22016501',
        "x-client-secret": 'cfsk_ma_test_8915ba929bb54d9d495eede8a6202a7c_c2b5ea45',
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        if response.status_code == 200 and res_json.get("link_url"):
            return res_json["link_url"]
        else:
            print("Cashfree error:", res_json)
            return None
    except Exception as e:
        print("Payment link generation failed:", e)
        return None


if __name__ == "__main__":
    link = create_cashfree_payment_link(
        order_id=1234,
        amount=199.00,
        name="Test User",
        phone="9999999999",
        email="testuser@example.com"
    )
    if link:
        print(f"\n✅ Payment Link Generated:\n{link}")
    else:
        print("\n❌ Failed to generate payment link.")
