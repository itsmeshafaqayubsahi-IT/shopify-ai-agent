# core/shopify_tools.py
import requests
from config import SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN

class ShopifyTools:
    def __init__(self):
        self.store_url = SHOPIFY_STORE_URL
        self.access_token = SHOPIFY_ACCESS_TOKEN
        self.headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token
        }

    def verify_customer_and_get_order(self, email: str, order_name: str):
        """
        Customer identity verify karta hai aur Shopify se order details fetch karta hai.
        """
        # Agar credentials set nahi hain toh simulation/mock data return karega testing ke liye
        if not self.store_url or "your-store" in self.store_url:
            return {
                "success": True,
                "mock": True,
                "order_details": {
                    "order_name": order_name,
                    "email": email,
                    "status": "Fulfilled",
                    "fulfillment_status": "Shipped",
                    "tracking_number": "TRK987654321",
                    "items": ["Classic Cotton Kurta (Size: M)"]
                }
            }

        # Real Shopify Admin API call
        api_url = f"https://{self.store_url}/admin/api/2024-01/orders.json?name={order_name}&status=any"
        try:
            response = requests.get(api_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                orders = response.json().get("orders", [])
                if not orders:
                    return {"success": False, "error": "Order not found with this name."}
                
                order = orders[0]
                # Email verification check
                if order.get("email", "").lower() != email.lower():
                    return {"success": False, "error": "Customer email does not match order records. Identity verification failed."}
                
                return {
                    "success": True,
                    "order_details": {
                        "order_name": order.get("name"),
                        "email": order.get("email"),
                        "financial_status": order.get("financial_status"),
                        "fulfillment_status": order.get("fulfillment_status", "Unfulfilled"),
                        "line_items": [item["title"] for item in order.get("line_items", [])]
                    }
                }
            else:
                return {"success": False, "error": f"Shopify API error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def submit_return_request(self, order_name: str, reason: str):
        """
        Return ya cancellation ki request ko staff approval ke liye queue mein daalta hai.
        """
        # Return submission logic (yahan aap database ya helpdesk ticket create kar sakti hain)
        return {
            "success": True,
            "message": f"Return request for order {order_name} has been successfully submitted for staff approval. Reason: {reason}"
        }