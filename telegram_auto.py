import os
import time
import subprocess
import pyautogui
import pyperclip


# =========================================================
# Configuration
# =========================================================

TELEGRAM_EXE = r"D:\AMsh\8.12.2025files\tportable-x64.5.16.6\Telegram\Telegram.exe"

# Telegram bot username
BOT_USERNAME = "@TeleChateBot"

# Message to send
MESSAGE = "سلام خوبی."


# =========================================================
# Screen Coordinates
# =========================================================

# Search bar
SEARCH_X = 1865
SEARCH_Y = 50

# First button
BUTTON_1_X = 2744
BUTTON_1_Y = 1222

# Second button
BUTTON_2_X = 2544
BUTTON_2_Y = 1042

# Message input box
MESSAGE_X = 2587
MESSAGE_Y = 1225

# End Chat button
END_CHAT_X = 2752
END_CHAT_Y = 1364

end2_chat_x = 2468
end2_chat_y = 1116


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
# Utility
# =========================================================

def click_at(x, y, name, wait=2):
    print(f"[CLICK] {name}")
    print(f"[CLICK] Position: X={x}, Y={y}")

    pyautogui.moveTo(
        x,
        y,
        duration=0.3
    )

    time.sleep(0.3)
    pyautogui.click()

    print(f"[CLICK] {name} clicked successfully.")
    time.sleep(wait)


# =========================================================
# Open Telegram
# =========================================================

def open_telegram():
    print("[TELEGRAM] Starting Telegram...")

    if not os.path.exists(TELEGRAM_EXE):
        print("[ERROR] Telegram.exe was not found!")
        print(f"[ERROR] Checked path: {TELEGRAM_EXE}")
        return False

    try:
        subprocess.Popen(
            [TELEGRAM_EXE],
            cwd=os.path.dirname(TELEGRAM_EXE)
        )

        print("[TELEGRAM] Telegram started successfully.")

        print(
            f"[TELEGRAM] Waiting "
            f"{TELEGRAM_START_WAIT} seconds..."
        )

        time.sleep(TELEGRAM_START_WAIT)

        print("[TELEGRAM] Telegram is ready.")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to start Telegram: {e}")
        return False


# =========================================================
# Search Bot
# =========================================================

def search_bot():
    print("[STEP 1] Opening Telegram search...")

    click_at(
        SEARCH_X,
        SEARCH_Y,
        "Search Bar",
        SEARCH_WAIT
    )

    print(f"[SEARCH] Searching for: {BOT_USERNAME}")

    # Copy username to clipboard
    pyperclip.copy(BOT_USERNAME)

    # Paste username
    pyautogui.hotkey("ctrl", "v")

    print("[SEARCH] Bot username entered.")

    time.sleep(2)

    print("[SEARCH] Opening bot result...")

    # The bot result should be clicked here.
    # Currently using the same approximate search/result
    # area because no separate bot-result coordinates
    # were provided.
    #
    # We click slightly below the search bar.

    bot_result_x = SEARCH_X
    bot_result_y = SEARCH_Y + 90

    click_at(
        bot_result_x,
        bot_result_y,
        "Bot Search Result",
        BOT_WAIT
    )


# =========================================================
# Click Bot Buttons
# =========================================================

def click_bot_buttons():
    print("[STEP 2] Clicking first bot button...")

    click_at(
        BUTTON_1_X,
        BUTTON_1_Y,
        "Button 1",
        BUTTON_WAIT
    )

    print("[STEP 3] Clicking second bot button...")

    click_at(
        BUTTON_2_X,
        BUTTON_2_Y,
        "Button 2",
        BUTTON_WAIT
    )


# =========================================================
# Write Message
# =========================================================

def write_message():
    print("[WAIT] Waiting 15 seconds before typing...")
    time.sleep(15)

    print("[STEP 4] Opening message input...")

    click_at(
        MESSAGE_X,
        MESSAGE_Y,
        "Message Input",
        MESSAGE_WAIT
    )

    print("[TYPE] Preparing message...")
    print(f"[TYPE] Message: {MESSAGE}")

    # Clipboard method supports Persian, emojis,
    # and mixed Persian/English text.
    pyperclip.copy(MESSAGE)

    print("[TYPE] Pasting message...")

    pyautogui.hotkey("ctrl", "v")

    time.sleep(0.5)

    print("[SEND] Sending message...")

    pyautogui.press("enter")

    print("[SEND] Message sent successfully.")

    time.sleep(2)


# =========================================================
# Menu + Additional Messages
# =========================================================

MENU_X = 3037
MENU_Y = 1364

MESSAGES = [
    "سلام خوبی؟ 👋",
    "دوسداری به گروه آموزش کامپیوتر و خدمات کافی نت و پوستر و چاپ و لوازم التحریر و طراحی سایت و هوشمندسازی خانه و همه چی با قطعات و آی او تی و تکنولوژی ما بیای؟",
    "توی گروهمون آموزش‌ها، خدمات کامپیوتری، طراحی، چاپ، برنامه‌نویسی، آی او تی، هوشمندسازی خانه و کلی موضوع دیگه داریم 🚀",
    "اگه دوست داشتی خوشحال می‌شیم به جمعمون اضافه بشی ❤️",
    "آیدی گروه: آی او تو ایران سی اس"
]


def send_text(message):
    print(f"[TYPE] Sending message: {message}")

    pyperclip.copy(message)

    pyautogui.hotkey("ctrl", "v")

    time.sleep(0.7)

    pyautogui.press("enter")

    print("[SEND] Message sent.")

    time.sleep(2)


def open_menu_and_send_messages():
    print("[STEP 5] Opening menu...")

    click_at(
        MENU_X,
        MENU_Y,
        "Menu",
        2
    )

    print("[STEP 6] Sending additional messages...")

    for index, message in enumerate(MESSAGES, start=1):
        print(f"[MESSAGE {index}/{len(MESSAGES)}]")

        # Click message input before each message
        click_at(
            MESSAGE_X,
            MESSAGE_Y,
            "Message Input",
            0.5
        )

        send_text(message)

    print("[MESSAGES] All additional messages sent successfully.")


# =========================================================
# End Chat
# =========================================================

def end_chat():
    print("[STEP 5] Ending chat...")

    click_at(
        END_CHAT_X,
        END_CHAT_Y,
        "End Chat",
        END_CHAT_WAIT
    )

    print("[CHAT] Chat ended successfully.")


def click_on_end_chat():
    print("endhing chat...")

    click_at(
        end2_chat_x,
        end2_chat_y
    )


# =========================================================
# Main
# =========================================================

def main():
    print("========================================")
    print("       Telegram Automation")
    print("========================================")
    print()

    # Open Telegram
    if not open_telegram():
        print("[EXIT] Program stopped.")
        return

    print()
    print("[AUTOMATION] Starting...")

    # Search and open bot
    search_bot()

    # Click bot buttons
    click_bot_buttons()

    # Write and send first message
    write_message()

    # Open menu and send additional messages
    open_menu_and_send_messages()

    # End chat
    end_chat()

    print()
    print("========================================")
    print("[DONE] Automation completed successfully.")
    print("========================================")


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    main()