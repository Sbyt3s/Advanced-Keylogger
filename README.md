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



## Webhook Setup

The keylogger is configured to send data to a Discord webhook by default, but you can use any webhook service that accepts POST requests with JSON payloads.

For Discord webhooks:
1. Go to your Discord server
2. Edit a channel
3. Select "Integrations" > "Webhooks"
4. Create a new webhook and copy the URL


## Installation

### Option 1: Easy Installation (Recommended)

If you encounter any installation issues, use this simplified method:

1. Add webhook url in the keylogger.py:
    Edit line number 253 of keylogger.py file

2. Run the easy installation script:
     easy_install.bat
  
3. Run the builder:
   build.bat


## Configuration Options

You can customize the keylogger by modifying these variables in `keylogger.py`:

# Configuration options
REPORT_INTERVAL = 60  # seconds
TAKE_SCREENSHOTS = True
MONITOR_CLIPBOARD = True
LOG_CLICKS = True

## Legal Disclaimer

This tool is provided for educational purposes only. Using a keylogger without explicit permission from the owner of the device is illegal and unethical. Always ensure you have proper authorization before deploying this tool. 
