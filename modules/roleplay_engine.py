import openai
import os
from modules.roleplay import load_system_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_roleplay(system_prompt: str, payload: dict, user_text: str, history: list):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"DATOS DEL ESCENARIO:\n{payload}"}
    ]

    for h in history:
        messages.append(h)

    messages.append({"role": "user", "content": user_text})

    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=0.7
    )

    assistant_text = response.choices[0].message.content

    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": assistant_text})

    return assistant_text, history
