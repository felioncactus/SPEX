import pygame
import sys
import os
from tkinter import Tk, Button, messagebox, Text, Frame, Scrollbar, RIGHT, Y, END, LEFT, BOTH, Canvas, PhotoImage, Label
import tkinter as tk
import threading
import random
import keyword
import re
# Initialize Pygame
pygame.init()

# Fullscreen display
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Programming with Python Syntax and Loops")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)  # Color for spikes
SEMI_TRANSPARENT_GRID = (255, 255, 255, 50)  # Semi-transparent white

# Grid properties
GRID_SIZE = 50  # Define grid size
initial_robot_position = (100, 100)  # Initial position of the robot
robot = pygame.Rect(initial_robot_position[0] // GRID_SIZE * GRID_SIZE,
                    initial_robot_position[1] // GRID_SIZE * GRID_SIZE,  # Align to grid
                    GRID_SIZE, GRID_SIZE)
robot_speed = 2

# Obstacle and spikes lists
obstacles = []
spikes = []


# Global variables for robot state
robot_state = {"x": initial_robot_position[0], "y": initial_robot_position[1], "speed": 2, "is_on": True}
current_tool = "obstacle"  # Can be "obstacle" or "spike"
# Global variable to control robot's movement
stop_robot = False
finish_lines = []  # List to store finish line positions
execution_start_time = None  # Time when the robot starts executing code
robot_energy = 100
batteries = []
movement_blocks = []
sand_blocks = []
water_blocks = []
glass_blocks = []
box_blocks = []

def execute_code(user_code):
    """
    Execute the user-written Python-like code in a separate thread.
    """
    global robot_state, stop_robot
    global execution_start_time
    execution_start_time = pygame.time.get_ticks()
    # Define a limited environment for execution
    local_env = {
        "MoveLeft": lambda steps: move_robot(-50, 0, steps),
        "MoveRight": lambda steps: move_robot(50, 0, steps),
        "MoveUp": lambda steps: move_robot(0, -50, steps),
        "MoveDown": lambda steps: move_robot(0, 50, steps),
        "pickUP": pick_up_box,
        "placeIT": place_box,
        "robot_detect": robot_detect,
        "robot_state": robot_state,
        "math": __import__("math"),  # Allow the math library
        "wait": lambda ms: pygame.time.wait(ms),  # Add a wait function for delays
    }

    def execute():
        nonlocal user_code
        try:
            exec(user_code, {}, local_env)
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error in your code:\n{e}")

    # Run the user code in a new thread
    robot_thread = threading.Thread(target=execute, daemon=True)
    robot_thread.start()

def pick_up_box():
    """
    Allows the robot to pick up a box if it is next to one.
    """
    global robot, box_blocks, robot_state

    # Determine the robot's surrounding grid positions
    surrounding_positions = [
        (robot.x - GRID_SIZE, robot.y),
        (robot.x + GRID_SIZE, robot.y),
        (robot.x, robot.y - GRID_SIZE),
        (robot.x, robot.y + GRID_SIZE)
    ]

    for box in box_blocks:
        if (box.x, box.y) in surrounding_positions:
            robot_state["carrying_box"] = box  # Store the reference to the box being carried
            box_blocks.remove(box)  # Remove the box from the list to avoid duplicate rendering
            return  # Only pick up one box

    messagebox.showinfo("Pick Up Box", "No box found nearby to pick up.")

def place_box():
    """
    Allows the robot to place a box if it is carrying one.
    """
    global robot, box_blocks, robot_state

    if robot_state.get("carrying_box", False):
        carried_box = robot_state["carrying_box"]
        # Place the box next to the robot
        carried_box.x = robot.x + GRID_SIZE
        carried_box.y = robot.y
        box_blocks.append(carried_box)  # Add the box back to the list for rendering
        robot_state["carrying_box"] = None  # Clear the carrying state
    else:
        messagebox.showinfo("Place Box", "The robot is not carrying any box.")


def add_finish_line():
    """
    Allows placement of the finish line using the mouse.
    """
    global robot, stop_robot, execution_start_time
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x // GRID_SIZE * GRID_SIZE
    grid_y = mouse_y // GRID_SIZE * GRID_SIZE
    finish_lines.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
#Bk is here 2

def robot_detect(target_type):
    """
    Detects if the robot is next to a specified type of object (e.g., obstacle).
    Returns True if found, otherwise False.
    """
    global robot, obstacles, spikes, sand_blocks, water_blocks, glass_blocks, box_blocks, batteries, finish_lines

    # Determine the robot's surrounding grid positions
    surrounding_positions = [
        (robot.x - GRID_SIZE, robot.y),
        (robot.x + GRID_SIZE, robot.y),
        (robot.x, robot.y - GRID_SIZE),
        (robot.x, robot.y + GRID_SIZE)
    ]

    # Check for the target type in the surroundings
    objects = {
        "obstacle": obstacles,
        "spike": spikes,
        "sand": sand_blocks,
        "water": water_blocks,
        "glass": glass_blocks,
        "box": box_blocks,
        "battery": batteries,
        "finish": finish_lines
    }

    if target_type in objects:
        for obj in objects[target_type]:
            if (obj.x, obj.y) in [(pos[0], pos[1]) for pos in surrounding_positions]:
                return True

    return False


