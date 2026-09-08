import os
import time
import subprocess

import cv2
import numpy as np
import pyautogui
import pyperclip

from PIL import ImageGrab


# =========================================================
# Configuration
# =========================================================

TELEGRAM_EXE = r"D:\AMsh\8.12.2025files\tportable-x64.5.16.6\Telegram\Telegram.exe"

# Telegram bot username
BOT_USERNAME = "@TeleChateBot"

# Message to send
MESSAGE = "سلام خوبی."


# =========================================================
# Base Directory / Images
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")


def image_path(filename):
    return os.path.join(IMAGE_DIR, filename)


# =========================================================
# Screen Coordinates
# =========================================================


# Search bar
SEARCH_X = 1865
SEARCH_Y = 50


# =========================================================
# Timing
# =========================================================

TELEGRAM_START_WAIT = 2
SEARCH_WAIT = 2
BOT_WAIT = 3

BUTTON_WAIT = 2
MESSAGE_WAIT = 1
END_CHAT_WAIT = 2


# =========================================================
# Image Recognition
# =========================================================

def find_and_click(
    image_path_value,
    name,
    confidence=0.70,
    wait=2,
    retries=5,
    retry_delay=1
):
    print()
    print(f"[IMAGE] Searching for: {name}")
    print(f"[IMAGE] Image: {image_path_value}")

    if not os.path.exists(image_path_value):
        print(
            f"[ERROR] Image not found: "
            f"{image_path_value}"
        )
        return False

    template = cv2.imread(
        image_path_value
    )

    if template is None:
        print(
            f"[ERROR] Could not load image: "
            f"{image_path_value}"
        )
        return False

    template_height, template_width = (
        template.shape[:2]
    )

    print(
        f"[IMAGE] Template size: "
        f"{template_width}x{template_height}"
    )

    for attempt in range(
        1,
        retries + 1
    ):

        print(
            f"[IMAGE] {name} "
            f"attempt {attempt}/{retries}"
        )

        try:
            # ---------------------------------------------
            # Screenshot WITHOUT pyautogui.screenshot()
            # ---------------------------------------------

            screenshot = ImageGrab.grab()

            screenshot = cv2.cvtColor(
                np.array(screenshot),
                cv2.COLOR_RGB2BGR
            )

            # ---------------------------------------------
            # OpenCV Template Matching
            # ---------------------------------------------

            result = cv2.matchTemplate(
                screenshot,
                template,
                cv2.TM_CCOEFF_NORMED
            )

            _, max_val, _, max_loc = (
                cv2.minMaxLoc(result)
            )

            print(
                f"[IMAGE] {name} confidence: "
                f"{max_val:.3f}"
            )

            # ---------------------------------------------
            # Found
            # ---------------------------------------------

            if max_val >= confidence:

                x = (
                    max_loc[0]
                    + template_width // 2
                )

                y = (
                    max_loc[1]
                    + template_height // 2
                )

                print(
                    f"[IMAGE] {name} FOUND!"
                )

                print(
                    f"[IMAGE] Position: "
                    f"X={x}, Y={y}"
                )

                # Move mouse
                pyautogui.moveTo(
                    x,
                    y,
                    duration=0.3
                )

                time.sleep(0.3)

                # Click
                pyautogui.click()

                print(
                    f"[IMAGE] {name} "
                    f"clicked successfully."
                )

                time.sleep(wait)

                return True

            # ---------------------------------------------
            # Not found
            # ---------------------------------------------

            print(
                f"[IMAGE] {name} not found."
            )

        except Exception as e:

            print(
                f"[ERROR] Screenshot/Image "
                f"recognition error: {e}"
            )

        if attempt < retries:
            time.sleep(retry_delay)

    print()
    print(
        f"[IMAGE] FAILED: {name} "
        f"was not found."
    )

    return False


# =========================================================
# Open Telegram
# =========================================================

