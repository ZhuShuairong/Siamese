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

### Build from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/ZhuShuairong/Siamese.git
   cd Siamese
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or
   pip install pystray Pillow pyperclip
   ```

3. Run the application:
   ```bash
   python Siamese.py
   ```

4. (Optional) Build executable:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.png;." --add-data "icon.ico;." --name "Siamese" Siamese.py
   ```

## Usage

### First Time Setup
1. Launch the application
2. The icon will appear in your system tray
3. Right-click the tray icon to access the menu

### Managing Prompts
- **Add New Prompt**: Right-click tray icon → "Add New Prompt"
- **Edit Prompt**: Select a prompt from the list → "Edit"
- **Delete Prompt**: Select a prompt → "Delete"
- **Copy to Clipboard**: Click on any prompt to copy its content
- **Search**: Use the search bar to filter prompts by keywords

### Settings
- **Language**: Switch between English and Chinese
- **Theme**: Toggle between dark and light modes
- **Auto-start**: Enable/disable automatic startup with Windows

### Import/Export
- **Export**: Save all prompts to a JSON file
- **Import**: Load prompts from a JSON file (merges with existing prompts)

## Requirements

- **Operating System**: Windows 10 or later
- **Python**: 3.8+ (for source installation)
- **Dependencies**:
  - pystray >= 0.18.0
  - Pillow >= 9.0.0, < 12.0.0
  - pyperclip >= 1.8.0

## File Structure

```
Siamese/
├── Siamese.py          # Main application file
├── pyproject.toml      # Project configuration and dependencies
├── prompts.json        # User prompts storage (created automatically)
├── icon.png           # Application icon (PNG format)
├── icon.ico           # Application icon (ICO format)
├── README.md          # This file
└── Siamese.spec       # PyInstaller specification file
```

## Configuration

The application stores user preferences and prompts in:
- `prompts.json`: Contains all user prompts and settings
- Windows Registry: Auto-start settings (optional)

## Troubleshooting

### Common Issues
- **Tray icon not visible**: Check if the application is running in Task Manager
- **Clipboard not working**: Ensure no other application is locking the clipboard
- **Import fails**: Verify the JSON file format matches the expected structure

### Logs
The application runs silently. For debugging, run from command line:
```bash
python Siamese.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Version History

- **v0.1.0**: Initial release with core prompt management features
