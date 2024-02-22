import gradio as gr
import os
import dotenv
import gradio_multimodalchatbot

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
        model_selector = gr.Dropdown(label="model", choices=["gpt-4-0125-preview", "gpt-3.5-turbo", "gpt-4-0125-preview", "gpt-4-all", "gpt-4-vision-preview"], visible=False)
        chatbot = gr.Chatbot(label="会客间")
        with gr.Row():
            msg = gr.Textbox(scale=8, label="你的回答", placeholder="如果面试官不满意，可能会随时结束，请谨言慎行😊")
            with gr.Column(scale=1):
                with gr.Row():
                    submit_btn = gr.Button(value="",icon=SUBMIT_BTN_ICON, min_width=0, scale=1)
                    file_upload_btn = gr.UploadButton("📁（开发中）", file_types=["images", "video", "audio"], min_width=0, scale=1)
                clear_btn = (gr.Button(value="Clear all", min_width=0, scale=1)).click(clear_all, [msg, chatbot])


        msg.submit(bot, [msg, chatbot, model_selector], outputs=[msg, chatbot])
        submit_btn.click(bot, [msg, chatbot, model_selector], outputs=[msg, chatbot])
        # 如果chatbot选项变成NOne 会怎么样？
        # # file_msg = file_upload_btn.upload(add_file, [chatbot, file_upload_btn], [chatbot], queue=False).then(
        #     bot, [chatbot, model_selector], chatbot
        # )

    demo.queue()
    demo.launch()

if __name__ == '__main__':
    main()
