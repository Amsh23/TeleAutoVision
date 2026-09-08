import time
import pyautogui


print("========================================")
print("      Mouse Position Detector")
print("========================================")
print()
print("Move your mouse to the target location.")
print("Press CTRL+C to stop.")
print()

try:
    while True:
        x, y = pyautogui.position()

        print(
            f"\rX = {x:4d} | Y = {y:4d}",
            end="",
            flush=True
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n")
    print("[EXIT] Position detector stopped.")