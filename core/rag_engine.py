# core/rag_engine.py

class StoreRAG:
    def __init__(self):
        # Approved Store Knowledge Base (FAQs & Policies)
        self.knowledge_base = {
            "shipping": "We offer standard shipping (3-5 business days) and expedited shipping (1-2 business days). Shipping costs are calculated at checkout. Free shipping on orders over $50.",
            "return": "Items can be returned within 30 days of delivery. Items must be unworn, unwashed, and in original packaging. Refunds require staff approval.",
            "cancellation": "Orders can be canceled within 2 hours of placement. After that, they enter fulfillment and must go through the return process.",
            "payment": "We accept major credit cards, PayPal, and Apple Pay securely through Shopify checkout."
        }

    def search_knowledge(self, query: str):
        """
        User ke query ke mutabiq relevant store policy ya FAQ search karta hai.
        """
        query_lower = query.lower()
        matched_info = []

        for key, text in self.knowledge_base.items():
            # Check if keyword or its root stem is in the user query
            if key in query_lower or key[:-1] in query_lower:
                matched_info.append(text)

        if matched_info:
            return " ".join(matched_info)
        
        return None