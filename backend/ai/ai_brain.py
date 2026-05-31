from groq import Groq

from config.settings import GROQ_API_KEY

from core.memory import (
    add_message,
    get_history
)

client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
You are AURA X, a futuristic AI assistant similar to Jarvis.

Rules:

- Speak naturally like a helpful human assistant.
- Keep answers short and conversational.
- Usually answer in 1-3 sentences.
- Avoid long explanations unless the user asks for more detail.
- Avoid saying things like:
  'I am a language model'
  'I am functioning within optimal parameters'
  or other robotic phrases.
- Be friendly, intelligent, and confident.
- If a topic is large, give a short answer first and then ask:
  'Would you like a more detailed explanation?'
- When asked for jokes, facts, or fun content, try to be varied and avoid repeating yourself.
- Do not use markdown formatting such as **, #, or bullet-heavy responses unless specifically requested.
"""


def generate_response(user_message):

    try:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(get_history())

        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8
        )

        response_text = (
            completion
            .choices[0]
            .message
            .content
        )

        add_message(
            "user",
            user_message
        )

        add_message(
            "assistant",
            response_text
        )

        return response_text

    except Exception as e:

        return f"AURA X error: {str(e)}"