def open_telegram():

    print()
    print("[TELEGRAM] Starting Telegram...")

    if not os.path.exists(TELEGRAM_EXE):

        print(
            "[ERROR] Telegram.exe was not found!"
        )

        print(
            f"[ERROR] Checked path: "
            f"{TELEGRAM_EXE}"
        )

        return False

    try:

        subprocess.Popen(
            [TELEGRAM_EXE],
            cwd=os.path.dirname(TELEGRAM_EXE)
        )

        print(
            "[TELEGRAM] Telegram started "
            "successfully."
        )

        print(
            f"[TELEGRAM] Waiting "
            f"{TELEGRAM_START_WAIT} seconds..."
        )

        time.sleep(
            TELEGRAM_START_WAIT
        )

        print(
            "[TELEGRAM] Telegram is ready."
        )

        return True

    except Exception as e:

        print(
            f"[ERROR] Failed to start "
            f"Telegram: {e}"
        )

        return False


# =========================================================
# Search Bot
# =========================================================

def search_bot():

    print()
    print(
        "[STEP 1] Opening Telegram search..."
    )

    print(
        f"[CLICK] Search Bar "
        f"X={SEARCH_X}, Y={SEARCH_Y}"
    )

    pyautogui.moveTo(
        SEARCH_X,
        SEARCH_Y,
        duration=0.3
    )

    time.sleep(0.3)

    pyautogui.click()

    time.sleep(SEARCH_WAIT)

    print(
        f"[SEARCH] Searching for: "
        f"{BOT_USERNAME}"
    )

    # Copy username
    pyperclip.copy(
        BOT_USERNAME
    )

    # Paste
    pyautogui.hotkey(
        "ctrl",
        "v"
    )

    print(
        "[SEARCH] Bot username entered."
    )

    time.sleep(2)

    print(
        "[SEARCH] Opening bot result..."
    )

    # Bot result
    bot_result_x = SEARCH_X
    bot_result_y = SEARCH_Y + 90

    pyautogui.moveTo(
        bot_result_x,
        bot_result_y,
        duration=0.3
    )

    time.sleep(0.3)

    pyautogui.click()

    print(
        "[SEARCH] Bot result clicked."
    )

    time.sleep(BOT_WAIT)


# =========================================================
# Click Bot Buttons
# =========================================================

def click_bot_buttons():
    print()
    print(
        "[STEP 2] Clicking first bot button..."
    )
    button_1 = find_and_click(
        image_path(
            "button_1.png"
        ),
        "Button 1",
        confidence=0.70,
        wait=BUTTON_WAIT,
        retries=5,
        retry_delay=1
    )

    if not button_1:
        print(
            "[ERROR] Button 1 not found."
        )
        print(
            "[MENU] Opening menu..."
        )

        if not click_menu():
            print(
                "[ERROR] Menu could not "
                "be opened."
            )
            return False

        time.sleep(1)

        print(
            "[STEP 2] Trying Button 1 again..."
        )

        button_1 = find_and_click(
            image_path(
                "button_1.png"
            ),
            "Button 1 Again",
            confidence=0.70,
            wait=BUTTON_WAIT,
            retries=5,
            retry_delay=1
        )

        if not button_1:
            print(
                "[ERROR] Button 1 still "
                "could not be clicked."
            )
            return False

    print()
    print(
        "[STEP 3] Clicking second bot button..."
    )

    button_2_images = [
        "nomatterwhathustreal.png",
        "findrealpeople.png"
    ]

    for index, image_name in enumerate(
        button_2_images,
        start=1
    ):
        button_2 = find_and_click(
            image_path(
                image_name
            ),
            f"Button 2 - {index}",
            confidence=0.35,
            wait=BUTTON_WAIT,
            retries=5,
            retry_delay=1
        )

        if not button_2:
            print(
                f"[ERROR] {image_name} could not "
                "be clicked."
            )
            return False

    print(
        "[BOT] All bot buttons clicked."
    )
    return True


# =========================================================
# Message Input
# =========================================================

def click_message_box():

    print()
    print(
        "[MESSAGE] Finding message box..."
    )

    return find_and_click(
        image_path(
            "message_box.png"
        ),
        "Message Box",
        confidence=0.80,
        wait=MESSAGE_WAIT,
        retries=5,
        retry_delay=1
    )


# =========================================================
# Send Text
# =========================================================

