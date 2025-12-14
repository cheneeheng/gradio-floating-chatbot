import gradio as gr
import pandas as pd

from gradio_floating_chatbot import (
    add_floating_chatbot,
    default_css,
    default_css_class_names,
    sample_chatbot_response,
)


with gr.Blocks(css=default_css) as demo:
    gr.Textbox(lines=20, label="Textbox 0")
    with gr.Row():
        with gr.Column():
            add_floating_chatbot(
                anchor_factory=lambda: gr.Textbox(lines=10, label="Textbox 1"),
                response_fn=sample_chatbot_response,
                title="Chatbot 1",
                **default_css_class_names,
            )
        with gr.Column(elem_classes="gfc-container"):
            with gr.Group(elem_classes="gfc-group"):
                add_floating_chatbot(
                    anchor_factory=lambda: gr.Textbox(
                        lines=10, label="Textbox 2"
                    ),
                    response_fn=sample_chatbot_response,
                    title="Chatbot 2",
                    **default_css_class_names,
                )

                add_floating_chatbot(
                    anchor_factory=lambda: gr.Textbox(
                        lines=10, label="Textbox 3"
                    ),
                    response_fn=sample_chatbot_response,
                    title="Chatbot 3",
                    **default_css_class_names,
                )
            add_floating_chatbot(
                anchor_factory=lambda: gr.Dataframe(
                    pd.DataFrame(
                        {"id": list(range(10)), "desc": ["apple"] * 10}
                    ),
                    label="DataFrame",
                ),
                response_fn=sample_chatbot_response,
                title="Chatbot 4",
                **default_css_class_names,
            )

demo.launch()
