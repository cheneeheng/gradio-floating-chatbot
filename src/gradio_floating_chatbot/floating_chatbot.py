__all__ = [
    "FloatingChatbot",
    "FloatingChatbotConfig",
    "sample_chatbot_response",
]

import json
import uuid
from dataclasses import asdict, dataclass, field
from typing import Callable, Literal

import gradio as gr
import yaml

from .css import default_css_class_names


@dataclass
class FloatingChatbotConfig:
    # Core config
    instance_name: str = field(
        default_factory=lambda: f"bot-{uuid.uuid4().hex[:8]}"
    )
    anchor_mode: Literal["global", "local"] = "local"
    collapsed: bool = True

    # CSS Mode
    use_default_css: bool = True

    # UI Text/Icons
    title: str = "Chatbot"
    icon: str = "💬"
    icon_type: Literal["text", "image"] = "text"

    # Dimensions
    min_height: str = "180px"
    max_height: str = "50vh"

    # CSS Classes (Default to None to allow validation logic)
    container_class: str | None = None
    float_btn_class: str | None = None
    panel_class: str | None = None
    panel_header_row_class: str | None = None
    panel_title_class: str | None = None
    panel_close_btn_class: str | None = None
    panel_chat_class: str | None = None
    panel_msg_txt_class: str | None = None

    def __post_init__(self):
        css_fields = [
            "container_class",
            "float_btn_class",
            "panel_class",
            "panel_header_row_class",
            "panel_title_class",
            "panel_close_btn_class",
            "panel_chat_class",
            "panel_msg_txt_class",
        ]

        if self.use_default_css:
            for field_name in css_fields:
                current_value = getattr(self, field_name)
                default_value = default_css_class_names[field_name]

                if current_value is not None:
                    # If value is present, it MUST match the default
                    if current_value != default_value:
                        raise ValueError(
                            f"Cannot set custom '{field_name}' ('{current_value}') when 'use_default_css' is True. "
                            f"Expected default '{default_value}' or None. "
                            "Set 'use_default_css=False' if you want to use custom classes."
                        )
                else:
                    # Apply defaults if None
                    setattr(self, field_name, default_value)
        else:
            # Enforce that ALL custom classes are provided
            missing_fields = [
                f for f in css_fields if getattr(self, f) is None
            ]
            if missing_fields:
                raise ValueError(
                    f"When 'use_default_css' is False, you must provide values for all CSS classes. "
                    f"Missing: {', '.join(missing_fields)}"
                )

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class FloatingChatbot:
    def __init__(
        self,
        config: FloatingChatbotConfig | dict | str | None = None,
        **kwargs,
    ):
        self.setup_config(config, **kwargs)
        self.components = {}
        self.panel_id = None

    def setup_config(
        self,
        config: FloatingChatbotConfig | dict | str | None = None,
        **kwargs,
    ):
        if isinstance(config, FloatingChatbotConfig):
            self.config = config
        elif isinstance(config, dict):
            self.config = FloatingChatbotConfig(**config)
        elif isinstance(config, str):
            # Check if file path
            if config.endswith(".json"):
                self.load_config_json(config)
            elif config.endswith(".yaml") or config.endswith(".yml"):
                self.load_config_yaml(config)
            else:
                self.config = FloatingChatbotConfig(instance_name=config)
        else:
            self.config = FloatingChatbotConfig()

        # Override with kwargs if provided
        # Note: If kwargs try to set CSS classes while use_default_css is True (default),
        # the dataclass logic isn't automatically re-triggered unless we re-create it
        # or manually validate.
        # Ideally, we should update the config object and then re-validate.

        for k, v in kwargs.items():
            if hasattr(self.config, k):
                setattr(self.config, k, v)

        # Re-run validation logic manually if needed, or rely on the user passing correct config initially.
        # Since __post_init__ runs only on creation, simply setting attributes doesn't trigger it.
        # However, for simplicity and robustness, we can just instantiate a new config if kwargs are heavy,
        # but here we simply trust the initial creation or re-verify if strictness is required.
        # Given the "Strict enforcement" requirement, let's re-validate if we modified it.
        if kwargs:
            # Quick re-validation hack: re-run logic
            self.config.__post_init__()

    def save_config_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.config.to_dict(), f, indent=2)

    def load_config_json(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)
        self.config = FloatingChatbotConfig.from_dict(data)

    def save_config_yaml(self, path: str):
        with open(path, "w") as f:
            yaml.dump(self.config.to_dict(), f)

    def load_config_yaml(self, path: str):
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        self.config = FloatingChatbotConfig.from_dict(data)

    def create_layout(
        self, anchor_factory: Callable[[], gr.Component] | None = None
    ):
        # Determine CSS classes based on anchor_mode
        container_cls = self.config.container_class

        if self.config.anchor_mode == "global":
            container_cls = f"{container_cls} gfc-global-anchor"

        self.panel_id = (
            f"gfc-{self.config.instance_name}-{uuid.uuid4().hex[:4]}"
        )

        with gr.Column(elem_classes=container_cls) as container:
            anchor = None
            if anchor_factory and self.config.anchor_mode == "local":
                anchor = anchor_factory()

            # Button Class
            btn_cls = self.config.float_btn_class or ""
            if self.config.anchor_mode == "global":
                btn_cls += " gfc-fixed"

            if self.config.icon_type == "image":
                float_btn = gr.Button(
                    "",
                    icon=self.config.icon,
                    elem_classes=btn_cls,
                    min_width=1,
                )
            else:
                float_btn = gr.Button(
                    self.config.icon,
                    elem_classes=btn_cls,
                    min_width=1,
                )

            # Panel Class
            pnl_cls = self.config.panel_class or ""
            if self.config.anchor_mode == "global":
                pnl_cls += " gfc-fixed"

            with gr.Column(
                visible=not self.config.collapsed,
                elem_classes=pnl_cls,
                elem_id=self.panel_id,
            ) as panel:
                with gr.Row(elem_classes=self.config.panel_header_row_class):
                    gr.HTML(
                        f"<div class='{self.config.panel_title_class}'>{self.config.title}</div>",
                        padding=True,
                    )
                    close_btn = gr.Button(
                        "❌",
                        min_width=1,
                        elem_classes=self.config.panel_close_btn_class,
                    )
                chat = gr.Chatbot(
                    type="messages",
                    height=None,
                    min_height=self.config.min_height,
                    max_height=self.config.max_height,
                    show_label=False,
                    elem_classes=self.config.panel_chat_class,
                    allow_tags=False,
                )
                msg = gr.Textbox(
                    placeholder="Type a message...",
                    submit_btn=True,
                    show_label=False,
                    elem_classes=self.config.panel_msg_txt_class,
                )

        self.components = {
            "anchor": anchor,
            "float_btn": float_btn,
            "panel": panel,
            "chat": chat,
            "msg": msg,
            "close_btn": close_btn,
            "container": container,
        }

        return self.components

    @staticmethod
    def _show_panel(_):
        return gr.update(visible=True)

    @staticmethod
    def _hide_panel(_):
        return gr.update(visible=False)

    def define_events(
        self,
        response_fn: Callable[[list[gr.ChatMessage], str], tuple[list, str]],
    ):
        if not self.components:
            raise RuntimeError(
                "Components not initialized. Call create_layout() first."
            )

        # This hidden textbox is used to pass the panel's ID to the JS functions
        # without creating a circular input/output dependency on the panel itself.
        panel_id_carrier = gr.Textbox(
            value=self.panel_id, visible=False, container=False
        )

        # JS for opening the panel and adding the Esc listener
        js_open_panel = f"""
    (panelId) => {{
      // Initialize a global stack to track the order of opened panels (LIFO)
      if (!window.gfcOpenPanelStack) {{
        window.gfcOpenPanelStack = [];
      }}

      // Add the panel's ID to the stack if it's not already there
      if (!window.gfcOpenPanelStack.includes(panelId)) {{
        window.gfcOpenPanelStack.push(panelId);
      }}

      // Add the global Esc key listener only once
      if (!window.gfcEscListenerAttached) {{
        document.addEventListener("keydown", (e) => {{
          if (e.key === "Escape" && window.gfcOpenPanelStack.length > 0) {{
            // Get the ID of the last opened panel without removing it from the stack
            const lastPanelId = window.gfcOpenPanelStack[window.gfcOpenPanelStack.length - 1];
            if (lastPanelId) {{
              const panelToClose = document.getElementById(lastPanelId);
              if (panelToClose) {{
                // Find and click the close button within that specific panel
                const closeButton = panelToClose.querySelector(".{self.config.panel_close_btn_class}");
                if (closeButton) {{
                  closeButton.dispatchEvent(new MouseEvent('click', {{ bubbles: true, cancelable: true, view: window }}));
                  // Blur the active element to prevent focus highlight on the float btn
                  if(document.activeElement) {{
                    document.activeElement.blur();
                  }}
                }}
              }}
            }}
          }}
        }});
        window.gfcEscListenerAttached = true;
      }}

      // Return the panelId to trigger the Python `show_panel` function
      return [panelId];
    }}
    """  # noqa: E501

        # JS for handling the close button click
        js_close_panel = """
    (panelId) => {
      // Ensure the stack exists
      if (!window.gfcOpenPanelStack) {
        window.gfcOpenPanelStack = [];
      }

      // Remove the panel's ID from the stack upon closing
      const index = window.gfcOpenPanelStack.indexOf(panelId);
      if (index > -1) {
        window.gfcOpenPanelStack.splice(index, 1);
      }

      // Return the panelId to trigger the Python `hide_panel` function
      return [panelId];
    }
    """

        float_btn = self.components["float_btn"]
        panel = self.components["panel"]
        close_btn = self.components["close_btn"]
        msg = self.components["msg"]
        chat = self.components["chat"]

        float_btn.click(
            fn=self._show_panel,
            inputs=[panel_id_carrier],
            outputs=[panel],
            js=js_open_panel,
        )
        close_btn.click(
            fn=self._hide_panel,
            inputs=[panel_id_carrier],
            outputs=[panel],
            js=js_close_panel,
        )

        # simple chatbot response -------------------------------------------------
        msg.submit(response_fn, [chat, msg], [chat, msg])


def sample_chatbot_response(
    history: list[gr.ChatMessage], message: str
) -> tuple[list[gr.ChatMessage], str]:
    history = history + [
        gr.ChatMessage(role="user", content=f"{message}"),
        gr.ChatMessage(role="assistant", content=f"Echo: {message}"),
    ]
    return history, ""
