import pytest

from gradio_floating_chatbot import FloatingChatbot, FloatingChatbotConfig


def test_config_init_defaults():
    bot = FloatingChatbot()
    assert bot.config.anchor_mode == "local"
    assert bot.config.title == "Chatbot"
    assert bot.config.collapsed is True
    assert bot.config.use_default_css is True
    # Verify default classes are populated
    assert bot.config.container_class == "gfc-container"


def test_config_init_dataclass():
    config = FloatingChatbotConfig(title="My Bot", anchor_mode="global")
    bot = FloatingChatbot(config)
    assert bot.config.title == "My Bot"
    assert bot.config.anchor_mode == "global"
    assert bot.config.use_default_css is True


def test_config_init_dict():
    config = {"title": "Dict Bot", "anchor_mode": "global"}
    bot = FloatingChatbot(config)
    assert bot.config.title == "Dict Bot"
    assert bot.config.anchor_mode == "global"


def test_save_load_json(tmp_path):
    config = FloatingChatbotConfig(title="JSON Bot", anchor_mode="global")
    bot = FloatingChatbot(config)
    path = tmp_path / "config.json"
    bot.save_config_json(str(path))

    bot2 = FloatingChatbot()
    bot2.load_config_json(str(path))
    assert bot2.config.title == "JSON Bot"
    assert bot2.config.anchor_mode == "global"
    assert bot2.config.use_default_css is True
    assert bot2.config.container_class == "gfc-container"


def test_save_load_yaml(tmp_path):
    config = FloatingChatbotConfig(title="YAML Bot", anchor_mode="global")
    bot = FloatingChatbot(config)
    path = tmp_path / "config.yaml"
    bot.save_config_yaml(str(path))

    bot2 = FloatingChatbot()
    bot2.load_config_yaml(str(path))
    assert bot2.config.title == "YAML Bot"
    assert bot2.config.anchor_mode == "global"


def test_init_from_file(tmp_path):
    # JSON
    path_json = tmp_path / "bot.json"
    bot = FloatingChatbot({"title": "File Bot"})
    bot.save_config_json(str(path_json))

    bot2 = FloatingChatbot(str(path_json))
    assert bot2.config.title == "File Bot"

    # YAML
    path_yaml = tmp_path / "bot.yaml"
    bot.save_config_yaml(str(path_yaml))

    bot3 = FloatingChatbot(str(path_yaml))
    assert bot3.config.title == "File Bot"


def test_config_icon_type():
    # Default
    config = FloatingChatbotConfig()
    assert config.icon_type == "text"

    # Custom
    config = FloatingChatbotConfig(icon="path/to/icon.png", icon_type="image")
    assert config.icon_type == "image"
    assert config.icon == "path/to/icon.png"


def test_init_str_name():
    # If string is passed and not file, it's instance_name
    bot = FloatingChatbot("my-bot-instance")
    assert bot.config.instance_name == "my-bot-instance"


def test_kwargs_override():
    bot = FloatingChatbot(
        title="Original", anchor_mode="local", instance_name="test"
    )
    assert bot.config.title == "Original"
    assert bot.config.instance_name == "test"

    # Re-setup
    bot.setup_config(title="New Title")
    assert bot.config.title == "New Title"


def test_css_enforcement_default_success():
    # Should work fine and populate defaults
    config = FloatingChatbotConfig(use_default_css=True)
    assert config.container_class == "gfc-container"


def test_css_enforcement_default_fail():
    # Should fail if we try to set a custom class while use_default_css is True
    with pytest.raises(
        ValueError, match="Cannot set custom 'container_class'"
    ):
        FloatingChatbotConfig(
            use_default_css=True, container_class="my-container"
        )


def test_css_enforcement_custom_success():
    # Should work if we provide ALL classes
    config = FloatingChatbotConfig(
        use_default_css=False,
        container_class="c1",
        float_btn_class="c2",
        panel_class="c3",
        panel_header_row_class="c4",
        panel_title_class="c5",
        panel_close_btn_class="c6",
        panel_chat_class="c7",
        panel_msg_txt_class="c8",
    )
    assert config.container_class == "c1"


def test_css_enforcement_custom_fail():
    # Should fail if we miss one
    with pytest.raises(ValueError, match="Missing: panel_msg_txt_class"):
        FloatingChatbotConfig(
            use_default_css=False,
            container_class="c1",
            float_btn_class="c2",
            panel_class="c3",
            panel_header_row_class="c4",
            panel_title_class="c5",
            panel_close_btn_class="c6",
            panel_chat_class="c7",
            # Missing panel_msg_txt_class
        )


def test_kwargs_revalidation():
    # Test that re-validation runs if we update via setup_config/kwargs
    bot = FloatingChatbot()
    # This should fail because we are in default mode (implied) and try to set a class
    with pytest.raises(
        ValueError, match="Cannot set custom 'container_class'"
    ):
        bot.setup_config(container_class="bad-idea")
