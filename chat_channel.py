is_quit = 0
import gradio as gr
from openai import OpenAI
def stop_generation():
    global is_quit
    is_quit = 1



def chat(message, history, model):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})
    client = OpenAI(base_url="https://api.link-ai.chat/v1")

    stream = client.chat.completions.create(
        model=model,
        messages=history_openai_format,
        stream=True,
    )
    prefix = ""
    for chunk in stream:

        if chunk.choices[0].delta.content is not None:
            yield (prefix := prefix + chunk.choices[0].delta.content)
        if is_quit:
            break