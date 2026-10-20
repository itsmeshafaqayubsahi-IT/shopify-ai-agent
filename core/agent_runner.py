import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOL_REGISTRY

load_dotenv()

# OpenAI client ko local Ollama service par point kar diya gaya hai
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "ollama")  # Ollama dummy key support karta hai
)

# Active local model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")

class UniversalAgent:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.business_name = self.config["business_name"]
        self.system_prompt = self.config["system_prompt"]
        self.enabled_tools = self.config["tools_enabled"]

    def run(self, user_message: str, conversation_history: list = None):
        if conversation_history is None:
            conversation_history = []

        # 1. Prepare messages with system prompt
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        # 2. Gather schemas only for tools enabled in this client's config
        openai_tools = []
        for tool_name in self.enabled_tools:
            if tool_name in TOOL_REGISTRY:
                openai_tools.append(TOOL_REGISTRY[tool_name]["schema"])

        # 3. Call Local Ollama Model
        kwargs = {
            "model": MODEL_NAME,
            "messages": messages
        }
        if openai_tools:
            kwargs["tools"] = openai_tools
            kwargs["tool_choice"] = "auto"

        response = client.chat.completions.create(**kwargs)
        response_message = response.choices[0].message

        # 4. Handle Tool Calls if the model requested any
        if response_message.tool_calls:
            messages.append(response_message) # Append assistant's tool call request
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in TOOL_REGISTRY:
                    # Execute the python function dynamically
                    tool_func = TOOL_REGISTRY[function_name]["function"]
                    tool_output = tool_func(**function_args)

                    # Append tool response back into messages
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_output,
                    })

            # Second call to Ollama to get final answer after tool output
            second_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            return second_response.choices[0].message.content

        return response_message.content