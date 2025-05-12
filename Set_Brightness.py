import screen_brightness_control as sbc
import argparse
def set_brightness(level):
    """
    Adjust the screen brightness to the specified level.
    :param level: Brightness level (0 to 100)
    """
    try:
        sbc.set_brightness(level)
        print(f"Brightness set to {level}%")
    except Exception as e:
        print(f"Failed to set brightness: {e}")

if __name__ == "__main__":
    # Example: Set brightness to 30%
    # set_brightness(30)
    parser = argparse.ArgumentParser(description="Set screen brightness.")
    parser.add_argument("--brightness", type=int, default=30, help="Set the brightness level (0 to 100)")
    args = parser.parse_args()
    set_brightness(args.brightness)