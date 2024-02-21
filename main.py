import gradio as gr
import os
import dotenv
import gradio_multimodalchatbot

import apitest
dotenv.load_dotenv()
import chat_channel
from modules.presets import small_and_beautiful_theme

SUBMIT_BTN_ICON = "https://www.iconfinder.com/icons/8665597/download/png/512"

def clear_all(msg, chatbot):
    msg = ""
    chatbot = []
def main():

    with gr.Blocks(title="chat_demo", theme=small_and_beautiful_theme) as demo:
        gr.Markdown("# Chat Demo built with gradio Blocks")
        model_selector = gr.Dropdown(label="model", choices=["gpt-4-0125-preview", "gpt-4-all", "gpt-4-vision-preview"])
        chatbot = gr.Chatbot()
        with gr.Row():
            msg = gr.Textbox(scale=8)
            with gr.Column(scale=1):
                with gr.Row():
                    submit_btn = gr.Button(value="",icon=SUBMIT_BTN_ICON, min_width=0, scale=1)
                    file_upload_btn = gr.UploadButton("📁", file_types=["images", "video", "audio"], min_width=0, scale=1)
                clear_btn = (gr.Button(value="Clear all", min_width=0, scale=1)).click(clear_all, [msg, chatbot])


        msg.submit(bot, [msg, chatbot, model_selector], outputs=[msg, chatbot])
        submit_btn.click(bo, [msg, chatbot, model_selector], outputs=[msg, chatbot])


    demo.launch()

if __name__ == '__main__':
    main()
