import gradio as gr
import pytest
from gradio_floating_chatbot import (
    FloatingChatbot,
    FloatingChatbotConfig,
    sample_chatbot_response,
)


def test_layout_local():
    config = FloatingChatbotConfig(anchor_mode="local")
    bot = FloatingChatbot(config)

    with gr.Blocks():
        components = bot.create_layout(lambda: gr.Textbox("Anchor"))
        bot.define_events(lambda h, m: (h, ""))

    # Check container class
    assert "gfc-container" in components["container"].elem_classes
    assert "gfc-float-btn" in components["float_btn"].elem_classes
    # Should NOT have gfc-fixed
    # elem_classes is list of strings
    assert not any(
        "gfc-fixed" in c for c in components["float_btn"].elem_classes
    )
    assert components["anchor"] is not None


def test_layout_global():
    config = FloatingChatbotConfig(anchor_mode="global")
    bot = FloatingChatbot(config)

    with gr.Blocks():
        # No anchor factory needed
        components = bot.create_layout()
        bot.define_events(lambda h, m: (h, ""))

    assert any(
        "gfc-global-anchor" in c for c in components["container"].elem_classes
    )
    assert any("gfc-fixed" in c for c in components["float_btn"].elem_classes)
    assert any("gfc-fixed" in c for c in components["panel"].elem_classes)
    assert components["anchor"] is None


def test_layout_image_icon():
    config = FloatingChatbotConfig(icon="path/to/icon.png", icon_type="image")
    bot = FloatingChatbot(config)
    with gr.Blocks():
        components = bot.create_layout()

    # When icon_type is image, button value should be empty string
    assert components["float_btn"].value == ""


def test_define_events_before_layout():
    bot = FloatingChatbot()
    with pytest.raises(RuntimeError, match="Components not initialized"):
        bot.define_events(lambda h, m: (h, ""))


def test_define_events_wiring():
    # Smoke test to ensure define_events doesn't crash and sets up click handlers
    bot = FloatingChatbot()
    with gr.Blocks():
        components = bot.create_layout(lambda: gr.Textbox("A"))
        bot.define_events(lambda h, m: (h, ""))

    assert bot.panel_id is not None


def test_sample_chatbot_response():
    history = []
    message = "Hello"
    new_history, cleared_msg = sample_chatbot_response(history, message)

    assert len(new_history) == 2
    assert new_history[0].role == "user"
    assert new_history[0].content == "Hello"
    assert new_history[1].role == "assistant"
    assert new_history[1].content == "Echo: Hello"
    assert cleared_msg == ""


def test_toggle_functions():
    # Test the static methods directly
    update_show = FloatingChatbot._show_panel(None)
    assert update_show["visible"] is True

    update_hide = FloatingChatbot._hide_panel(None)
    assert update_hide["visible"] is False
