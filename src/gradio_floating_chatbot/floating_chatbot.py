__all__ = [
    "add_floating_chatbot",
    "sample_chatbot_response",
    "default_css",
]

from typing import Callable

import gradio as gr


def add_floating_chatbot(
    anchor_factory: Callable[[], gr.Component],
    response_fn: Callable[[list[gr.ChatMessage], str], tuple[list, str]],
    container_class: str,
    float_btn_class: str,
    panel_class: str,
    panel_header_row_class: str,
    panel_title_class: str,
    panel_close_btn_class: str,
    panel_chat_class: str,
    panel_msg_txt_class: str,
    title: str = "Chatbot",
    icon: str = "💬",
    min_height: str = "180px",
    max_height: str = "50vh",
) -> tuple[
    gr.Component, gr.Button, gr.Column, gr.Chatbot, gr.Textbox, gr.Button
]:
    """
    Create a floating chatbot panel attached to an anchor component.

    This helper wraps any Gradio component (Textbox, Dataframe, Image, etc.)
    inside a container with a floating action button. Clicking the button
    reveals a themed panel containing a chatbot interface and a message input.
    The panel includes a header row with a static title and a close button.

    Args:
        anchor_factory: Callable that builds and returns the anchor component
            (e.g. lambda: gr.Textbox(...)).
        response_fn: Function that handles chatbot responses. It must accept
            (history, message) and return (updated_history, cleared_message).
        container_class: CSS class applied to the parent container. Should set
            `position: relative` so the floating panel/button can be positioned.
        float_btn_class: CSS class applied to the floating button.
        panel_class: CSS class applied to the floating panel container.
        panel_header_row_class: CSS class applied to the header row of the panel.
        panel_title_class: CSS class applied to the title element inside the header.
        panel_close_btn_class: CSS class applied to the close button inside the header.
        panel_chat_class: CSS class applied to the Chatbot component inside the panel.
        panel_msg_txt_class: CSS class applied to the Textbox message input inside the panel.
        title: Text shown as the panel title. Defaults to "Chatbot".
        icon: Emoji/text used for the floating action button. Defaults to "💬".
        min_height: Minimum height for the chatbot component. Defaults to "180px".
        max_height: Maximum height for the chatbot component. Defaults to "50vh".

    Returns:
        tuple containing:
            - anchor: the anchor component created by anchor_factory
            - float_btn: the floating action button
            - panel: the floating panel container
            - chat: the Chatbot component inside the panel
            - msg: the Textbox used for message input
            - close_btn: the close button in the panel header

    Side Effects:
        - Wires up toggle logic: clicking the floating button shows the panel,
          clicking the close button hides it.
        - Connects the message input to the provided response_fn so that
          submitted messages update the chatbot history.
    """
    # Layout ------------------------------------------------------------------
    with gr.Column(elem_classes=container_class):
        anchor = anchor_factory()
        float_btn = gr.Button(
            icon,
            elem_classes=float_btn_class,
            min_width=1,
        )

        with gr.Column(visible=False, elem_classes=panel_class) as panel:
            with gr.Row(elem_classes=panel_header_row_class):
                gr.HTML(f"<div class='{panel_title_class}'>{title}</div>")
                close_btn = gr.Button(
                    "❌",
                    min_width=1,
                    elem_classes=panel_close_btn_class,
                )
            chat = gr.Chatbot(
                type="messages",
                height=None,
                min_height=min_height,
                max_height=max_height,
                show_label=False,
                elem_classes=panel_chat_class,
            )
            msg = gr.Textbox(
                placeholder="Type a message...",
                submit_btn=True,
                show_label=False,
                elem_classes=panel_msg_txt_class,
            )

    # toggle logic ------------------------------------------------------------
    def show_panel():
        return gr.update(visible=True)

    def hide_panel():
        return gr.update(visible=False)

    float_btn.click(fn=show_panel, inputs=None, outputs=panel)
    close_btn.click(fn=hide_panel, inputs=None, outputs=panel)

    # simple chatbot response -------------------------------------------------
    msg.submit(response_fn, [chat, msg], [chat, msg])

    return anchor, float_btn, panel, chat, msg, close_btn


def sample_chatbot_response(
    history: list[gr.ChatMessage], message: str
) -> tuple[list[gr.ChatMessage], str]:
    history = history + [
        gr.ChatMessage(role="user", content=f"{message}"),
        gr.ChatMessage(role="assistant", content=f"Echo: {message}"),
    ]
    return history, ""
