# core/agent.py
import json
import datetime

class ShopifySupportAgent:
    def __init__(self):
        # Strict System Prompt to prevent invented store policies
        self.system_prompt = (
            "You are a professional and helpful customer support AI agent for a Shopify store. "
            "You must ONLY answer product questions, order tracking, and store policies using the provided "
            "approved knowledge base or Shopify tool data. "
            "NEVER invent or make up store policies, return windows, or discounts if they are not in your context. "
            "If information is missing, or if the customer asks for a refund, cancellation, or human help, "
            "you must politely inform them that you are escalating the request to a human support team member."
        )

    def log_mock_email_to_owner(self, customer_email: str, order_name: str, message: str):
        """
        Simulates sending an email notification to the store owner's inbox.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n" + "="*60)
        print(" 📧 [MOCK EMAIL SENT TO STORE OWNER / SUPPORT TEAM]")
        print("="*60)
        print(f" Timestamp : {timestamp}")
        print(f" To        : owner@store-support.com")
        print(f" Customer  : {customer_email or 'Not Provided'}")
        print(f" Order     : {order_name or 'N/A'}")
        print(f" Query     : {message}")
        print(f" Status    : 🟢 Delivered (Action Required: Human Follow-up)")
        print("="*60 + "\n")

    def process_message(self, user_message: str, customer_email: str = None, order_name: str = None):
        response_data = {
            "reply": "",
            "escalate_to_human": False,
            "tool_called": None
        }

        # Check for escalation keywords
        if any(kw in user_message.lower() for kw in ["cancel", "refund", "human", "talk to agent", "support"]):
            # Trigger mock email log in terminal
            self.log_mock_email_to_owner(customer_email, order_name, user_message)
            
            response_data["reply"] = "I understand you need assistance with this request. Since refunds and cancellations require human approval, I have notified our support team via email. A team member will reach out to you shortly."
            response_data["escalate_to_human"] = True
        else:
            response_data["reply"] = f"Thank you for reaching out! I'm here to help you with your query regarding: '{user_message}'. How else can I assist you with our store policies or products today?"
            
        return response_data