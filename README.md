# Offline OCR Screen Tool for Windows

Press a keyboard shortcut, drag a box over any text on your screen, and the text is
recognized **offline** and copied to your clipboard. It works like the Snipping Tool,
but for extracting text. It uses [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
and runs silently in the background.

## Features

- Global hotkey (default `Ctrl+Shift+F`), works in any app
- Drag-to-select overlay, `Esc` cancels
- Fully offline, no internet needed after setup
- Text is copied to the clipboard automatically
- Optional popup window showing (and letting you edit) the copied text
- Multi-language support (e.g. English + Bengali)
- Starts automatically at login with no console window

## Requirements

- Windows 10 or 11 (64-bit), about 1 GB free disk space
- Python 3.10+
- Tesseract OCR (UB Mannheim Windows build)

## Setup

### 1. Install Python

1. Download Python from <https://www.python.org/downloads/>.
2. Run the installer and tick **Add Python to PATH**, then click Install Now.
3. Open Command Prompt and check:
   ```
   python --version
   ```
   If you use the newer Python install manager and `python` is not recognized, use `py` instead of `python` (and `pyw` instead of `pythonw`) everywhere below.

### 2. Install Tesseract OCR

1. Open <https://github.com/UB-Mannheim/tesseract/wiki> and download the latest 64-bit installer (`tesseract-ocr-w64-setup-...exe`).
2. Run it. If Windows shows "Windows protected your PC", click **More info**, then **Run anyway**.
3. On the **Additional language data** screen, tick any extra languages you need (e.g. Bengali). English is included.
4. Keep the default folder `C:\Program Files\Tesseract-OCR`.
5. Verify:
   ```
   "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```

### 3. Get this project

```
git clone https://github.com/MHShiqder/OCR-TEXT-COPY C:\ocr_tool
cd C:\ocr_tool
```

No Git? Click **Code → Download ZIP** on GitHub and extract it to `C:\ocr_tool`.

### 4. Install the Python libraries

```
pip install -r requirements.txt
```

If `pip` is not recognized: `python -m pip install -r requirements.txt`

### 5. Run it

```
python ocr_tool.py
```

Press `Ctrl+Shift+F`, drag over some text, release, then paste with `Ctrl+V`.
Close the window or press `Ctrl+C` to stop it.

### 6. Start automatically at login

1. Press `Win + R`, type `shell:startup`, press Enter. The Startup folder opens.
2. Open your `C:\ocr_tool` folder in another window.
3. Right-click `start_ocr.vbs`, choose **Show more options → Create shortcut** (on Windows 10: **Create shortcut**).
4. Move that shortcut into the Startup folder.
5. Double-click the shortcut once to start the tool now.

Nothing appears on screen. The tool is running in the background and the hotkey works.

## Configuration

Edit the settings at the top of `ocr_tool.py`:

| Setting | Meaning | Example |
|---|---|---|
| `HOTKEY` | Shortcut keys, joined with `+`, lowercase | `"ctrl+alt+o"` |
| `LANG` | OCR language(s) | `"eng"`, `"eng+ben"` |
| `SHOW_POPUP` | `True` shows the text window, `False` copies silently | `False` |

After editing, restart the tool: end **Python / pythonw.exe** in Task Manager (`Ctrl+Shift+Esc`), then run `start_ocr.vbs` again.

Avoid shortcuts already used by Windows or your apps (e.g. `win+shift+s` is the Snipping Tool).

## Troubleshooting

| Problem | Fix |
|---|---|
| Nothing happens at startup | Run `python ocr_tool.py` in Command Prompt to see the error message |
| `TesseractNotFoundError` | The path in `ocr_tool.py` does not match where Tesseract is installed |
| Overlay does not disappear / odd behavior | Two copies are running. End all Python tasks in Task Manager and start once |
| `TabError` or indentation error | The file mixes tabs and spaces. Use spaces only |
| Selected area is offset | Make sure the `SetProcessDpiAwareness(1)` line at the top is present |
| Hotkey does not work in some apps | Those apps run as administrator. Run the script as administrator too |
| Language not found | Install that language data with the Tesseract installer, or put its `.traineddata` file in `C:\Program Files\Tesseract-OCR\tessdata` |
| Poor accuracy | Select a larger, clearer area and avoid very small text |

## Performance

Idle use is tiny: roughly 20 to 40 MB of RAM and about 0% CPU. It only works for a second or two after each capture.

## License

MIT, see [LICENSE](LICENSE).