def send_text(message):

    print(
        f"[TYPE] Preparing message:"
    )

    print(
        f"[TYPE] {message}"
    )

    # Copy Persian/emoji text
    pyperclip.copy(message)

    # Paste
    pyautogui.hotkey(
        "ctrl",
        "v"
    )

    time.sleep(0.7)

    # Send
    pyautogui.press(
        "enter"
    )

    print(
        "[SEND] Message sent."
    )

    time.sleep(2)


# =========================================================
# Write First Message
# =========================================================

def write_message():

    print()
    print(
        "[WAIT] Waiting 15 seconds "
        "before typing..."
    )

    time.sleep(15)

    print()
    print(
        "[STEP 4] Finding message input..."
    )

    if not click_message_box():

        print(
            "[ERROR] Message input "
            "was not found."
        )

        return False

    print(
        "[TYPE] Sending first message..."
    )

    send_text(
        MESSAGE
    )

    return True


# =========================================================
# Additional Messages
# =========================================================

MESSAGES = [
    "سلام خوبی؟ 👋",

    "دوسداری به گروه آموزش کامپیوتر و خدمات کافی نت و پوستر و چاپ و لوازم التحریر و طراحی سایت و هوشمندسازی خانه و همه چی با قطعات و IoT و تکنولوژی ما بیای؟",
    "توی گروهمون آموزش‌ها، خدمات کامپیوتری، طراحی، چاپ، برنامه‌نویسی، IoT، هوشمندسازی خانه و کلی موضوع دیگه داریم 🚀",
    "اگه دوست داشتی خوشحال می‌شیم به جمعمون اضافه بشی ❤️",
    "آیدی گروه: iotirancs",
    "اگر آیدی گروه نیومدش برات اینو بنویس با ادساین اولش (آی او تی ایران سی اس)",
    "نظرت چیه میای اوکی ای؟",
    time.sleep(5)
]


# =========================================================
# Menu
# =========================================================

def click_menu():

    print()
    print(
        "[MENU] Searching for Menu..."
    )

    return find_and_click(
        image_path(
            "menu.png"
        ),
        "Menu",
        confidence=0.80,
        wait=2,
        retries=5,
        retry_delay=1
    )


# =========================================================
# Open Menu + Send Messages
# =========================================================

def open_menu_and_send_messages():

    print()
    print(
        "[STEP 5] Opening menu..."
    )

    if not click_menu():

        print(
            "[ERROR] Menu could not "
            "be opened."
        )

        return False

    print()
    print(
        "[STEP 6] Sending additional "
        "messages..."
    )

    for index, message in enumerate(
        MESSAGES,
        start=1
    ):

        print()
        print(
            f"[MESSAGE {index}/"
            f"{len(MESSAGES)}]"
        )

        # Find message box
        if not click_message_box():

            print(
                "[ERROR] Message box "
                "not found."
            )

            return False

        # Send message
        send_text(
            message
        )

    print()
    print(
        "[MESSAGES] All additional "
        "messages sent successfully."
    )

    return True


# =========================================================
# End Chat
# =========================================================

