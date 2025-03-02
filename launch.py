import webview
import screeninfo
import tkinter as tk
from tkinter import messagebox

# Get screen dimensions
monitor = screeninfo.get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Define the window size
window_width = 400
window_height = 300

# Calculate the position for bottom-right corner
window_x = screen_width - window_width
window_y = screen_height - window_height

# JavaScript to enable dragging
drag_js = """
let isDragging = false;
let offsetX, offsetY;

document.addEventListener('mousedown', (e) => {
    if (e.target.tagName === 'IFRAME') return; // Prevent dragging from inside the iframe
    isDragging = true;
    offsetX = e.clientX;
    offsetY = e.clientY;
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        let moveX = e.screenX - offsetX;
        let moveY = e.screenY - offsetY;
        window.pywebview.api.move(moveX, moveY);
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
});
"""

class WindowAPI:
    def move(self, x, y):
        webview.windows[0].move(x, y)

    def close(self):
        webview.windows[0].destroy()

    def toggle_maximize(self):
        window = webview.windows[0]
        if window.width == screen_width and window.height == screen_height:
            window.resize(window_width, window_height)
            window.move(window_x, window_y)
        else:
            window.resize(screen_width, screen_height)
            window.move(0, 0)


def inject_js():
    webview.windows[0].evaluate_js(drag_js)


# Create a simple title bar with minimize, maximize, and close buttons
def create_custom_title_bar(window):
    # Create a new tkinter window for the title bar
    title_bar = tk.Toplevel(window)
    title_bar.overrideredirect(True)  # Remove window border/frame
    title_bar.geometry(f"{window_width}x30+{window_x}+{window_y}")  # Custom size for title bar
    title_bar.configure(bg="gray")

    # Add buttons for minimize, maximize, and close
    close_button = tk.Button(title_bar, text="X", command=lambda: window.destroy(), bg="red", fg="white", bd=0)
    close_button.pack(side="right", padx=5)

    maximize_button = tk.Button(title_bar, text="⤢", command=lambda: window.api.toggle_maximize(), bg="green", fg="white", bd=0)
    maximize_button.pack(side="right")

    title_label = tk.Label(title_bar, text="RBXGold Notifier", bg="gray", fg="white")
    title_label.pack(side="left", padx=5)

    title_bar.lift()  # Ensure title bar is always on top of the window


# Create the window
window = webview.create_window(
    'RBXGold',
    'https://rbxgold.com',
    width=window_width,
    height=window_height,
    x=window_x,
    y=window_y,
    resizable=True,  # Allow resizing the window
    frameless=True,  # Remove default window frame
    on_top=True,
    js_api=WindowAPI()
)

# Start WebView and inject JavaScript
webview.start(inject_js)
