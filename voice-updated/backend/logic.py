# logic.py  ← REPLACE YOUR ENTIRE FILE WITH THIS

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_community.llms import HuggingFaceEndpoint
# import os
# from dotenv import load_dotenv
# from memory import retrieve_memory  # ← this now uses free HF embeddings

# env_path = os.path.join(os.path.dirname(__file__), '.env')
# load_dotenv(env_path)

# # === 1. LLM Setup - ONLY FREE OPTIONS ===
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# if GROQ_API_KEY:
#     print("Using Groq (Llama 3.3 70B) - FAST & FREE")
#     llm = ChatOpenAI(
#         base_url="https://api.groq.com/openai/v1",
#         api_key=GROQ_API_KEY,
#         model="llama-3.3-70b-versatile",
#         temperature=0.7,
#         max_tokens=500
#     )
# elif OPENROUTER_API_KEY and OPENROUTER_API_KEY.startswith("sk-or-"):
#     print("Using OpenRouter Free Tier")
#     llm = ChatOpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=OPENROUTER_API_KEY,
#         model="meta-llama/llama-3.2-3b-instruct:free",
#         temperature=0.7,
#         max_tokens=500
#     )
# else:
#     print("No Groq or OpenRouter key found! Using HuggingFace (slower but 100% free)")
#     # Fully free fallback - no key needed
#     llm = HuggingFaceEndpoint(
#         repo_id="HuggingFaceH4/zephyr-7b-beta",
#         task="text-generation",
#         temperature=0.7,
#         max_new_tokens=500
#     )

# # === 2. Prompt with Memory ===
# prompt_template = """
# You are a friendly, concise, and helpful AI voice assistant.
# Respond naturally in 1–3 short sentences max.

# {memories}User: {user_text}
# Assistant:
# """

# chat_prompt = ChatPromptTemplate.from_template(prompt_template)
# chain = chat_prompt | llm

# def generate_reply(user_text: str) -> str:
#     user_text = user_text.strip()
#     if not user_text:
#         return "Sorry, I didn't catch that. Could you repeat?"

#     try:
#         memories = retrieve_memory(user_text, k=3)
#         response = chain.invoke({"memories": memories, "user_text": user_text})
#         return response.content.strip() if hasattr(response, "content") else str(response).strip()
#     except Exception as e:
#         print(f"LLM error: {e}")
#         return "I'm having a little trouble thinking right now. Try again in a moment!"




# ---------------------------------------------------------------------------------------------------------

# logic.py ← FINAL GROQ VERSION (Dec 2025 – blazing fast)

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from memory import retrieve_memory
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# === GROQ SETUP – FASTEST & FREE ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env! Get free key at https://console.groq.com/keys")

print("Using Groq Llama 3.1 70B – up to 800+ tokens/sec!")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",        # or "llama-3.3-70b-versatile" (even newer)
    api_key=GROQ_API_KEY,
    temperature=0.7,
    max_tokens=512,
)

# === Prompt with memory (same as before) ===
prompt_template = """
You are a friendly, natural, concise voice assistant.
Keep replies short and conversational (1-3 sentences max).

{memories}
User: {user_text}
Assistant:
"""

chat_prompt = ChatPromptTemplate.from_template(prompt_template)
chain = chat_prompt | llm

def generate_reply(user_text: str) -> str:
    user_text = user_text.strip()
    if not user_text:
        return "Sorry, I didn't catch that."

    try:
        memories = retrieve_memory(user_text, k=3)
        response = chain.invoke({"memories": memories, "user_text": user_text})
        return response.content.strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return "Hmm, I'm thinking... try again!"