# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-03

### Breaking Changes
- **Python Requirement**: This library now requires Python 3.12 or newer.
- **Gradio Requirement**: Support has been updated for Gradio 6.2.0. Older versions of Gradio are no longer supported.

### Fixed
- **Panel Visibility**: Fixed a visual issue where the chatbot's border would remain visible even when the chat window was closed or toggled off. The panel now hides completely as expected.

### Changed
- **Compatibility**: Internal updates to ensure seamless integration with the latest Gradio 6.x ecosystem.

## [0.0.2] - 2025-12-18

### Added
- **Global Anchoring**: Support for `anchor_mode="global"`, allowing the chatbot to float fixed on the viewport over all content.
- **FloatingChatbotConfig**: A dataclass for type-safe configuration management.
- **Persistence**: Methods to load and save configurations from JSON and YAML files.
- **Accessibility**: Global `Esc` key support to close chatbot panels (handles multiple panels in LIFO order).
- **Multiple Instance Support**: Robust support for multiple independent chatbot instances on the same page via UUID generation.
- **CI/CD Pipeline**: GitHub Actions workflow (`.github/workflows/release.yml`) for automated testing and publishing to PyPI.
- **Initial Test Suite**: Comprehensive tests in `tests/` covering configuration validation and layout logic.

### Changed
- **Architecture Refactor**: Transitioned from functional `add_floating_chatbot` to a class-based `FloatingChatbot` design for better state management and extensibility.
- **Modularization**: Separated CSS logic into `css.py` and core logic into `floating_chatbot.py`.
- **Improved UX**: Enhanced visual state management, such as blurring buttons after closure.

### Removed
- **`add_floating_chatbot` function**: This has been replaced by the `FloatingChatbot` class. Users should now instantiate `FloatingChatbot` and call `create_layout()`.

### Dependencies
- Added `pyyaml` for configuration file support.
