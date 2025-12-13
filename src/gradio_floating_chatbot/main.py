import gradio as gr

from gradio_floating_chatbot import FloatingChatbot


def main():
    """
    Main function to launch the Gradio demo application.
    """
    with gr.Blocks(analytics_enabled=False) as app:
        gr.Markdown("# Floating Chatbot Demo")
        gr.Markdown(
            "This is the main UI. The chatbots should float over it without affecting the layout."
        )

        with gr.Row():
            gr.Button("Button 1")
            gr.Button("Button 2")

        # Instantiate the floating chatbots
        chatbot1 = FloatingChatbot(
            label="Assistant 1", icon_position="bottom-right"
        )
        chatbot2 = FloatingChatbot(
            label="Assistant 2", icon_position="top-left"
        )

        gr.Slider(label="A slider")

        # Add global JS for ESC key handling after all chatbots are created
        all_ids = [chatbot1.elem_id, chatbot2.elem_id]
        app.head = (app.head or "") + FloatingChatbot.get_global_js(all_ids)

    app.launch()


if __name__ == "__main__":
    main()