def move_robot(dx, dy, steps):
    """
    Move the robot by the specified delta (dx, dy) for a number of steps.
    Includes energy consumption and battery collection.
    """
    global robot, stop_robot, robot_energy, batteries

    for _ in range(steps):
        if robot_energy <= 0:  # Stop if energy is depleted
            stop_robot = True
            Tk().withdraw()  # Hide the root Tkinter window
            messagebox.showinfo("Out of Energy!", "The robot has run out of energy!")
            reset_game()  # Reset the game
            return  # Exit the function
        
        if stop_robot or robot_energy <= 0:  # Stop if no energy
            break

        
        pygame.time.wait(50)  # Delay for smooth movement
        new_robot = robot.move(dx, dy)

        # Align the robot's position to the nearest grid square
        new_robot.x = round(new_robot.x / GRID_SIZE) * GRID_SIZE
        new_robot.y = round(new_robot.y / GRID_SIZE) * GRID_SIZE

        # Check for movement blocks
        for block in movement_blocks:
            if new_robot.colliderect(block["rect"]):
                if block["type"] == "MoveRight":
                    dx, dy = 50, 0
                elif block["type"] == "MoveLeft":
                    dx, dy = -50, 0
                elif block["type"] == "MoveUp":
                    dx, dy = 0, -50
                elif block["type"] == "MoveDown":
                    dx, dy = 0, 50
                movement_blocks.remove(block)  # Remove block after execution
                break

        # Check for collision with sand (speed -x2, energy -5)
        for sand in sand_blocks:
            if new_robot.colliderect(sand):
                pygame.time.wait(150)
                robot_energy -= 5  # Decrease energy by 5
                break

        # Check for collision with water (speed -x4, energy -10)
        for water in water_blocks:
            if new_robot.colliderect(water):
                pygame.time.wait(350)
                robot_energy -= 10  # Decrease energy by 10
                break

        # Check for collision with glass (speed x4, energy -20)
        for glass in glass_blocks:
            if new_robot.colliderect(glass):
                robot_energy -= 20  # Decrease energy by 10
                glass_blocks.remove(glass)  # Remove glass block after interaction
                break

        # Check for collision with box (speed x4, energy -20)
        for box in box_blocks:
            if new_robot.colliderect(box):
                robot_energy -= 15  # Decrease energy by 10
                box_blocks.remove(box)  # Remove box block after interaction
                break

        # Check for collision with obstacles (block movement)
        if not any(new_robot.colliderect(obstacle) for obstacle in obstacles):
            robot = new_robot
            robot_energy -= 1  # Decrease energy on every step
        else:
            break  # Stop if there's an obstacle

        # Apply penalties for carrying a box
        if robot_state.get("carrying_box", False):
            robot_energy -= 5  # Additional penalty per step

        # Move the box with the robot if carrying one
        if robot_state.get("carrying_box", False):
            carried_box = robot_state["carrying_box"]
            carried_box.x = robot.x
            carried_box.y = robot.y

        # Check for collision with batteries (restore energy)
        for battery in batteries:
            if new_robot.colliderect(battery):
                robot_energy = min(robot_energy + 20, 100)  # Add energy, max 100
                batteries.remove(battery)  # Remove the battery
                break

        # Check for collision with spikes (reset position)
        if any(new_robot.colliderect(spike) for spike in spikes):
            robot.x, robot.y = initial_robot_position
            break

        # Check for collision with finish lines (victory)
        if any(new_robot.colliderect(finish) for finish in finish_lines):
            stop_robot = True
            execution_time = pygame.time.get_ticks() - execution_start_time
            execution_time_seconds = execution_time / 1000.0
            Tk().withdraw()  # Hide the root Tkinter window
            messagebox.showinfo("FINISH!", f"Robot reached the finish line in {execution_time_seconds:.2f} seconds!")
            reset_game()  # Call reset_game after the message box closes
            break

def execute_environment_code(user_code):
    """
    Execute the user-written Python-like code for the environment in a separate thread.
    """
    global obstacles, spikes, batteries, sand_blocks, water_blocks, glass_blocks, box_blocks, movement_blocks

    # Define a limited environment for execution
    local_env = {
        "place": place_tool,
        "remove": remove_tool,
        "grid_size": GRID_SIZE,
        "WIDTH": WIDTH,  # Expose the game width
        "HEIGHT": HEIGHT,  # Expose the game height
        "wait": lambda ms: pygame.time.wait(ms),  # Add a wait function for delays
    }

    def execute():
        nonlocal user_code
        try:
            exec(user_code, {}, local_env)
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error in your code:\n{e}")

    # Run the user code in a new thread
    environment_thread = threading.Thread(target=execute, daemon=True)
    environment_thread.start()

def place_tool(tool, x, y):
    """
    Places the specified tool at the given grid coordinates.
    """
    global obstacles, spikes, batteries, sand_blocks, water_blocks, glass_blocks, box_blocks, movement_blocks

    grid_x = x * GRID_SIZE
    grid_y = y * GRID_SIZE
    rect = pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE)

    if tool == "obstacle":
        obstacles.append(rect)
    elif tool == "spike":
        spikes.append(rect)
    elif tool == "battery":
        batteries.append(rect)
    elif tool == "sand":
        sand_blocks.append(rect)
    elif tool == "water":
        water_blocks.append(rect)
    elif tool == "glass":
        glass_blocks.append(rect)
    elif tool == "box":
        box_blocks.append(rect)
    elif tool in ["MoveRight", "MoveLeft", "MoveUp", "MoveDown"]:
        movement_blocks.append({"type": tool, "rect": rect})

