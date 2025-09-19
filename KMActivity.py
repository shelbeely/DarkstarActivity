import threading
import time
from datetime import datetime
from pynput import keyboard, mouse

# Path to store activity timestamp
ACTIVITY_FILE = "activity_timestamp.txt"
activity_lock = threading.Lock()

def write_timestamp():
    """Write the current time to the activity file."""
    with activity_lock:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ACTIVITY_FILE, "w") as f:
            f.write(timestamp)

def on_keyboard_activity(key):
    write_timestamp()

def on_mouse_activity(x, y):
    write_timestamp()

def start_listeners():
    # Start listeners in daemon mode so they terminate with the script
    keyboard_listener = keyboard.Listener(on_press=on_keyboard_activity)
    mouse_listener = mouse.Listener(on_move=on_mouse_activity)
    keyboard_listener.daemon = True
    mouse_listener.daemon = True
    keyboard_listener.start()
    mouse_listener.start()

    print("Listening for activity... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    start_listeners()
