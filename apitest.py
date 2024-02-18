is_quit = 0
import gradio as gr
from openai import OpenAI
def stop_generation():
    global is_quit
    is_quit = 1


def api_test(context, model):

    client = OpenAI(base_url="https://api.link-ai.chat/v1")

    stream = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system",
         "content": "你是openai的机器人"},
        {"role": "user", "content": context}
      ],
      stream=True,
    )
    prefix = ""
    for chunk in stream:

        if chunk.choices[0].delta.content is not None:
            yield(prefix := prefix + chunk.choices[0].delta.content)
        if is_quit:
           break

    # return completion.choices[0].message.content

