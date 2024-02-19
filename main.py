import gradio as gr
import os
import dotenv
import gradio_multimodalchatbot

import apitest
dotenv.load_dotenv()
import chat_channel


def main():
    my_chatbot = gr.Chatbot(
            show_copy_button=True,
            avatar_images=("https://cdn-icons-png.flaticon.com/512/4472/4472507.png",
                           "https://cdn-icons-png.flaticon.com/512/3662/3662817.png"
                           ),

        )
    print(my_chatbot.get_block_name())
    # demo = gr.ChatInterface(
    #     chat_channel.chat,
    #     chatbot=my_chatbot,
    #     textbox=gr.Textbox(
    #         placeholder=""
    #     ),
    #     additional_inputs=[gr.Dropdown(label="model", choices=["gpt-4-all", "gpt-4-vision-preview", "gpt-4-turbo", "gpt-4", "gpt-4V"])],
    #     theme="NoCrypt/miku",
    #     title="chat_demo"
    # ).launch(share=False, favicon_path="./favicon.ico")
    with gr.Blocks() as demo:
        chatbot =gr.Chatbot(
            [],
            elem_id="chatbot",
            bubble_full_width=False,
            show_copy_button=True,
            avatar_images=("https://cdn-icons-png.flaticon.com/512/4472/4472507.png",
                           "https://cdn-icons-png.flaticon.com/512/3662/3662817.png"
                           ),

        )
        with gr.Row():
            txt = gr.Textbox(
                placeholder=""
            )
            btn = gr.UploadButton("📁", file_types=["images", "vedio", "audio"])
        txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(chatbot, )
    demo.launch()

if __name__ == '__main__':
    main()
