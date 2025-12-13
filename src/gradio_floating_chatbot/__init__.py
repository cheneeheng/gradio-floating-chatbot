import time
import uuid

import gradio as gr


__all__ = ["FloatingChatbot"]


class FloatingChatbot:
    """
    A floating chatbot component for Gradio apps.
    This component overlays the UI without altering the layout of underlying components.
    It can be collapsed into an icon, supports multiple instances, and can be closed
    with the Esc key or a close button.
    """

    _css_injected = set()

    def __init__(
        self,
        label: str = "Floating Chatbot",
        value: list[dict[str, str | None]] | None = None,
        icon_position: str = "bottom-right",
        collapsed: bool = True,
        height: int = 400,
        elem_id: str | None = None,
    ):
        """
        Initializes the FloatingChatbot.

        Args:
            label (str): The label for the chatbot window header.
            value (list[dict[str, str | None]] | None): The initial conversation history.
            icon_position (str): The position of the chatbot icon ('bottom-right' or 'top-left').
            collapsed (bool): Whether the chatbot is initially collapsed.
            height (int): The height of the chatbot window in pixels.
            elem_id (str | None): A unique ID for the component. If None, one is generated.
        """
        self.label = label
        self.value = value or []
        self.icon_position = icon_position
        self.height = height
        self.elem_id = elem_id or f"floating-chatbot-{uuid.uuid4()}"

        # Inject CSS once per Blocks instance
        blocks_instance = gr.Blocks.get_instances()[-1]
        if blocks_instance.app_id not in FloatingChatbot._css_injected:
            blocks_instance.head = (
                blocks_instance.head or ""
            ) + self._get_css()
            FloatingChatbot._css_injected.add(blocks_instance.app_id)

        self._render(initial_collapsed=collapsed)

    def _get_css(self) -> str:
        """Returns the CSS for styling the floating chatbot."""
        return """
<style>
.floating-chatbot-container {
    position: fixed !important;
    z-index: 1000;
    transition: all 0.3s ease-in-out;
}
.floating-chatbot-container.bottom-right {
    bottom: 20px;
    right: 20px;
}
.floating-chatbot-container.top-left {
    top: 20px;
    left: 20px;
}
.chatbot-window-wrapper {
    width: 350px;
    border-radius: 10px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background-color: white;
    transition: opacity 0.3s ease-in-out;
}
.chatbot-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 10px;
    background-color: #f1f1f1;
}
.chatbot-header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: bold;
}
.floating-chatbot-container .close-button {
    min-width: unset !important;
    padding: 0 !important;
    width: 24px;
    height: 24px;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}
.floating-chatbot-container .icon-button {
    border-radius: 50% !important;
    width: 60px;
    height: 60px;
    font-size: 24px;
    line-height: 1;
    transition: opacity 0.3s ease-in-out;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,0.2);
}
.floating-chatbot-container .icon-button:focus {
    outline: none;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,0.2);
}
/* Remove focus border from layout elements */
.floating-chatbot-container:focus,
.floating-chatbot-container:focus-within,
.icon-wrapper:focus,
.icon-wrapper:focus-within,
.window-wrapper:focus,
.window-wrapper:focus-within {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}
</style>
"""

    def _render(self, initial_collapsed: bool):
        """Creates the Gradio components for the chatbot."""
        is_collapsed = gr.State(initial_collapsed)

        with gr.Group(
            elem_id=self.elem_id,
            elem_classes=["floating-chatbot-container", self.icon_position],
        ):
            with gr.Column(
                visible=initial_collapsed, elem_classes=["icon-wrapper"]
            ) as icon_wrapper:
                icon_button = gr.Button("💬", elem_classes=["icon-button"])

            with gr.Column(
                visible=not initial_collapsed, elem_classes=["window-wrapper"]
            ) as window_wrapper:
                with gr.Column(
                    elem_classes=["chatbot-window-wrapper"],
                ):
                    with gr.Row(elem_classes=["chatbot-header"]):
                        gr.Markdown(f"### {self.label}")
                        close_button = gr.Button(
                            "❌", elem_classes=["close-button"]
                        )

                    chatbot_component = gr.Chatbot(
                        self.value,
                        elem_id=f"{self.elem_id}-chatbot",
                        height=self.height - 100,
                    )

                    with gr.Row():
                        txt = gr.Textbox(
                            scale=4,
                            show_label=False,
                            placeholder="Enter text and press enter",
                            container=False,
                        )

        def toggle_visibility(is_collapsed_val: bool) -> tuple:
            return (
                gr.update(visible=is_collapsed_val),
                gr.update(visible=not is_collapsed_val),
                not is_collapsed_val,
            )

        icon_button.click(
            toggle_visibility,
            [is_collapsed],
            [icon_wrapper, window_wrapper, is_collapsed],
        )
        close_button.click(
            toggle_visibility,
            [is_collapsed],
            [icon_wrapper, window_wrapper, is_collapsed],
        )

        txt.submit(
            self._add_message,
            [chatbot_component, txt],
            [chatbot_component, txt],
        ).then(self._bot_response, chatbot_component, chatbot_component)

    def _add_message(
        self, history: list[dict[str, str | None]], message: str
    ) -> tuple[list[dict[str, str | None]], str]:
        """Adds a user message to the chat history."""
        if not message:
            return history, ""
        history.append({"role": "user", "content": message})
        return history, ""

    def _bot_response(self, history: list[dict[str, str | None]]):
        """Generates a streaming bot response."""
        response = "I am a floating chatbot."
        history.append({"role": "assistant", "content": ""})
        for character in response:
            history[-1]["content"] = (history[-1]["content"] or "") + character
            time.sleep(0.05)
            yield history

    @staticmethod
    def get_global_js(all_chatbot_ids: list[str]) -> str:
        """
        Returns a JavaScript string to handle global events like the Escape key.
        This script adds a single event listener to the document to control all
        chatbot instances.
        """
        esc_listener_js = (
            """
document.addEventListener('keydown', function(e) {
    if (e.key === "Escape") {
        const chatbot_ids = """
            + str(all_chatbot_ids)
            + """;
        chatbot_ids.forEach(id => {
                const container = document.getElementById(id);
                if (!container) return;
                const window_wrapper = container.querySelector('.window-wrapper');
                // Gradio hides the parent of the component
                if (window_wrapper && window_wrapper.parentElement && !window_wrapper.parentElement.classList.contains('hidden')) {
                    const close_button = window_wrapper.querySelector('.close-button');
                    if (close_button) {
                        close_button.click();
                    }
                }
            });
        }
    });
    """
        )
        return f"<script>{esc_listener_js}</script>"
