# TeleAutoVision

## What it does

TeleAutoVision automates a Telegram conversation with a configured bot. It opens Telegram, finds on-screen controls from image templates, sends the configured messages, and closes the chat when the flow is complete.

The image-recognition automation is in `withopencvimages/ImageRecognition.py`. It uses the visible Telegram interface instead of fixed coordinates for bot controls.

## Features

- Telegram automation for the existing bot and message flow.
- OpenCV image recognition using template matching against live screenshots.
- PyAutoGUI interaction for mouse movement, clicks, and pasting text.
- A retry mechanism that preserves the configured retry count and delay.
- Menu recovery: Button 1 is retried after opening the menu when the first search fails.
- A multi-image button flow: `nomatterwhathustreal.png` is clicked before `findrealpeople.png`.

## How it works

1. The script checks for the required templates in `withopencvimages/images`.
2. It starts the Telegram executable in `TELEGRAM_EXE` and opens the configured bot.
3. `find_and_click` captures the screen with Pillow, matches the template with OpenCV, and clicks the centre of the best match.
4. It clicks Button 1. If the existing retries do not find it, the script opens the menu and retries Button 1 once.
5. It clicks `nomatterwhathustreal.png`, then `findrealpeople.png`, in that order.
6. It finds the message box, sends the configured messages, and runs the existing menu/end-chat flow.

## Project Structure

```text
TeleAutoVision/
├── telegram_auto.py                    # Coordinate-based automation variant
├── get_mouse_position.py                # Screen-coordinate helper
├── withopencvimages/
│   ├── ImageRecognition.py              # Image-recognition automation
│   └── images/                          # OpenCV templates
│       ├── button_1.png
│       ├── nomatterwhathustreal.png
│       ├── findrealpeople.png
│       ├── message_box.png
│       ├── menu.png
│       ├── end_chat_1.png
│       └── end_chat_2.png
└── LICENSE
```

## Requirements

- Windows with Telegram Desktop installed.
- Python 3.
- `opencv-python`
- `numpy`
- `pyautogui`
- `pyperclip`
- `Pillow`

The other modules used by the script (`os`, `time`, and `subprocess`) are part of Python's standard library.

## Installation

1. Clone or download the repository on Windows.
2. Open PowerShell in the repository root.
3. Create and activate a virtual environment (recommended):

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```powershell
   py -m pip install opencv-python numpy pyautogui pyperclip Pillow
   ```

5. Set `TELEGRAM_EXE` in `withopencvimages/ImageRecognition.py` to the full path of `Telegram.exe`. Review `BOT_USERNAME`, `MESSAGE`, and the search coordinates for your setup.
6. Open Telegram on the display used to capture the templates, then run:

   ```powershell
   py .\withopencvimages\ImageRecognition.py
   ```

## Images

Place these templates in `withopencvimages/images`:

- `button_1.png`
- `nomatterwhathustreal.png`
- `findrealpeople.png`
- `message_box.png`
- `menu.png`
- `end_chat_1.png`
- `end_chat_2.png`

`button_2.png` is not used by the image-recognition flow. Recapture a template when the visible Telegram control differs because of its theme, language, zoom, scaling, or layout.

## Configuration

Important values in `withopencvimages/ImageRecognition.py` are:

- `TELEGRAM_EXE`: absolute path to Telegram Desktop.
- `BOT_USERNAME`: bot opened by the search flow.
- `MESSAGE` and `MESSAGES`: text sent by the automation.
- `SEARCH_X` and `SEARCH_Y`: location of Telegram's search bar.
- `TELEGRAM_START_WAIT`, `SEARCH_WAIT`, `BOT_WAIT`, `BUTTON_WAIT`, and `MESSAGE_WAIT`: waits between existing steps.
- `confidence`: template threshold passed to `find_and_click`. Calls that used `0.80` now use `0.35` while keeping the same matching method.
- `retries` and `retry_delay`: retry count and pause for an image search.

## Troubleshooting

### Image not found

Check that the expected PNG exists in `withopencvimages/images`, the relevant Telegram control is visible, and no window covers it. The console logs the template path and confidence for every attempt.

### Low confidence

Templates must closely match the current control. Recapture them at the same Telegram theme, language, zoom level, and display scaling. Avoid lowering a threshold blindly: an overly low value can select the wrong control.

### Telegram not opening

Confirm that `TELEGRAM_EXE` points to a real `Telegram.exe` and that Python can start it. The script prints the exact path it checked.

### Wrong screen scaling

The search flow uses `SEARCH_X` and `SEARCH_Y`, so another monitor arrangement, resolution, or Windows display scale can move the target. Re-measure those values with `get_mouse_position.py`.

### Wrong screenshot/template size

OpenCV template matching is sensitive to scale. Capture templates at the same effective size as the Telegram window used during automation; a different DPI scale or zoom level can prevent a match.

## Notes

- Keep Telegram's resolution, layout, and Windows display scaling consistent with the template captures.
- Screenshots come from Pillow's `ImageGrab`, and matching uses OpenCV's `TM_CCOEFF_NORMED`; templates are not automatically resized.
- Test the full flow with a safe account before relying on it for regular use.

## Disclaimer

Use automation responsibly and only for accounts, conversations, and actions you are authorized to manage. You are responsible for complying with Telegram's terms, bot rules, and applicable laws.
