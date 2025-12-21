import gradio as gr

from gradio_floating_chatbot import (
    FloatingChatbot,
    FloatingChatbotConfig,
    default_css,
    sample_chatbot_response,
)


# Custom CSS for the second example
custom_css = """
.my-container { position: relative; }
.my-btn { position: absolute; bottom: 50px; left: 20px; font-size: 24px; }
.my-panel { position: absolute; bottom: 100px; left: 20px; width: 300px; background: #eee; padding: 10px; border: 2px solid blue; }
.my-header { display: flex; justify-content: space-between; font-weight: bold; }
.my-title { color: blue; }
.my-close { color: red; cursor: pointer; }
.my-chat { height: 200px; overflow-y: auto; background: white; }
.my-msg { margin-top: 10px; }
"""  # noqa: E501

# Combine default and custom CSS for the demo
full_css = default_css + "\n" + custom_css

with gr.Blocks(css=full_css) as demo:
    gr.Markdown("# Floating Chatbot Demo")
    gr.Textbox(lines=5, label="Textbox 0")

    with gr.Row():
        with gr.Column(elem_classes="gfc-container"):
            # 1. Standard Usage (Uses Default CSS)
            # We don't specify classes, so it enforces defaults.
            config = FloatingChatbotConfig(
                title="Standard Bot",
                anchor_mode="local",
                instance_name="bot-standard",
            )
            bot1 = FloatingChatbot(config)
            bot1.create_layout(
                anchor_factory=lambda: gr.Textbox(lines=5, label="Anchor 1")
            )
            bot1.define_events(sample_chatbot_response)

        with gr.Column():
            # 2. Custom CSS Usage
            # We set use_default_css=False and MUST provide all classes.
            custom_config = FloatingChatbotConfig(
                title="Custom Bot",
                anchor_mode="local",
                instance_name="bot-custom",
                use_default_css=False,
                container_class="my-container",
                float_btn_class="my-btn",
                panel_class="my-panel",
                panel_header_row_class="my-header",
                panel_title_class="my-title",
                panel_close_btn_class="my-close",
                panel_chat_class="my-chat",
                panel_msg_txt_class="my-msg",
            )

            bot2 = FloatingChatbot(custom_config)
            bot2.create_layout(
                anchor_factory=lambda: gr.Textbox(
                    lines=5, label="Anchor 2 (Custom)"
                )
            )
            bot2.define_events(sample_chatbot_response)

    # Global Chatbot (Fixed Position)
    gr.Markdown("## Global Chatbot is active! Check the bottom right.")

    global_config = FloatingChatbotConfig(
        title="Global Bot", anchor_mode="global", instance_name="global-bot"
    )

    global_bot = FloatingChatbot(global_config)
    global_bot.create_layout()
    global_bot.define_events(sample_chatbot_response)

demo.launch()
