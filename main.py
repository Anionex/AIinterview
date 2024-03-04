# gradio程序在运行时会生成不止一个实例，但是全局变量不会生成新的实例
# from stt_comm.stt import STT

import gradio as gr
import os
import dotenv
import gradio_multimodalchatbot
import gradio_unifiedaudio

import chat_channel
from modules.webui import *


dotenv.load_dotenv()
from chat_channel import bot
from modules.presets import small_and_beautiful_theme

SUBMIT_BTN_ICON = "https://www.iconfinder.com/icons/8665597/download/png/512"

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history


def user(user_message, history):
    return "", history + [[user_message, None]]


# def audio_transcribe(stream, new_chunk):
#     if stream is not None:
#         stream = merge(stream, new_chunk)
#     else:
#         stream = new_chunk
#
#     return stream, transcriber(stream)


def main():
    # stt = STT()
    with gr.Blocks(title="chat_demo", theme="soft") as demo:
        gr.Markdown("# AI面试文字DEMO \n *开始面试*")

        with gr.Row():
            with gr.Column(scale=6, elem_id="chatbot-area"):
                with gr.Row(elem_id="chatbot-header"):
                #     gr.HTML(get_html("chatbot_header_btn.html").format(
                #         json_label="历史记录（JSON）",
                #         md_label="导出为 Markdown"
                #     ), elem_id="chatbot-header-btn-bar")
                    degree_btn = gr.Dropdown(label="公司规模", choices=["大型", "中型", "小型"], scale=9)
                    # gr.Button("喝水")
                chatbot = gr.Chatbot(label="会客间", height=500, scale=99, show_copy_button=True)

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
            msg = gr.Textbox(scale=9, label="你的回答", placeholder="如果面试官不满意，可能会随时结束，请谨言慎行😊")
            # audio_input = gr.Microphone(sources=["microphone"], label="🎙️", streaming=True, scale=1)
            with gr.Column(scale=1):
                with gr.Row():
                    submit_btn = gr.Button(value="",icon=SUBMIT_BTN_ICON, min_width=0, scale=1)
                    file_upload_btn = gr.UploadButton("📁（开发中）", file_types=["images", "video", "audio"], min_width=0, scale=1)
                clear_btn = (gr.Button(value="Clear all", min_width=0, scale=1))
        with gr.Row():
            gr.HTML(get_html("footer.html"))

        msg.submit(user, [msg, chatbot]).then(bot, [msg, chatbot, model_selector, job, job_desc, job_require], outputs=[msg, chatbot])
        submit_btn.click(user, [msg, chatbot]).then(bot, [msg, chatbot, model_selector, job, job_desc, job_require], outputs=[msg, chatbot])
        clear_btn.click(lambda: None, None, chatbot, queue=False)
        # audio_input.stream(audio_transcribe, ["state", audio_input], ["state", msg])
        # 如果chatbot选项变成NOne 会怎么样？
        # # file_msg = file_upload_btn.upload(add_file, [chatbot, file_upload_btn], [chatbot], queue=False).then(
        #     bot, [chatbot, model_selector], chatbot
        # )
        # job_desc.change(chat_channel.change_job_desc, job_desc, None)
        # job_require.change(chat_channel.change_job_require, job_require, None)
        # job.change(chat_channel.change_job, job, None)
    demo.queue(default_concurrency_limit=5)
    demo.launch()

if __name__ == '__main__':
    main()