def remove_tool(tool, x, y):
    """
    Removes the specified tool at the given grid coordinates.
    """
    global obstacles, spikes, batteries, sand_blocks, water_blocks, glass_blocks, box_blocks, movement_blocks

    grid_x = x * GRID_SIZE
    grid_y = y * GRID_SIZE

    def remove_from_list(lst):
        for obj in lst:
            if obj.x == grid_x and obj.y == grid_y:
                lst.remove(obj)
                break

    if tool == "obstacle":
        remove_from_list(obstacles)
    elif tool == "spike":
        remove_from_list(spikes)
    elif tool == "battery":
        remove_from_list(batteries)
    elif tool == "sand":
        remove_from_list(sand_blocks)
    elif tool == "water":
        remove_from_list(water_blocks)
    elif tool == "glass":
        remove_from_list(glass_blocks)
    elif tool == "box":
        remove_from_list(box_blocks)
    elif tool in ["MoveRight", "MoveLeft", "MoveUp", "MoveDown"]:
        for block in movement_blocks:
            if block["rect"].x == grid_x and block["rect"].y == grid_y:
                movement_blocks.remove(block)
                break

def open_environment_program_window():
    """
    Opens a Tkinter window for programming the environment with syntax highlighting and proper auto-indent.
    """
    python_keywords = set(keyword.kwlist)  # Python's reserved keywords
    operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
    delimiters = {'(', ')', '{', '}', '[', ']', ':', ',', '.'}

    def submit_code():
        input_code = text_editor.get("1.0", "end").strip()
        root.destroy()
        execute_environment_code(input_code)

    def update_line_numbers(event=None):
        """Updates the line numbers to accurately reflect the lines in the text editor."""
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", END)

        # Generate line numbers
        lines = text_editor.index("end-1c").split(".")[0]
        line_number_content = "\n".join(str(i) for i in range(1, int(lines) + 1))
        line_numbers.insert("1.0", line_number_content)

        line_numbers.config(state="disabled")

    def handle_tab(event):
        """Handles the Tab key to insert spaces instead of a Tab character."""
        text_editor.insert("insert", " " * 4)
        return "break"

    def auto_indent(event):
        """Automatically adds an indentation after a colon."""
        current_line = text_editor.get("insert linestart", "insert")
        if current_line.strip().endswith(":"):
            indentation = len(current_line) - len(current_line.lstrip())
            text_editor.insert("insert", "\n" + " " * (indentation + 4))
            return "break"

    def apply_syntax_highlighting(event=None):
        """Applies syntax highlighting to the content of the text editor."""
        text_editor.tag_remove("Keyword", "1.0", END)
        text_editor.tag_remove("String", "1.0", END)
        text_editor.tag_remove("Comment", "1.0", END)
        text_editor.tag_remove("Operator", "1.0", END)
        text_editor.tag_remove("Delimiter", "1.0", END)

        content = text_editor.get("1.0", "end-1c")

        for kw in python_keywords:
            for match in re.finditer(rf'\b{kw}\b', content):
                start, end = match.span()
                start_index = f"1.0 + {start}c"
                end_index = f"1.0 + {end}c"
                text_editor.tag_add("Keyword", start_index, end_index)

        for match in re.finditer(r'(["\'])(?:(?=(\\?))\2.)*?\1', content):
            start, end = match.span()
            start_index = f"1.0 + {start}c"
            end_index = f"1.0 + {end}c"
            text_editor.tag_add("String", start_index, end_index)

        for match in re.finditer(r'#.*', content):
            start, end = match.span()
            start_index = f"1.0 + {start}c"
            end_index = f"1.0 + {end}c"
            text_editor.tag_add("Comment", start_index, end_index)

        for op in operators:
            for match in re.finditer(re.escape(op), content):
                start, end = match.span()
                start_index = f"1.0 + {start}c"
                end_index = f"1.0 + {end}c"
                text_editor.tag_add("Operator", start_index, end_index)

        for delim in delimiters:
            for match in re.finditer(re.escape(delim), content):
                start, end = match.span()
                start_index = f"1.0 + {start}c"
                end_index = f"1.0 + {end}c"
                text_editor.tag_add("Delimiter", start_index, end_index)

    root = Tk()
    root.title("Program Environment")
    root.geometry("900x500")
    root.configure(bg="#000B58")

    # Set window icon
    try:
        root.iconbitmap("textures/icons/icon.ico")  # Ensure "icon.ico" is in the same directory
    except Exception as e:
        print("Icon file not found:", e)

    # Frame for editor and line numbers
    editor_frame = Frame(root, bg="#000B58")
    editor_frame.pack(fill=BOTH, expand=True)

    # Line numbers
    line_numbers = Text(
        editor_frame, 
        width=4, 
        bg="#003161", 
        fg="#FF8000", 
        state="disabled", 
        padx=5, 
        pady=5
    )
    line_numbers.pack(side=LEFT, fill=Y)

    # Text editor with scrollbar
    scrollbar = Scrollbar(editor_frame, bg="#000B58", troughcolor="#003161", activebackground="#000B58")
    scrollbar.pack(side=RIGHT, fill=Y)

    text_editor = Text(
        editor_frame, 
        wrap="none", 
        yscrollcommand=scrollbar.set, 
        undo=True, 
        bg="#000B58", 
        fg="white", 
        insertbackground="white"
    )
    text_editor.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=text_editor.yview)

    text_editor.tag_config("Keyword", foreground="#FFD700")
    text_editor.tag_config("String", foreground="#00FF00")
    text_editor.tag_config("Comment", foreground="#A9A9A9")
    text_editor.tag_config("Operator", foreground="#FFA500")
    text_editor.tag_config("Delimiter", foreground="#87CEEB")

    text_editor.bind("<KeyRelease>", update_line_numbers)
    text_editor.bind("<KeyRelease>", apply_syntax_highlighting, add="+")
    text_editor.bind("<Tab>", handle_tab)  # Bind Tab key for spaces
    text_editor.bind("<Return>", auto_indent)  # Bind Enter key for auto-indent

    # Run button
    btn = Button(
        root, 
        text="RUN", 
        command=submit_code, 
        bg="#FF0000", 
        fg="white", 
        font=("Arial", 10, "bold"),  # Bold font style
        activebackground="#B20000", 
        activeforeground="white",
        relief="flat",  # Flat button style
        padx=10,  # Padding for width
        pady=5   # Padding for height
        
    )

        # Hover effect
    def on_hover(event):
        btn.config(bg="#C13E24")  # Darker shade on hover

    def on_leave(event):
        btn.config(bg="#FF0000")  # Original color when not hovering

    btn.bind("<Enter>", on_hover)  # Mouse enters
    btn.bind("<Leave>", on_leave)  # Mouse leaves
    btn.pack(side=RIGHT, padx=10, pady=10)

    update_line_numbers()
    apply_syntax_highlighting()

    root.mainloop()

