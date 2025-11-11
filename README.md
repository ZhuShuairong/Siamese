# Siamese Prompt Manager

A comprehensive prompt management application with system tray integration for Windows. Designed to help users organize, store, and quickly access AI prompts and text snippets with a clean, intuitive interface.

## Features

### Core Functionality
- **Prompt Management**: Create, edit, delete, and organize prompts with titles and content
- **System Tray Integration**: Runs in the background with a tray icon for quick access
- **Clipboard Integration**: One-click copying of prompts to clipboard with automatic clearing
- **Search Functionality**: Real-time search through all prompts with keyword filtering

### Advanced Features
- **Pin Important Prompts**: Pin up to 5 frequently used prompts for instant access
- **Import/Export**: JSON-based import and export of prompt collections
- **Multi-language Support**: English and Chinese language options
- **Theme Support**: Dark and light themes with custom color schemes
- **Auto-start**: Option to launch automatically with Windows startup
- **Persistent Storage**: All prompts saved in JSON format locally

### User Interface
- **Clean GUI**: Modern tkinter-based interface with responsive design
- **Context Menus**: Right-click tray icon for quick actions
- **Preview System**: Content preview for long prompts
- **Validation**: Input validation and error handling

## Installation

### Pre-built Executable (Recommended)
1. Download `Siamese.exe` from the releases page
2. Place the executable in your desired directory
3. Run `Siamese.exe` directly (no installation required)

 # Siamese Prompt Manager (Prompt Manager for Windows)

Siamese is a Windows-focused system tray Prompt Manager (written in Python) that helps you store, organize, and quickly copy text prompts/snippets to the clipboard. The UI is tkinter-based and the app is intended to run in the background with a tray icon for fast access.

This README has been updated to match the behavior of the current `Siamese.py` implementation.

## What it does
- Runs as a system tray application on Windows (tray icon via `pystray`).
- Manage prompts: add, edit, delete, and pin prompts (max 5 pinned for quick access).
- Copy prompt content to the clipboard from the tray or manager window. The clipboard is automatically cleared after ~30s.
- Import/export prompts as JSON files.
- Two languages supported (English/Chinese) and light/dark themes.
- Optional auto-start via Windows registry.

## Important notes
- Configuration and prompts are persisted under your Windows AppData folder:

  `%APPDATA%\PromptManager\prompts.json`

  (The app creates this directory/file on first run.)

- The app attempts to set title bar colors on Windows and uses DPI awareness for sharper UI on high-DPI displays.

## Running the application

### If you have the pre-built executable (recommended)
- Double-click `Siamese.exe` to run it. The app will run in the background and create a tray icon.
- Place the exe (and `icon.png`/`icon.ico` if you want custom icons in the same folder). No Python installation is required to run the exe.

To run from PowerShell (as an example):

```powershell
.\Siamese.exe
```

### Running from source (requires Python)
1. Ensure you're on Windows and have Python 3.8+ installed.
2. Install dependencies:

```powershell
python -m pip install pystray Pillow pyperclip
```

3. Run the app:

```powershell
python Siamese.py
```

Running from source will print errors to the console if something goes wrong — useful for debugging.

## Building an executable (optional)
You can produce a standalone `Siamese.exe` using PyInstaller:

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.png;." --add-data "icon.ico;." --name "Siamese" Siamese.py
```

Adjust the `--add-data` paths for your platform/pyinstaller version.

## Usage summary
- Right-click the tray icon to open the manager window and access settings.
- Use the manager window to search, add, edit, delete, pin, import, and export prompts.
- Pinned prompts (up to 5) appear in the tray menu for one-click copy.

## File structure (repo)

```
Siamese/
├── Siamese.py          # Main application (tray-based Prompt Manager)
├── pyproject.toml      # Project metadata / dependency hints
├── prompts.json        # User prompts storage (created in %APPDATA% on run)
├── icon.png            # Optional icon used by the app
├── icon.ico            # Optional ICO used for window icon
├── README.md           # This file
└── Siamese.spec        # PyInstaller spec (optional)
```

## Requirements
- Windows 10 or later
- Python 3.8+ to run from source
- Packages (if running from source): `pystray`, `Pillow`, `pyperclip`

## Troubleshooting
- If the tray icon doesn't show, confirm the process is running in Task Manager.
- If clipboard copying fails, ensure no other process has locked the clipboard and that `pyperclip` supports your environment (may need additional platform-specific dependencies).
- Import/export expects a JSON object with a `prompts` array of objects containing `title` and `content` strings.

## Contributing
Follow the normal GitHub workflow: fork, branch, test, and submit a PR.

## License
MIT

---
Updated to reflect changes in `Siamese.py` (tray behavior, AppData config path, themes, language, pin limits, and clipboard clearing).
## License
