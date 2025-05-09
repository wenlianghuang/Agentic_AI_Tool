import pyautogui
import time

# 等待一秒，確保使用者準備好
time.sleep(1)

# 模擬按下 Win + G 快捷鍵
pyautogui.hotkey('win', 'g')

print("已模擬按下 Win + G 開啟 Xbox Game Bar。")