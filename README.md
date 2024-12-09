# SPEX - Spirit of Exploration

Welcome to the wonderful world of programming! SPEX is a game designed to introduce beginners (just like me) to the basics of coding in a fun and interactive way. Whether you want to program a robot or design an environment, this game has something for you.

#### Core Philosophy
This project is built on two core principles:

1. **Learning by Doing**: The best way to learn is through hands-on experience. Dive in, make mistakes, and learn as you go!
   
2. **Adaptability**: Programming teaches us to handle both fixed ("hard-coded") solutions and flexible, adaptable systems. For example, imagine programming a robot to navigate a maze. You could give it an exact step-by-step algorithm, but what happens if the maze changes? Alternatively, you could create a program that allows the robot to adapt and find the finish line on its own. That’s the spirit of exploration we’re aiming for!

---

### How to Program a Robot 101

This tutorial will guide you through programming your new robotic friend, R1! Don’t worry; it’s beginner-friendly and uses Python, a language known for its simplicity and power.

#### Meet R1
R1 is waiting for you to take control. Press **P** on your keyboard to open the programming window. Here, you can write commands for R1 and click the **Run** button to execute them.

#### Basic Commands
Here are the commands R1 understands:

- **MoveLeft(steps)**: Moves left by the specified number of steps.
- **MoveRight(steps)**: Moves right by the specified number of steps.
- **MoveUp(steps)**: Moves up by the specified number of steps.
- **MoveDown(steps)**: Moves down by the specified number of steps.
- **pickUP()**: Picks up a box.
- **placeIT()**: Places a box.
- **robot_detect(item)**: Detects specific items or obstacles.
- **wait(ms)**: Pauses for the specified time (in milliseconds).

**Note**: Each movement consumes energy, so plan your actions wisely. You’ll learn how to recharge energy later.

#### Example: Move Your Robot
Try moving R1 around:

```python
MoveRight(3)
MoveDown(2)
```

**Challenge**: Place a box at coordinates (5, 2), pick it up, and move it to (7, 4). Use the cursor to find coordinates and plan your algorithm.

---

### Programming Concepts: Conditions and Loops

To make R1 smarter, you’ll need to learn some basic programming concepts:

#### Conditional Statements
Conditional statements help R1 react to its environment. For example:

```python
if robot_detect("obstacle"):
    MoveDown(1)
elif robot_detect("water"):
    MoveLeft(1)
else:
    MoveRight(1)
```

#### Loops
Loops allow R1 to repeat tasks efficiently. Python supports two main types of loops:

- **While Loops**: Repeat while a condition is true.

```python
steps = 0
while steps < 5:
    MoveRight(1)
    steps += 1
```

- **For Loops**: Repeat a set number of times.

```python
for i in range(5):
    if robot_detect("obstacle"):
        MoveDown(1)
    else:
        MoveRight(1)
```

**Tip**: Comments (lines starting with `#`) are ignored by the robot but help you understand your code.

---

### How to Program an Environment 101

Programming the environment is just as fun! Press **E** on your keyboard to open the environment editor. Here are the new commands:

- **place(item, x, y)**: Places an item at specified coordinates.
- **remove(item, x, y)**: Removes an item from specified coordinates.
- **wait(ms)**: Pauses for the specified time.

#### Example: Randomized Battery Placement
Here’s how to place and remove a battery randomly:

```python
import random

while True:
    x = random.randint(0, WIDTH // grid_size - 1)
    y = random.randint(0, HEIGHT // grid_size - 1)

    place("battery", x, y)
    wait(1000)

    remove("battery", x, y)
    wait(500)
```

**New Concepts**:
- `import random`: Allows you to generate random numbers.
- `WIDTH` and `HEIGHT`: Represent the screen size.

---

### Tool Menu: No <EMPTY> Space

Press **T** to open the tool menu. Here’s what each tool does:

- **Obstacle**: Blocks R1’s path.
- **Spike**: Sends R1 back to its starting position.
- **Movement Blocks**: Change R1’s direction automatically.
- **Sand**: Slows R1 and costs -5 energy per step.
- **Water**: Slows R1 and costs -10 energy per step.
- **Glass**: Costs -20 energy per step.
- **Box**: Can be picked up and placed.
- **Finish Line**: Ends the level and shows R1’s performance.
- **Battery**: Recharges +20 energy.

**Challenge**: Program R1 to navigate a generated level and reach the finish line!

---

### Game Controls

- **[O]**: Restart R1’s position.
- **[^]**: Restart the game.
- **[X]**: Exit the game.

---

### This Project Needs a Hero!

As a beginner programmer, I’ve made plenty of mistakes creating this game—from not organizing files to leaving bugs in the code. The graphics aren’t perfect, and there’s a lot to improve. But I’m proud of what I’ve built and hope you enjoy it too!

If you fell in love with this project and want to contribute, bring your joy and creativity. We need you to make this game even better!

