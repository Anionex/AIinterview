is_quit = 0
import gradio as gr
import os
from openai import OpenAI
def stop_generation():
    global is_quit
    is_quit = 1

def chat_multimodal(history, message, model):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})
    client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))

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

def chat(message, history, model):
    history_openai_format = [ {"role": "system", "content": ""}]
    history_gradio_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})

        history_gradio_format.append((human, assistant))
    history_openai_format.append({"role": "user", "content": message})
    yield "", history_gradio_format + [(message, "")]
    client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))

    stream = client.chat.completions.create(
        model=model,
        messages=history_openai_format,
        stream=True,
    )
    prefix = ""

    for chunk in stream:

        if chunk.choices[0].delta.content is not None:
            prefix = prefix + chunk.choices[0].delta.content
            yield "", history_gradio_format + [(message, prefix)]
        if is_quit:
            break