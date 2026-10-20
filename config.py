# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Aap yahan apni API keys ya Shopify credentials set kar sakti hain
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL", "your-store.myshopify.com")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "your-shopify-token")