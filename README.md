# gradio-floating-chatbot

A flexible, floating chatbot component for Gradio applications.

> [!NOTE]
> This component's implementation was mainly done with **Gemini CLI**, and the planning was conducted with **Microsoft Copilot**.

## Features

- **Floating UI**: Collapsible chatbot window that floats over your content.
- **Anchoring Modes**:
  - **Local**: Attached to a specific component (relative positioning).
  - **Global**: Fixed to the viewport (floats over everything).
- **Configuration**:
  - Class-based architecture.
  - Configurable via `dataclass`, Dictionary, JSON, or YAML.
  - Persistence support (save/load configs).
- **Multiple Instances**: Support for multiple independent chatbots on the same page.

## Requirements

- **Python**: >= 3.12
- **Gradio**: >= 6.2.0

## Installation

```bash
pip install gradio-floating-chatbot
# or
uv add gradio-floating-chatbot
```

## Usage

### Basic Usage (Local Anchor)

```python
import gradio as gr
from gradio_floating_chatbot import FloatingChatbot, FloatingChatbotConfig, sample_chatbot_response, default_css

with gr.Blocks(css=default_css) as demo:

    # 1. Create Config
    config = FloatingChatbotConfig(
        title="My Assistant",
        anchor_mode="local",
        instance_name="assistant1"
    )

    # 2. Initialize Bot
    bot = FloatingChatbot(config)

    # 3. Create Layout
    # anchor_factory creates the component that the bot is attached to
    bot.create_layout(
        anchor_factory=lambda: gr.Textbox(label="Main Content")
    )

    # 4. Define Events
    bot.define_events(sample_chatbot_response)

demo.launch()
```

### Global Anchoring

To make the chatbot float fixed on the screen (regardless of scroll):

```python
config = FloatingChatbotConfig(
    title="Global Bot",
    anchor_mode="global"
)
bot = FloatingChatbot(config)

# No anchor_factory needed for global mode
bot.create_layout()

bot.define_events(sample_chatbot_response)
```

### JSON/YAML Configuration

You can load configuration from external files:

```python
# Load from JSON
bot = FloatingChatbot("config.json")

# Load from YAML
bot = FloatingChatbot("config.yaml")

# Save config
bot.save_config_json("my_config.json")
```

**Example `config.yaml`:**

```yaml
instance_name: "support-bot"
title: "Support Agent"
anchor_mode: "global"
collapsed: true
min_height: "300px"
```

### Image Icon Example

```python
config = FloatingChatbotConfig(
    icon="https://example.com/bot-icon.png",
    icon_type="image"
)
bot = FloatingChatbot(config)
```

## Configuration Options (`FloatingChatbotConfig`)

| Field           | Type                  | Default   | Description                                  |
| --------------- | --------------------- | --------- | -------------------------------------------- |
| `instance_name` | `str`                 | UUID      | Unique ID for the instance.                  |
| `title`         | `str`                 | "Chatbot" | Title shown in the header.                   |
| `anchor_mode`   | `"local" \| "global"` | "local"   | Positioning mode.                            |
| `collapsed`     | `bool`                | `True`    | Initial state.                               |
| `icon`          | `str`                 | "💬"      | Icon for the floating button (text or path). |
| `icon_type`     | `"text" \| "image"`   | "text"    | Type of icon (text or image).                |
| `min_height`    | `str`                 | "180px"   | Minimum height of chat window.               |
