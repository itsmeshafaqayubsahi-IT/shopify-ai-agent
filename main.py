# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from core.agent import ShopifySupportAgent
from core.shopify_tools import ShopifyTools
from core.rag_engine import StoreRAG

app = FastAPI(title="Shopify AI Support Agent", version="1.0")

# Initialize modules
agent = ShopifySupportAgent()
shopify = ShopifyTools()
rag = StoreRAG()

# Request Model for Chat
class ChatRequest(BaseModel):
    message: str
    customer_email: Optional[str] = None
    order_name: Optional[str] = None

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        user_msg = req.message
        
        # 1. Check if user is asking about order tracking or status
        if any(kw in user_msg.lower() for kw in ["order", "tracking", "status", "where is my"]):
            if not req.customer_email or not req.order_name:
                return {
                    "reply": "To check your order status and tracking details, please provide your Order Number (e.g., #1022) and the Email address used during purchase for verification.",
                    "escalate_to_human": False,
                    "requires_verification": True
                }
            
            # Verify customer & fetch order via Shopify tool
            verification_result = shopify.verify_customer_and_get_order(req.customer_email, req.order_name)
            if not verification_result["success"]:
                return {
                    "reply": f"Verification Failed: {verification_result['error']}",
                    "escalate_to_human": False
                }
            
            order_data = verification_result["order_details"]
            return {
                "reply": f"Order Verified! Here are your details:\n- Order: {order_data.get('order_name')}\n- Status: {order_data.get('fulfillment_status', 'Processing')}\n- Tracking Number: {order_data.get('tracking_number', 'Will be updated soon')}",
                "escalate_to_human": False,
                "tool_called": "verify_customer_and_get_order"
            }

        # 2. Check Store RAG for Policies & FAQs
        rag_answer = rag.search_knowledge(user_msg)
        if rag_answer:
            return {
                "reply": f"{rag_answer}\n\n*(Source: Official Store Policy)*",
                "escalate_to_human": False,
                "tool_called": "rag_knowledge_base"
            }

        # 3. Default Agent Processing (Escalations, general chat)
        agent_response = agent.process_message(user_msg, req.customer_email, req.order_name)
        return agent_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve Static UI if available
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")