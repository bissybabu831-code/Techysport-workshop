import gradio
from groq import Groq

# Groq Client
client = Groq(
    api_key="YOUR_API_KEY_HERE"
)

# System Prompt (Technical Chatbot)
def initialize_messages():
    return [{
        "role": "system",
        "content": (
            "You are a highly skilled technical assistant. "
            "You explain programming, debugging, AI, Python, JavaScript, APIs, web development, "
            "and general tech concepts in a simple and clear way. "
            "You provide correct code examples, explain errors, and suggest fixes. "
            "You never guess — you only give accurate and reliable information. "
            "Your tone is friendly, helpful, and direct."
        )
    }]

messages_prmt = initialize_messages()
print(type(messages_prmt))


# LLM Chat Function
def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )

    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply


# Gradio UI
iface = gradio.ChatInterface(
    customLLMBot,
    chatbot=gradio.Chatbot(height=300),
    textbox=gradio.Textbox(
        placeholder="Ask me anything about coding, errors, AI, or development..."
    ),
    title="Technical Assistant Chatbot",
    description=(
        "A smart technical chatbot that helps you with coding, debugging, AI, and software development."
    ),
    theme="soft",
    examples=[
        "How to fix ModuleNotFoundError in Python?",
        "Explain API with a simple example.",
        "How do I connect frontend and backend?",
        "What is the difference between list and tuple?",
        "Why my VS Code is not detecting Python?"
    ]
)

iface.launch(share=True)
