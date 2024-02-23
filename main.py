import gradio as gr
import os
import dotenv
import gradio_multimodalchatbot

import chat_channel
from modules.webui import *


dotenv.load_dotenv()
from chat_channel import bot
from modules.presets import small_and_beautiful_theme

SUBMIT_BTN_ICON = "https://www.iconfinder.com/icons/8665597/download/png/512"

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def clear_all(msg, chatbot):
    msg = ""
    chatbot = []
def main():

    with gr.Blocks(title="chat_demo", theme="soft") as demo:
        gr.Markdown("# AI面试文字DEMO \n *开始面试*")

        with gr.Row():
            with gr.Column(scale=6, elem_id="chatbot-area"):
                with gr.Row(elem_id="chatbot-header"):
                #     gr.HTML(get_html("chatbot_header_btn.html").format(
                #         json_label="历史记录（JSON）",
                #         md_label="导出为 Markdown"
                #     ), elem_id="chatbot-header-btn-bar")
                    degree_btn = gr.Dropdown(label="难度", choices=["困难", "一般", "简单"], scale=9)
                    # gr.Button("喝水")
                chatbot = gr.Chatbot(label="会客间", height=500, scale=99)

            with gr.Tab("基础设置"):
                with gr.Accordion(label="必填项目", open=True, elem_id="accordion-1"):
                    job = gr.Textbox(label="职位", placeholder="您想要应聘什么职位？",
                                          elem_id="system-txtbox-3")
                    job_desc = gr.Textbox(label="职位描述", placeholder="在此处输入职位描述...", elem_id="system-txtbox-3")
                    job_require = gr.Textbox(label="职位要求", placeholder="在此处输入职位要求...", elem_id="system-txtbox-3")
                    # gr.HTML("<style>#system-txtbox-2 {height:32vh;} #system-txtbox-3 {height:21vh;}</style>")
            with gr.Tab("高级"):
                model_selector = gr.Dropdown(label="model",
                                             choices=["gpt-4-0125-preview", "gpt-3.5-turbo", "gpt-4-0125-preview",
                                                      "gpt-4-all", "gpt-4-vision-preview"], elem_id="system-txtbox-2")
                with gr.Row():
                    gr.Textbox(label="自定义system prompt", value="请注意prompt内容", scale=9, elem_id="system-txtbox-2")
                    apply_prompt_btn = gr.Button(value="应用", min_width=0, scale=1)
        with gr.Row():
            msg = gr.Textbox(scale=8, label="你的回答", placeholder="如果面试官不满意，可能会随时结束，请谨言慎行😊")
            with gr.Column(scale=1):
                with gr.Row():
                    submit_btn = gr.Button(value="",icon=SUBMIT_BTN_ICON, min_width=0, scale=1)
                    file_upload_btn = gr.UploadButton("📁（开发中）", file_types=["images", "video", "audio"], min_width=0, scale=1)
                clear_btn = (gr.Button(value="Clear all", min_width=0, scale=1)).click(clear_all, [msg, chatbot])
        with gr.Row():
            gr.HTML(get_html("footer.html"))
            # gr.Markdown("![](https://img.shields.io/badge/built_with-gradio-orange?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTc2IiBoZWlnaHQ9IjU3NiIgdmlld0JveD0iMCAwIDU3NiA1NzYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0yODcuNSAyMjlMODYgMzQ0LjVMMjg3LjUgNDYwTDQ4OSAzNDQuNUwyODcuNSAyMjlaIiBzdHJva2U9InVybCgjcGFpbnQwX2xpbmVhcl8xMDJfNykiIHN0cm9rZS13aWR0aD0iNTkiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTI4Ny41IDExNkw4NiAyMzEuNUwyODcuNSAzNDdMNDg5IDIzMS41TDI4Ny41IDExNloiIHN0cm9rZT0idXJsKCNwYWludDFfbGluZWFyXzEwMl83KSIgc3Ryb2tlLXdpZHRoPSI1OSIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNODYgMzQ0TDI4OCAyMjkiIHN0cm9rZT0idXJsKCNwYWludDJfbGluZWFyXzEwMl83KSIgc3Ryb2tlLXdpZHRoPSI1OSIgc3Ryb2tlLWxpbmVqb2luPSJiZXZlbCIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJwYWludDBfbGluZWFyXzEwMl83IiB4MT0iNjAiIHkxPSIzNDQiIHgyPSI0MjkuNSIgeTI9IjM0NCIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjRjlEMTAwIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0Y5NzcwMCIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXJfMTAyXzciIHgxPSI1MTMuNSIgeTE9IjIzMSIgeDI9IjE0My41IiB5Mj0iMjMxIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNGOUQxMDAiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjRjk3NzAwIi8+CjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQyX2xpbmVhcl8xMDJfNyIgeDE9IjYwIiB5MT0iMzQ0IiB4Mj0iNDI4Ljk4NyIgeTI9IjM0MS44MTEiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iI0Y5RDEwMCIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGOTc3MDAiLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8L3N2Zz4K "")")
            # gr.Markdown("![](https://img.shields.io/badge/model-gpt4-purple?logo=openai "")")


        msg.submit(bot, [msg, chatbot, model_selector], outputs=[msg, chatbot])
        submit_btn.click(bot, [msg, chatbot, model_selector], outputs=[msg, chatbot])
        # 如果chatbot选项变成NOne 会怎么样？
        # # file_msg = file_upload_btn.upload(add_file, [chatbot, file_upload_btn], [chatbot], queue=False).then(
        #     bot, [chatbot, model_selector], chatbot
        # )
        job_desc.change(chat_channel.change_job_desc, job_desc, None)
        job_require.change(chat_channel.change_job_require, job_require, None)
        job.change(chat_channel.change_job, job, None)
    demo.queue()
    demo.launch()

if __name__ == '__main__':
    main()
