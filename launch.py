import sys
import webview

# Get the website URL from command-line argument
if len(sys.argv) < 2:
    print("Usage: python launch.py <website_url>")
    sys.exit(1)

site_url = sys.argv[1]

# JavaScript for dragging
drag_js = """
let isDragging = false;
let offsetX, offsetY;

document.getElementById("drag-bar").addEventListener("mousedown", (e) => {
    isDragging = true;
    offsetX = e.clientX;
    offsetY = e.clientY;
});

document.addEventListener("mousemove", (e) => {
    if (isDragging) {
        let moveX = e.screenX - offsetX;
        let moveY = e.screenY - offsetY;
        window.pywebview.api.move(moveX, moveY);
    }
});

document.addEventListener("mouseup", () => {
    isDragging = false;
});
"""

# HTML for draggable window
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notifier</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }}
        body {{ background: transparent; }}

        .window {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            border-radius: 12px;
            overflow: hidden; 
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            background: white;
            padding: 10px;
        }}

        .title-bar {{
            height: 30px;
            background: #333;
            color: white;
            display: flex;
            align-items: center;
            padding: 0 10px;
            cursor: grab;
            user-select: none;
        }}

        .title {{
            flex-grow: 1;
        }}

        .buttons {{
            display: flex;
        }}

        .button {{
            width: 30px;
            text-align: center;
            cursor: pointer;
        }}

        .button:hover {{
            background: #555;
        }}

        iframe {{
            width: 100%;
            height: 300px;
            border: none;
        }}
    </style>
</head>
<body>
    <div class="window">
        <div class="title-bar" id="drag-bar">
            <div class="title">Notifier</div>
            <div class="buttons">
                <div class="button" onclick="window.pywebview.api.close()">✖</div>
            </div>
        </div>

        <iframe src="{site_url}"></iframe>
    </div>

    <script>
        {drag_js}
    </script>
</body>
</html>
"""

class WindowAPI:
    def close(self):
        webview.windows[0].destroy()

    def move(self, x, y):
        webview.windows[0].move(x, y)

# Create the window
webview.create_window(
    'Notifier',
    html_content,
    width=400,
    height=350,
    resizable=False,
    frameless=True,
    on_top=True,
    js_api=WindowAPI()
)

# Start WebView
webview.start()
