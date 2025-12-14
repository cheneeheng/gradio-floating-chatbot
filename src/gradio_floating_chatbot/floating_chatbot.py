import gradio as gr
import pandas as pd


with gr.Blocks(
    css="""
.container {
  position: relative; /* parent must be relative */
}

.float-btn {
  position: absolute;
  bottom: 12px;
  right: 12px;
  z-index: 20001;
  width: 28px;
  height: 28px;
  padding: 0;
  font-size: 14px;
  line-height: 1;
  border-radius: 50%;
}

.floating-panel {
  position: absolute;
  bottom: 12px;
  right: 12px;
  z-index: 20002;
  width: calc(50% - 12px);
  min-width: 200px;  /* never smaller than 200px */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

#special-group {
  overflow: visible !important;
}

#special-group .styler {
  overflow: visible !important;
}


"""
) as demo:
    gr.Textbox(lines=50, label="Textbox 0")
    with gr.Row():
        # First textbox + floating button + floating panel
        with gr.Column(elem_classes="container"):
            txt1 = gr.Textbox(lines=10, label="Textbox 1")
            float_btn1 = gr.Button("⚡", elem_classes="float-btn", min_width=1)
            with gr.Column(
                visible=False, elem_classes="floating-panel"
            ) as panel1:
                gr.Markdown("### Chatbot 1")
                chat1 = gr.Chatbot(
                    type="messages",
                    height=None,
                    min_height="180px",
                    max_height="50vh",
                )
                msg1 = gr.Textbox(
                    placeholder="Type a message...", submit_btn=True
                )
                close_btn1 = gr.Button("Close")

        with gr.Column(elem_classes="container"):
            with gr.Group(elem_id="special-group"):
                with gr.Row():
                    with gr.Column(elem_classes="container"):
                        # Second textbox + floating button + floating panel
                        txt2 = gr.Textbox(lines=10, label="Textbox 2")
                        float_btn2 = gr.Button(
                            "💬", elem_classes="float-btn", min_width=1
                        )
                        with gr.Column(
                            visible=False, elem_classes="floating-panel"
                        ) as panel2:
                            gr.Markdown("### Chatbot 2")
                            chat2 = gr.Chatbot(
                                type="messages",
                                height=None,
                                min_height="180px",
                                max_height="50vh",
                            )
                            msg2 = gr.Textbox(
                                placeholder="Type a message...",
                                submit_btn=True,
                            )
                            close_btn2 = gr.Button("Close")

                with gr.Row():
                    with gr.Column(elem_classes="container"):
                        # Third textbox + floating button
                        txt3 = gr.Textbox(lines=10, label="Textbox 3")
                        float_btn3 = gr.Button(
                            "❄️", elem_classes="float-btn", min_width=1
                        )
                        with gr.Column(
                            visible=False, elem_classes="floating-panel"
                        ) as panel3:
                            gr.Markdown("### Chatbot 3")
                            chat3 = gr.Chatbot(
                                type="messages",
                                height=None,
                                min_height="180px",
                                max_height="50vh",
                            )
                            msg3 = gr.Textbox(
                                placeholder="Type a message...",
                                submit_btn=True,
                            )
                            close_btn3 = gr.Button("Close")

            # DataFrame + floating button
            df = gr.Dataframe(
                pd.DataFrame({"id": list(range(10)), "desc": ["apple"] * 10}),
                label="DataFrame",
            )
            float_btn4 = gr.Button("⭐", elem_classes="float-btn", min_width=1)
            with gr.Column(
                visible=False, elem_classes="floating-panel"
            ) as panel4:
                gr.Markdown("### Chatbot 4")
                chat4 = gr.Chatbot(
                    type="messages",
                    height=None,
                    min_height="180px",
                    max_height="50vh",
                )
                msg4 = gr.Textbox(
                    placeholder="Type a message...", submit_btn=True
                )
                close_btn4 = gr.Button("Close")

    # toggle logic
    def show_panel():
        return gr.update(visible=True)

    def hide_panel():
        return gr.update(visible=False)

    float_btn1.click(show_panel, None, panel1)
    close_btn1.click(hide_panel, None, panel1)

    float_btn2.click(show_panel, None, panel2)
    close_btn2.click(hide_panel, None, panel2)

    float_btn3.click(show_panel, None, panel3)
    close_btn3.click(hide_panel, None, panel3)

    float_btn4.click(show_panel, None, panel4)
    close_btn4.click(hide_panel, None, panel4)

    # simple chatbot response function
    def respond(history, message):
        history = history + [
            gr.ChatMessage(role="user", content=f"{message}"),
            gr.ChatMessage(role="assistant", content=f"Echo: {message}"),
        ]
        return history, ""

    # wire up each chatbot
    msg1.submit(respond, [chat1, msg1], [chat1, msg1])
    msg2.submit(respond, [chat2, msg2], [chat2, msg2])
    msg3.submit(respond, [chat3, msg3], [chat3, msg3])
    msg4.submit(respond, [chat4, msg4], [chat4, msg4])

demo.launch()
