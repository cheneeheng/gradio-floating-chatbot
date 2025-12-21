__all__ = [
    "default_css",
    "default_css_class_names",
]

default_css = """
.gfc-container {
  position: relative; /* parent must be relative for float btn in local mode */
}

/* For global anchoring */
.gfc-fixed {
  position: fixed !important;
  /* z-index needs to be high to float above everything */
  z-index: 99999 !important;
}

.gfc-float-btn {
  position: absolute;
  bottom: 10px;
  right: 12px;
  z-index: 20001;
  width: 28px;
  height: 28px;
  padding: 0;
  font-size: 14px;
  line-height: 1;
  border-radius: 50%; /* make button round */
}

.gfc-panel {
  position: absolute;
  bottom: 10px;
  right: 12px;
  z-index: 20002;
  width: calc(50% - 12px);
  min-width: 200px;
  padding: 8px;
  border-radius: 6px;
  background: var(--block-background-fill);
  border-width: 1px !important;  /* to overwrite when used with gr.Group */
  border-style: solid;
  border-color: var(--block-border-color);
  gap: 8px !important;   /* to overwrite when used with gr.Group */
}

.gfc-panel-header {
  display: flex; /* for right aligning */
  align-items: center;
  justify-content: space-between; /* for right aligning */
}

.gfc-panel-title {
  font-weight: 600;
  font-size: 14px;
  flex-grow: 1;
}

.gfc-panel-close-btn {
  flex: 0 0 auto;   /* for right aligning */
  width: 28px;
  height: 28px;
  padding: 0;   /* for centering */
  border-radius: 4px;
  font-size: 16px;
  line-height: 1;
}

.gfc-panel-chat {
  border-width: 1px !important;  /* to overwrite when used with gr.Group */
  border-style: solid;
  border-color: var(--input-border-color);
  border-radius: 4px !important;
}

.gfc-panel-msg-txt {
  border-width: 1px !important;  /* to overwrite when used with gr.Group */
  border-style: solid;
  border-color: var(--input-border-color);
  border-radius: 4px !important;
}

.gfc-panel .form {
  border-width: 0px !important;
  border-radius: 4px !important;
}

.gfc-group {
  overflow: visible !important;
}

.gfc-group .styler {
  overflow: visible !important;
}
"""

default_css_class_names = {
    "container_class": "gfc-container",
    "float_btn_class": "gfc-float-btn",
    "panel_class": "gfc-panel",
    "panel_header_row_class": "gfc-panel-header",
    "panel_title_class": "gfc-panel-title",
    "panel_close_btn_class": "gfc-panel-close-btn",
    "panel_chat_class": "gfc-panel-chat",
    "panel_msg_txt_class": "gfc-panel-msg-txt",
}
