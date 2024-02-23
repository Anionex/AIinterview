is_quit = 0
import gradio as gr
import os
from openai import OpenAI


def stop_generation():
    global is_quit
    is_quit = 1

job = ""
job_desc = ""
job_require = ""
def change_job_desc(job_desc_):
    global job_desc
    job_desc = job_desc_


def change_job(job_):
    global job
    job = job_


def change_job_require(job_require_):
    global job_require
    job_require = job_require_




def bot(message, history, model):
    system_prompt = "面试职位:\n" + job + "职位描述:\n" + job_desc + "\n" + "职位要求：\n" + job_require + "\n"
    identity = "请你作为一名任何领域的专业面试官，根据[面试职位]、[职位描述]和[职位要求]面试前来的应聘者。"
    flow = "你们的面试采用一问一答的形式，一开始你会根据[面试职位]、[职位描述]和[职位要求]提醒应聘者应聘本职位的一些注意事项，并紧接着进入角色，问出面试的第一个问题。当应聘者说“停止面试”，你会告诉应聘者是否被聘用以及被或不被聘用的原因，并紧接着退出角色，复盘本次面试是否达到要求。"
    character = "进入角色后，你的语气应该立马变得严厉，并且带居高临下的姿态,如果你感觉对方没有诚意，可以简单责备对方并立即离场，然后退出角色并直接复盘本次失败的原因和本次面试的发挥。注意，当你退出角色之前，你的责备应该口语化而不是一大串，应该区分没有“能力”和没有“诚意”。更重要的是，你和用户的互动，特别是面试的提问应该紧紧围绕着给出的[职位描述]和[职位要求]。如果[面试职位]、[职位描述]和[职位要求]其中一个为空，请主动询问相关内容。"
    if os.getenv("identity") != None:
        identity = os.getenv("identity")
    if os.getenv("flow") != None:
        flow = os.getenv("flow")
    if os.getenv("character") != None:
        character = os.getenv("character")
    system_prompt += identity + flow + character + "\n现在，面试正式开始！"
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