def reset_game():
    """
    Relaunch the current script to reset the game after cleaning up.
    """
    global stop_robot

    # Stop any active threads
    stop_robot = True
    threading._shutdown()  # Force a cleanup of threads if necessary

    # Reset global variables if needed
    reset_robot_position()
    obstacles.clear()
    spikes.clear()

    # Relaunch the script
    python = sys.executable
    os.execl(python, python, *sys.argv)


def open_program_window():
    """
    Opens a Tkinter window for programming the robot with syntax highlighting and proper auto-indent.
    """
    python_keywords = set(keyword.kwlist)  # Python's reserved keywords
    operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
    delimiters = {'(', ')', '{', '}', '[', ']', ':', ',', '.'}

    def close_window():
        root.destroy()

    def submit_code():
        input_code = text_editor.get("1.0", "end").strip()
        root.destroy()
        execute_code(input_code)

    def update_line_numbers(event=None):
        """Updates the line numbers to accurately reflect the lines in the text editor."""
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", END)

        # Generate line numbers
        lines = text_editor.index("end-1c").split(".")[0]
        line_number_content = "\n".join(str(i) for i in range(1, int(lines) + 1))
        line_numbers.insert("1.0", line_number_content)

        line_numbers.config(state="disabled")

    def handle_tab(event):
        """Handles the Tab key to insert spaces instead of a Tab character."""
        text_editor.insert("insert", " " * 4)
        return "break"

    def auto_indent(event):
        """Automatically adds an indentation after a colon."""
        current_line = text_editor.get("insert linestart", "insert")
        if current_line.strip().endswith(":"):
            indentation = len(current_line) - len(current_line.lstrip())
            text_editor.insert("insert", "\n" + " " * (indentation + 4))
            return "break"

    def apply_syntax_highlighting(event=None):
        """Applies syntax highlighting to the content of the text editor."""
        text_editor.tag_remove("Keyword", "1.0", END)
        text_editor.tag_remove("String", "1.0", END)
        text_editor.tag_remove("Comment", "1.0", END)
        text_editor.tag_remove("Operator", "1.0", END)
        text_editor.tag_remove("Delimiter", "1.0", END)

        content = text_editor.get("1.0", "end-1c")

        for kw in python_keywords:
            for match in re.finditer(rf'\b{kw}\b', content):
                start, end = match.span()
                start_index = f"1.0 + {start}c"
                end_index = f"1.0 + {end}c"
                text_editor.tag_add("Keyword", start_index, end_index)

        for match in re.finditer(r'(["\'])(?:(?=(\\?))\2.)*?\1', content):
            start, end = match.span()
            start_index = f"1.0 + {start}c"
            end_index = f"1.0 + {end}c"
            text_editor.tag_add("String", start_index, end_index)

        for match in re.finditer(r'#.*', content):
            start, end = match.span()
            start_index = f"1.0 + {start}c"
            end_index = f"1.0 + {end}c"
            text_editor.tag_add("Comment", start_index, end_index)

        for op in operators:
            for match in re.finditer(re.escape(op), content):
                start, end = match.span()
                start_index = f"1.0 + {start}c"
                end_index = f"1.0 + {end}c"
                text_editor.tag_add("Operator", start_index, end_index)

        for delim in delimiters:
            for match in re.finditer(re.escape(delim), content):
                start, end = match.span()
                start_index = f"1.0 + {start}c"
                end_index = f"1.0 + {end}c"
                text_editor.tag_add("Delimiter", start_index, end_index)

    root = Tk()
    root.title("Program Robot")
    root.geometry("900x500")
    root.configure(bg="#000B58")
    #root.overrideredirect(True)  # Hide the title bar

    # Set window icon
    try:
        root.iconbitmap("textures/icons/icon.ico")  # Ensure "icon.ico" is in the same directory
    except Exception as e:
        print("Icon file not found:", e)

    # Frame for editor and line numbers
    editor_frame = Frame(root, bg="#000B58")
    editor_frame.pack(fill=BOTH, expand=True)

    # Line numbers
    line_numbers = Text(
        editor_frame, 
        width=4, 
        bg="#003161", 
        fg="#FF8000", 
        state="disabled", 
        padx=5, 
        pady=5
    )
    line_numbers.pack(side=LEFT, fill=Y)

    # Text editor with scrollbar
    scrollbar = Scrollbar(editor_frame, bg="#000B58", troughcolor="#003161", activebackground="#000B58", highlightthickness=0)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_editor = Text(
        editor_frame, 
        wrap="none", 
        yscrollcommand=scrollbar.set, 
        undo=True, 
        bg="#000B58", 
        fg="white", 
        insertbackground="white"
    )
    text_editor.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=text_editor.yview)

    text_editor.tag_config("Keyword", foreground="#FFD700")
    text_editor.tag_config("String", foreground="#00FF00")
    text_editor.tag_config("Comment", foreground="#A9A9A9")
    text_editor.tag_config("Operator", foreground="#FFA500")
    text_editor.tag_config("Delimiter", foreground="#87CEEB")

    text_editor.bind("<KeyRelease>", update_line_numbers)
    text_editor.bind("<KeyRelease>", apply_syntax_highlighting, add="+")
    text_editor.bind("<Tab>", handle_tab)  # Bind Tab key for spaces
    text_editor.bind("<Return>", auto_indent)  # Bind Enter key for auto-indent

    # Run button
    btn = Button(
        root, 
        text="RUN", 
        command=submit_code, 
        bg="#FF0000", 
        fg="white", 
        font=("Arial", 10, "bold"),  # Bold font style
        activebackground="#B20000", 
        activeforeground="white",
        relief="flat",  # Flat button style
        padx=10,  # Padding for width
        pady=5   # Padding for height
        
    )

        # Hover effect
    def on_hover(event):
        btn.config(bg="#C13E24")  # Darker shade on hover

    def on_leave(event):
        btn.config(bg="#FF0000")  # Original color when not hovering

    btn.bind("<Enter>", on_hover)  # Mouse enters
    btn.bind("<Leave>", on_leave)  # Mouse leaves
    btn.pack(side=RIGHT, padx=10, pady=10)

    # Close button
    btnCLOSE = Button(
        root, 
        text="CLOSE", 
        command=close_window, 
        bg="#62825D", 
        fg="white", 
        font=("Arial", 10, "bold"),  # Bold font style
        activebackground="#62825D", 
        activeforeground="white",
        relief="flat",  # Flat button style
        padx=10,  # Padding for width
        pady=5   # Padding for height
        
    )

        # Hover effect
    def on_hover(event):
        btnCLOSE.config(bg="#526E48")  # Darker shade on hover

    def on_leave(event):
        btnCLOSE.config(bg="#62825D")  # Original color when not hovering

    btnCLOSE.bind("<Enter>", on_hover)  # Mouse enters
    btnCLOSE.bind("<Leave>", on_leave)  # Mouse leaves
    btnCLOSE.pack(side=LEFT, padx=10, pady=10)

    update_line_numbers()
    apply_syntax_highlighting()

    root.mainloop()

