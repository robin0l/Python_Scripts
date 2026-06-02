import pyautogui
import random
import threading
import time
import keyboard

# Flag to control the running state of the script
running = True

# Get the screen width and height
screen_width, screen_height = pyautogui.size()

# Calculate the boundaries for mouse movement (50% of the screen size centered around the center)
center_x, center_y = screen_width // 2, screen_height // 2
movement_range_x = screen_width // 4  # 50% of the width centered around the center
movement_range_y = screen_height // 4  # 50% of the height centered around the center
min_x, max_x = center_x - movement_range_x, center_x + movement_range_x
min_y, max_y = center_y - movement_range_y, center_y + movement_range_y

# Function to move the mouse continuously and randomly within the limited area
def move_mouse_continuously():
    while running:
        x, y = pyautogui.position()  # Get the current mouse position
        dx = random.randint(-10, 10)  # Random small change in x
        dy = random.randint(-10, 10)  # Random small change in y
        new_x = max(min_x, min(max_x, x + dx))  # Constrain x within the boundaries
        new_y = max(min_y, min(max_y, y + dy))  # Constrain y within the boundaries
        pyautogui.moveTo(new_x, new_y)  # Move the mouse to the new position
        time.sleep(0.1)  # Small delay to control the speed of movement

# Function to stop the script when ESC is pressed
def check_for_esc():
    global running
    keyboard.wait('esc')
    running = False
    print("ESC key pressed. Stopping the script.")

# Function to type random characters on mouse click
def type_random_characters_on_click():
    while running:
        if pyautogui.mouseDown():  # Check if the mouse is clicked
            random_char = chr(random.randint(65, 90))  # Random uppercase letter
            pyautogui.typewrite(random_char)
            time.sleep()  # Small delay to prevent rapid typing
        time.sleep()  # Small delay to control the check frequency

# Start the mouse movement in a separate thread
mouse_thread = threading.Thread(target=move_mouse_continuously)
mouse_thread.daemon = True
mouse_thread.start()

# Start the ESC key listener in a separate thread
esc_thread = threading.Thread(target=check_for_esc)
esc_thread.daemon = True
esc_thread.start()

# Start the random character typing on click in a separate thread
typing_thread = threading.Thread(target=type_random_characters_on_click)
typing_thread.daemon = True
typing_thread.start()

# Your main script tasks
def main_script_tasks():
    while running:
        for i in range(10):
            if not running:
                break
            print(f"Performing task {i+1}")
            time.sleep(2)  # Simulate a task that takes 2 seconds
        if not running:
            break
    print("Main script tasks completed.")

if __name__ == "__main__":
    main_script_tasks()
    print("Script terminated.")