def end_chat():

    print()
    print(
        "========================================"
    )

    print(
        "[END CHAT] Starting..."
    )

    print(
        "========================================"
    )

    max_attempts = 5

    for attempt in range(
        1,
        max_attempts + 1
    ):

        print()
        print(
            f"[END CHAT] Attempt "
            f"{attempt}/{max_attempts}"
        )

        # -------------------------------------------------
        # Try to find first End Chat option
        # -------------------------------------------------

        found_first = find_and_click(
            image_path(
                "end_chat_1.png"
            ),
            "End Chat Option 1",
            confidence=0.80,
            wait=2,
            retries=2,
            retry_delay=1
        )

        # -------------------------------------------------
        # First option found
        # -------------------------------------------------

        if found_first:

            print(
                "[END CHAT] First option "
                "clicked."
            )

            time.sleep(1)

            # Find second confirmation
            found_second = find_and_click(
                image_path(
                    "end_chat_2.png"
                ),
                "End Chat Option 2",
                confidence=0.80,
                wait=2,
                retries=5,
                retry_delay=1
            )

            if found_second:

                print()
                print(
                    "[END CHAT] Chat closed "
                    "successfully."
                )

                return True

            # Second option wasn't found
            print(
                "[END CHAT] Second option "
                "was not found."
            )

            print(
                "[END CHAT] Opening menu again..."
            )

            time.sleep(1)

            find_and_click(
                image_path(
                    "menu.png"
                ),
                "Menu",
                confidence=0.80,
                wait=2,
                retries=5,
                retry_delay=1
            )

            continue

        # -------------------------------------------------
        # First option wasn't found
        # -------------------------------------------------

        print(
            "[END CHAT] First End Chat "
            "option was not found."
        )

        print(
            "[END CHAT] Opening Menu again..."
        )

        time.sleep(1)

        menu_clicked = find_and_click(
            image_path(
                "menu.png"
            ),
            "Menu",
            confidence=0.80,
            wait=2,
            retries=5,
            retry_delay=1
        )

        if menu_clicked:

            print(
                "[END CHAT] Menu opened. "
                "Trying End Chat again..."
            )

            time.sleep(1)

        else:

            print(
                "[END CHAT] Menu was also "
                "not found."
            )

            time.sleep(2)

    print()
    print(
        "[END CHAT] Failed after "
        f"{max_attempts} attempts."
    )

    return False


# =========================================================
# Main
# =========================================================

def main():

    print()
    print(
        "========================================"
    )

    print(
        "       Telegram Automation"
    )

    print(
        "========================================"
    )

    print()

    # -----------------------------------------------------
    # Check Images
    # -----------------------------------------------------

    print(
        "[CHECK] Checking image files..."
    )

    required_images = [
        "button_1.png",
        "nomatterwhathustreal.png",
        "findrealpeople.png",
        "message_box.png",
        "menu.png",
        "end_chat_1.png",
        "end_chat_2.png"
    ]

    missing_images = []

    for filename in required_images:

        full_path = image_path(
            filename
        )

        if os.path.exists(full_path):

            print(
                f"[OK] {filename}"
            )

        else:

            print(
                f"[MISSING] {filename}"
            )

            missing_images.append(
                filename
            )

    if missing_images:

        print()
        print(
            "[ERROR] Missing image files:"
        )

        for filename in missing_images:
            print(
                f" - {filename}"
            )

        print()
        print(
            "[ERROR] Put all images "
            "inside the images folder."
        )

        return

    print()
    print(
        "[CHECK] All image files found."
    )

    # -----------------------------------------------------
    # Open Telegram
    # -----------------------------------------------------

    if not open_telegram():

        print(
            "[EXIT] Program stopped."
        )

        return

    print()
    print(
        "[AUTOMATION] Starting..."
    )

    # -----------------------------------------------------
    # Search Bot
    # -----------------------------------------------------

    search_bot()

    # -----------------------------------------------------
    # Bot Buttons
    # -----------------------------------------------------

    if not click_bot_buttons():

        print(
            "[EXIT] Bot buttons failed."
        )

        return

    # -----------------------------------------------------
    # First Message
    # -----------------------------------------------------

    if not write_message():

        print(
            "[EXIT] First message failed."
        )

        return

    # -----------------------------------------------------
    # Menu + Additional Messages
    # -----------------------------------------------------

    if not open_menu_and_send_messages():

        print(
            "[EXIT] Additional messages "
            "failed."
        )

        return

    # -----------------------------------------------------
    # End Chat
    # -----------------------------------------------------

    if not end_chat():

        print(
            "[WARNING] Could not close "
            "the chat automatically."
        )

        return

    # -----------------------------------------------------
    # Done
    # -----------------------------------------------------

    print()
    print(
        "========================================"
    )

    print(
        "[DONE] Automation completed "
        "successfully."
    )

    print(
        "========================================"
    )


#=========================================================
#Entry Point
#=========================================================

def main():
    if not open_telegram():
        return

    for i in range(4):
        print(f"Starting cycle {i + 1}/3")

        search_bot()
        click_bot_buttons()
        write_message()
        open_menu_and_send_messages()
        end_chat()

        time.sleep(3)

    print("All 3 cycles completed.")



#with no loop for test
if __name__ == "__main__":
    main()