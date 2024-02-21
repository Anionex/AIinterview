is_quit = 0
import gradio as gr
import os
from openai import OpenAI
def stop_generation():
    global is_quit
    is_quit = 1

system_prompt = "请你作为一名任何领域的面试官，面试前来的应聘者。我们的面试采用一问一答的形式，一开始，我将向你说明我前来应聘的职位，而你一开始会回答应聘本职位的一些注意事项，并紧接着进入角色，问出面试的第一个问题。当我说“停止面试”，你会告诉我是否被聘用以及被或不被聘用的原因，并紧接着退出角色，复盘本次面试是否达到要求。你的语气应该是严格和尊重的，但是带一点长辈对晚辈的轻佻和不屑,如果你感觉对方没有诚意，可以责备对方并立即离场，然后退出角色并直接进入复盘。现在，我要告诉你我面试的岗位。"


def bot(message, history, model):
    history_openai_format = [ {"role": "system", "content": system_prompt}]
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