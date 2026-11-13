import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import time
import tkinter as tk
import keyboard
import pyperclip
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

HOTKEY = "ctrl+shift+f"   # change to any combo, e.g. "ctrl+alt+o"
LANG = "eng"              # "eng+ben" for English + Bengali (language data must be installed)
SHOW_POPUP = True         # True = show the text window, False = copy silently


def show_popup(text):
    win = tk.Tk()
    win.title("Text copied")
    win.attributes("-topmost", True)
    w, h = 420, 260
    x = win.winfo_screenwidth() - w - 20
    y = win.winfo_screenheight() - h - 70
    win.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(win, text="Copied to clipboard", anchor="w",
             font=("Segoe UI", 10, "bold")).pack(fill="x", padx=10, pady=(8, 2))

    box = tk.Text(win, wrap="word", font=("Segoe UI", 10))
    box.pack(fill="both", expand=True, padx=10, pady=4)
    box.insert("1.0", text if text else "(No text found)")

    btns = tk.Frame(win)
    btns.pack(fill="x", padx=10, pady=(0, 8))
    tk.Button(btns, text="Copy", width=10,
              command=lambda: pyperclip.copy(box.get("1.0", "end-1c"))).pack(side="left")
    tk.Button(btns, text="Close", width=10, command=win.destroy).pack(side="right")

    win.bind("<Escape>", lambda e: win.destroy())
    win.focus_force()
    win.mainloop()


class Selector:
    def __init__(self):
        self.box = None
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True, "-topmost", True, "-alpha", 0.3)
        self.root.configure(bg="black", cursor="cross")
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.start = None
        self.rect = None
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.focus_force()
        self.root.mainloop()

        # The overlay is closed by now, so do the OCR
        if self.box:
            time.sleep(0.15)   # let the overlay fully disappear before the screenshot
            img = ImageGrab.grab(bbox=self.box)
            img = img.resize((img.width * 2, img.height * 2))   # helps with small text
            text = pytesseract.image_to_string(img, lang=LANG).strip()
            if text:
                pyperclip.copy(text)
            if SHOW_POPUP or not text:
                show_popup(text)

    def on_press(self, e):
        self.start = (e.x_root, e.y_root)
        self.rect = self.canvas.create_rectangle(e.x, e.y, e.x, e.y, outline="red", width=2)

    def on_drag(self, e):
        if self.rect is None:
            return
        x0, y0 = self.start
        self.canvas.coords(self.rect, x0 - self.root.winfo_rootx(),
                           y0 - self.root.winfo_rooty(), e.x, e.y)

    def on_release(self, e):
        if self.start is None:
            return
        x0, y0 = self.start
        x1, y1 = e.x_root, e.y_root
        box = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        if box[2] - box[0] > 5 and box[3] - box[1] > 5:
            self.box = box
        self.root.destroy()


keyboard.add_hotkey(HOTKEY, Selector)
keyboard.wait()