def generate_level():
    """
    Generates a maze-like level with a variety of tools, obstacles, and blocks.
    Ensures a path from the start to the finish and uses all block types.
    """
    global obstacles, spikes, batteries, water_blocks, sand_blocks, glass_blocks, box_blocks, finish_lines, robot

    # Clear existing tools on the map
    obstacles.clear()
    spikes.clear()
    batteries.clear()
    water_blocks.clear()
    sand_blocks.clear()
    glass_blocks.clear()
    box_blocks.clear()
    finish_lines.clear()

    # Define the grid dimensions
    num_columns = WIDTH // GRID_SIZE
    num_rows = HEIGHT // GRID_SIZE

    # Create a grid to track visited cells for pathfinding
    grid = [[0 for _ in range(num_columns)] for _ in range(num_rows)]
    stack = []

    # Start position (top-left corner)
    start_x, start_y = 0, 0
    grid[start_y][start_x] = 1  # Mark the start cell as part of the path
    stack.append((start_x, start_y))

    # DFS maze generation
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < num_columns and 0 <= ny < num_rows and grid[ny][nx] == 0:
                # Count the number of adjacent path cells
                adjacent_count = sum(1 for ddx, ddy in directions if 0 <= nx + ddx < num_columns and 0 <= ny + ddy < num_rows and grid[ny + ddy][nx + ddx] == 1)
                if adjacent_count == 1:
                    neighbors.append((nx, ny))

        if neighbors:
            next_x, next_y = random.choice(neighbors)
            grid[next_y][next_x] = 1
            stack.append((next_x, next_y))
        else:
            stack.pop()

    # Place obstacles, tools, and box blocks based on the maze structure
    for row in range(num_rows):
        for col in range(num_columns):
            if grid[row][col] == 0:  # Wall cell
                if random.random() < 0.3:  # Higher probability for placing obstacles
                    obstacles.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:  # Path cell
                if random.random() < 0.1:  # Probability for placing spikes
                    spikes.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif random.random() < 0.1:  # Probability for placing water
                    water_blocks.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif random.random() < 0.1:  # Probability for placing batteries
                    batteries.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif random.random() < 0.1:  # Probability for placing sand blocks
                    sand_blocks.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif random.random() < 0.1:  # Probability for placing glass blocks
                    glass_blocks.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif random.random() < 0.05:  # Probability for placing box blocks
                    box_blocks.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Ensure a finish line is placed on a path cell
    while True:
        finish_x = random.randint(0, num_columns - 1)
        finish_y = random.randint(0, num_rows - 1)
        if grid[finish_y][finish_x] == 1 and (finish_x, finish_y) != (0, 0):  # Not at the start
            finish_lines.append(pygame.Rect(finish_x * GRID_SIZE, finish_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            break

    # Place the robot at the start position
    robot = pygame.Rect(start_x * GRID_SIZE, start_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

    # Print confirmation
    print(f"Level generated with {len(obstacles)} obstacles, {len(spikes)} spikes, "
          f"{len(water_blocks)} water blocks, {len(batteries)} batteries, {len(sand_blocks)} sand blocks, "
          f"{len(glass_blocks)} glass blocks, {len(box_blocks)} box blocks, and 1 finish line.")


def open_tool_menu():
    """
    Opens a Tkinter menu for selecting a tool (obstacle, spike, finish line, battery, or movement block)
    with flat buttons, bold text, icons, and multi-column layout.
    """
    def set_tool(tool):
        global current_tool
        current_tool = tool
        tool_window.destroy()

    # Create the main tool window
    tool_window = Tk()
    tool_window.title("Select Tool")
    tool_window.geometry("350x620")
    tool_window.configure(bg="#f0f0f0")

        # Set window icon
    try:
        tool_window.iconbitmap("textures/icons/tools.ico")  # Ensure "icon.ico" is in the same directory
    except Exception as e:
        print("Icon file not found:", e)

    # Icons for tools (ensure these paths point to your actual icons)
    icons = {
        "obstacle": PhotoImage(file="textures/blocks/obstacle.png"),
        "spike": PhotoImage(file="textures/blocks/spike.png"),
        "finish": PhotoImage(file="textures/blocks/finish.png"),
        "battery": PhotoImage(file="textures/blocks/battery.png"),
        "MoveRight": PhotoImage(file="textures/blocks/moveRight.png"),
        "MoveLeft": PhotoImage(file="textures/blocks/moveLeft.png"),
        "MoveUp": PhotoImage(file="textures/blocks/moveUp.png"),
        "MoveDown": PhotoImage(file="textures/blocks/moveDown.png"),
        "sand": PhotoImage(file="textures/blocks/sand.png"),
        "water": PhotoImage(file="textures/blocks/water.png"),
        "glass": PhotoImage(file="textures/blocks/glass.png"),
        "box": PhotoImage(file="textures/blocks/box.png"),
        "generate": PhotoImage(file="textures/blocks/generate.png"),
    }

    # Tool configuration (text, icon key)
    tools = [
        ("Obstacle", "obstacle"),
        ("Spike", "spike"),
        ("Finish Line", "finish"),
        ("Battery", "battery"),
        ("Move Right", "MoveRight"),
        ("Move Left", "MoveLeft"),
        ("Move Up", "MoveUp"),
        ("Move Down", "MoveDown"),
        ("Sand", "sand"),
        ("Water", "water"),
        ("Glass", "glass"),
        ("Box", "box"),
    ]

    # Add buttons in a grid layout
    for idx, (label, icon_key) in enumerate(tools):
        row = idx // 3  # 3 buttons per row
        col = idx % 3   # Column index
        btn = Button(
            tool_window,
            text=label,
            image=icons[icon_key],  # Add the corresponding icon
            compound="top",  # Display the icon above the text
            command=lambda tool=icon_key: set_tool(tool),
            relief="flat",
            font=("Arial", 10, "bold"),  # Bold text
            bg="#e0e0e0",
            fg="black",
            activebackground="#d0d0d0",
            activeforeground="black",
            padx=10,
            pady=10,
        )
        btn.grid(row=row, column=col, padx=10, pady=10)

    # Ensure the "Generate Level" button has its specific command
    generate_button = Button(
        tool_window,
        text="Generate Level",
        image=icons["generate"],
        compound="top",
        command=generate_level,
        relief="flat",
        font=("Arial", 10, "bold"),
        bg="#e0e0e0",
        fg="black",
        activebackground="#d0d0d0",
        activeforeground="black",
        padx=10,
        pady=10,
    )
    generate_button.grid(row=(len(tools) // 3), column=0, columnspan=3, pady=10)

    
    tool_window.mainloop()

def draw_grid():
    """
    Draw a semi-transparent grid on the background.
    """
    grid_spacing = GRID_SIZE  # Grid spacing in pixels
    grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH, grid_spacing):
        pygame.draw.line(grid_surface, SEMI_TRANSPARENT_GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, grid_spacing):
        pygame.draw.line(grid_surface, SEMI_TRANSPARENT_GRID, (0, y), (WIDTH, y))
    screen.blit(grid_surface, (0, 0))

def reset_robot_position():
    """
    Resets the robot to its initial starting position.
    """
    global robot, robot_state
    robot.x, robot.y = initial_robot_position
    robot_state["x"], robot_state["y"] = initial_robot_position
    update_display()  # Redraw the display with the new robot position

def update_display():
    """
    Updates the Pygame display with the current robot state.
    """
    screen.fill(BLACK)

    # Draw grid
    draw_grid()

    # Draw obstacles
    obstacle_image = pygame.image.load('textures/blocks/obstacle.png')
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle)

    # Draw spikes
    spike_image = pygame.image.load('textures/blocks/spike.png')
    for spike in spikes:
        screen.blit(spike_image, spike)

    # Draw Finish
    finish_image = pygame.image.load('textures/blocks/finish.png')
    for finish in finish_lines:
        screen.blit(finish_image, finish)

    # Draw batteries battery
    battery_image = pygame.image.load('textures/blocks/battery.png')
    for battery in batteries:
        screen.blit(battery_image, battery)


    # Draw sand blocks (e.g., yellow color)
    sand_image = pygame.image.load('textures/blocks/sand.png')
    for sand in sand_blocks:
        screen.blit(sand_image, sand)

    # Draw water blocks (e.g., blue color)
    water_image = pygame.image.load('textures/blocks/water.png')
    for water in water_blocks:
        screen.blit(water_image, water)

    # Draw glass blocks (e.g., white color)
    glass_image = pygame.image.load('textures/blocks/glass.png')
    for glass in glass_blocks:
        screen.blit(glass_image, glass)

    # Draw box blocks (e.g., brown color)
    box_image = pygame.image.load('textures/blocks/box.png')
    for box in box_blocks:
        screen.blit(box_image, box)

    # Draw movement blocks
    moveUP_image = pygame.image.load('textures/blocks/moveUp.png') #Up
    moveDown_image = pygame.image.load('textures/blocks/moveDown.png') #Down
    moveLeft_image = pygame.image.load('textures/blocks/moveLeft.png') #Left
    moveRight_image = pygame.image.load('textures/blocks/moveRight.png') #Right
    for block in movement_blocks:
        if block["type"] == "MoveRight":
            image = moveRight_image
        elif block["type"] == "MoveLeft":
            image = moveLeft_image
        elif block["type"] == "MoveUp":
            image = moveUP_image
        elif block["type"] == "MoveDown":
            image = moveDown_image

        # Draw the image for the block
        screen.blit(image, block["rect"].topleft)  # Use .topleft to position the image correctly


    # Draw the robot
    robot_image = pygame.image.load('textures/Robot.png')
    screen.blit(robot_image, robot)


    # Display energy level
    font = pygame.font.SysFont(None, 36)
    energy_text = font.render(f"Energy: {robot_energy}%", True, WHITE)
    screen.blit(energy_text, (20, 60))


    # Draw the title
    font = pygame.font.SysFont(None, 48)
    title_text = font.render("Sand Box Zone", True, WHITE)
    screen.blit(title_text, (20, 20))

    # Draw instruction text in the bottom-right corner
    font = pygame.font.SysFont(None, 28)  # Slightly smaller font for instructions
    instruction_text = (
        "Press: T for (Tools Menu), E for (Environment Programming), "
        "P for (Robot Programming), [X] for EXIT, [O] for robot pos reload, [^] for entire game reload"
    )
    rendered_text = font.render(instruction_text, True, WHITE)

    # Calculate the position for the bottom-right corner
    text_width, text_height = font.size(instruction_text)
    text_x = WIDTH - text_width - 20  # 20px padding from the right
    text_y = HEIGHT - text_height - 20  # 20px padding from the bottom

    # Draw the text onto the screen
    screen.blit(rendered_text, (text_x, text_y))


    # Draw the reset button
    resetRobot_image = pygame.image.load('textures/buttons/reloadPosBTN.png')
    resetRobot_image = pygame.transform.scale(resetRobot_image, (50, 50))  # Resize to fit grid
    screen.blit(resetRobot_image, (1750, 50))  # Position at (35, 1) on the grid

    # Draw the reset game button
    resetGAME_image = pygame.image.load('textures/buttons/reloadGameBTN.png')
    resetGAME_image = pygame.transform.scale(resetGAME_image, (50, 50))  # Resize to fit grid
    screen.blit(resetGAME_image, (1800, 50))  # Position at (36, 1) on the grid

    # Display current tool information
    font = pygame.font.SysFont(None, 36)
    current_tool_text = font.render(f"Current Tool: {current_tool}", True, WHITE)
    screen.blit(current_tool_text, (20, HEIGHT - 80))  # Adjust the position as needed

    # Draw mouse coordinates as grid square indices
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x // GRID_SIZE
    grid_y = mouse_y // GRID_SIZE
    coord_text = pygame.font.SysFont(None, 36).render(f"X:{grid_x}, Y:{grid_y}", True, WHITE)
    screen.blit(coord_text, (20, HEIGHT - 40))

# Highlight the borders of the cell under the cursor
    hover_rect = pygame.Rect(grid_x * GRID_SIZE, grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, (255, 255, 255), hover_rect, 3)  # White border with 3-pixel width

    # Draw the exit button
    EXITbtn_image = pygame.image.load('textures/buttons/exitBTN.png')
    EXITbtn_image = pygame.transform.scale(EXITbtn_image, (50, 50))  # Resize to fit grid
    screen.blit(EXITbtn_image, (1850, 50))  # Position at (37, 1) on the grid

    # Draw mouse cursor as a cross
    pygame.draw.line(screen, WHITE, (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2)
    pygame.draw.line(screen, WHITE, (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2)

    pygame.display.flip()


# Hide the system mouse cursor
pygame.mouse.set_visible(False)

# Main loop
running = True
clock = pygame.time.Clock()  # Pygame clock for controlling frame rate
robot_moving = False
while running:
    screen.fill(BLACK)  # Clear the screen for the next frame

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Press 'P' to program the robot
                open_program_window()
            elif event.key == pygame.K_t:  # Press 'T' to open tool menu
                open_tool_menu()
            elif event.key == pygame.K_e:  # Press 'E' to program the environment
                open_environment_program_window()
            elif event.key == pygame.K_s:  # Press 'S' to stop/start the robot
                stop_robot = not stop_robot  # Toggle the stop state of the robot
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if 1850 < mouse_x < 1900 and 50 < mouse_y < 100:
                running = False  # Exit button
            elif 1750 < mouse_x < 1800 and 50 < mouse_y < 100:
                reset_robot_position()  # Reset Robot Position button
            elif 1800 < mouse_x < 1850 and 50 < mouse_y < 100:
                reset_game()  # Reload

            else:
                grid_x = mouse_x // GRID_SIZE * GRID_SIZE
                grid_y = mouse_y // GRID_SIZE * GRID_SIZE

                if event.button == 1:  # Left mouse button to add obstacle or spike
                    if current_tool == "obstacle":
                        obstacles.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))  # Same size as the robot
                    elif current_tool == "spike":
                        spikes.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))  # Same size as the robot
                    elif current_tool == "finish":
                        finish_lines.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
                    elif current_tool == "battery":
                        batteries.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
                    elif current_tool == "water":
                        water_blocks.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
                    elif current_tool == "sand":
                        sand_blocks.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
                    elif current_tool == "glass":
                        glass_blocks.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
                    elif current_tool == "box":
                        box_blocks.append(pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE))
                    elif current_tool in ["MoveRight", "MoveLeft", "MoveUp", "MoveDown"]:
                        movement_blocks.append({"type": current_tool, "rect": pygame.Rect(grid_x, grid_y, GRID_SIZE, GRID_SIZE)})
                elif event.button == 3:  # Right mouse button to remove obstacle or spike
                    if current_tool == "obstacle":
                        for obstacle in obstacles:
                            if obstacle.collidepoint(mouse_x, mouse_y):
                                obstacles.remove(obstacle)
                                break
                    elif current_tool == "spike":
                        for spike in spikes:
                            if spike.collidepoint(mouse_x, mouse_y):
                                spikes.remove(spike)
                                break
                    elif current_tool == "finish":
                        for finish in finish_lines:
                            if finish.collidepoint(mouse_x, mouse_y):
                                finish_lines.remove(finish)
                                break
                    elif current_tool == "battery":
                        for battery in batteries:
                            if battery.collidepoint(mouse_x, mouse_y):
                                batteries.remove(battery)
                                break
                    elif current_tool in ["MoveRight", "MoveLeft", "MoveUp", "MoveDown"]:
                        for block in movement_blocks:
                            if block["rect"].collidepoint(mouse_x, mouse_y):
                                movement_blocks.remove(block)
                                break  # Remove the block and break the loop
                    elif current_tool == "sand":
                        for sand in sand_blocks:
                            if sand.collidepoint(mouse_x, mouse_y):
                                sand_blocks.remove(sand)
                                break
                    elif current_tool == "water":
                        for water in water_blocks:
                            if water.collidepoint(mouse_x, mouse_y):
                                water_blocks.remove(water)
                                break
                    elif current_tool == "glass":
                        for glass in glass_blocks:
                            if glass.collidepoint(mouse_x, mouse_y):
                                glass_blocks.remove(glass)
                                break
                    elif current_tool == "box":
                        for box in box_blocks:
                            if box.collidepoint(mouse_x, mouse_y):
                                box_blocks.remove(box)
                                break
    # Update robot position if it's moving
    if not stop_robot:
        robot_moving = True  # Use a flag to indicate the robot is executing code

    # Draw the grid, obstacles, and other elements
    update_display()

    # Limit the frame rate for smoother visuals
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
sys.exit()
