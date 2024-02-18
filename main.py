import gradio
import gradio as gr
import os
import dotenv
import apitest
dotenv.load_dotenv()


def main():

    demo = gr.Interface(apitest.api_test, inputs=["text", gradio.Dropdown(choices=["gpt-4-turbo", "gpt-4","gpt-4V"])], outputs="text", theme="NoCrypt/miku", title="chat_demo")
    demo.launch(share=False,favicon_path="./favicon.ico")
    print(os.getenv("HTTP_PROXY"))

if __name__ == '__main__':
    main()

