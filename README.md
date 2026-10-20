# 🛍️ Shopify AI Support Agent

An intelligent, hallucination-free AI customer support agent built for Shopify stores using Python (FastAPI), RAG (Retrieval-Augmented Generation) for store policies, and Shopify Admin API tools for real-time order tracking and customer verification.

## 🚀 Features
- **Strict Guardrails**: Prevents AI hallucination by strictly restricting answers to verified store policies.
- **RAG Policy Engine**: Automatically handles customer queries regarding shipping, returns, cancellations, and payments.
- **Shopify Order Tracking**: Securely verifies customer email against order numbers to fetch live fulfillment and tracking details.
- **Human Escalation & Mock Email Alerts**: Instantly flags refunds/cancellations and simulates dispatching email alerts to the store support team.
- **Clean Web UI**: Lightweight, responsive chat interface built-in.

---

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, Uvicorn, Pydantic
- **Integration**: Shopify Admin REST API / Requests
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)

---

## ⚙️ Installation & Setup

1. **Clone or Download the Repository**
2. **Create and Activate Virtual Environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate