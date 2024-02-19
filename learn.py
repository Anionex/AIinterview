import gradio as gr
import os
import dotenv
import gradio_multimodalchatbot

import apitest
dotenv.load_dotenv()
import chat_channel


def main():

    with gr.Blocks() as demo:
        model_selector = gr.Dropdown(label="model", choices=["gpt-4-0125-preview", "gpt-4-all", "gpt-4-vision-preview", "gpt-4-turbo", "gpt-4V"])
        chatbot = gr.Chatbot()
        with gr.Row():
            msg = gr.Textbox(min_width=50000)
            submit_btn = msg.submit(chat_channel.chat, [msg, chatbot, model_selector], outputs=[msg, chatbot])

            btn = gr.Button(value="Submit", size="sm")
            btn.click(chat_channel.chat, [msg, chatbot, model_selector],  outputs=[msg, chatbot])
            clear_btn = gr.ClearButton([msg, chatbot], size="sm")




    demo.launch()

if __name__ == '__main__':
    main()
