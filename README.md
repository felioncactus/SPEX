# SPEX - Spirit of Exploration
<div align="center">
  <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/main_title.gif?raw=true" alt="Image description">
</div><br>
Welcome to the wonderful world of programming! SPEX is a game designed to introduce beginners (just like me) to the basics of coding in a fun and interactive way. Whether you want to program a robot or design an environment, this game has something for you.

#### Core Philosophy
This project is built on two core principles:

1. **Learning by Doing**: The best way to learn is through hands-on experience. Dive in, make mistakes, and learn as you go!
   
2. **Adaptability**: Programming teaches us to handle both fixed ("hard-coded") solutions and flexible, adaptable systems. For example, imagine programming a robot to navigate a maze. You could give it an exact step-by-step algorithm, but what happens if the maze changes? Alternatively, you could create a program that allows the robot to adapt and find the finish line on its own. That’s the spirit of exploration we’re aiming for!

---

## How to Program a Robot 101

This tutorial will guide you through programming your new robotic friend, R1!
<br>Don’t worry; it’s beginner-friendly and uses Python, a language known for its simplicity and power.

### Meet R1 <br>
<table>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/Robot.png" alt="Your Robot">
    </td>
    <td>
      R1 is waiting for you to take control. Press <b>P</b> on your keyboard to open the programming window. Here, you can write commands for R1 and click the <b>RUN</b> button to execute them.
    </td>
  </tr>
</table>

### Robot Programming Interface

![Robot Programming Interface](https://github.com/felioncactus/SPEX/blob/main/screenshots/wd_prALL.png?raw=true)

### Basic Commands
Here are the commands R1 understands:

<table>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/move.gif?raw=true" alt="Your Robot" width = 450px>
    </td>
    <td>
      <b>MoveLeft(steps):</b> Moves left by the specified number of steps. <br>
      <b>MoveRight(steps):</b> Moves right by the specified number of steps. <br>
      <b>MoveUp(steps):</b> Moves up by the specified number of steps. <br>
      <b>MoveDown(steps):<b> Moves down by the specified number of steps.<br>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/box.gif?raw=true" alt="Your Robot" width = 450px>
    </td>
    <td>
      <b>pickUP():</b> Picks up a box. <br>
      <b>placeIT():</b> Places a box. <br>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/robot_detect.gif?raw=true" alt="Your Robot" width = 450px>
    </td>
    <td>
      <b>robot_detect(item):</b> Detects specific items or obstacles. <br>
      <b>wait(ms):</b> Pauses for the specified time (in milliseconds) <br>
      <b>items available to detect:</b>
      <table>
          <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/obstacle.png?raw=true" alt="obstacle" width="20"></td>
             <td><b>obstacle</b></td>
           </tr>
          <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/spike.png?raw=true" alt="spike" width="20"></td>
             <td><b>spike</b>.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/sand.png?raw=true" alt="Icon 2" width="20"></td>
             <td><b>Sand</b></td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/water.png?raw=true" alt="Icon 3" width="20"></td>
             <td><b>Water</b></td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/glass.png?raw=true" alt="Icon 4" width="20"></td>
             <td><b>Glass</b></td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/box.png?raw=true" alt="Icon 5" width="20"></td>
             <td><b>Box</b></td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/finish.png?raw=true" alt="Icon 6" width="20"></td>
             <td><b>Finish Line</b></td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/battery.png?raw=true" alt="Icon 7" width="20"></td>
             <td><b>Battery</b></td>
           </tr>
         </table>
    </td>
  </tr>
</table>

**Note**: Each movement consumes energy (**-1pt**), so plan your actions wisely. You’ll learn how to recharge energy later.

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

## How to Program an Environment 101



Programming the environment is just as fun! Press **E** on your keyboard to open the environment editor. Here are the new commands:

- **place(item, x, y)**: Places an item at specified coordinates.
- **remove(item, x, y)**: Removes an item from specified coordinates.
- **wait(ms)**: Pauses for the specified time.

### Environment Programming Interface

![Environment Programming Interface](https://github.com/felioncactus/SPEX/blob/main/screenshots/environ.gif?raw=true)

### Example: Randomized Battery Placement
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

## Tool Menu: No <EMPTY> Space

Press **T** to open the tool menu. Here’s what each tool does:

<table>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/obstacle.png?raw=true" alt="Obstacle">
    </td>
    <td>
      <b>Obstacle:</b> Blocks R1’s path. <br>
    </td>
     <td>
        <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/obstacle.gif?raw=true" alt="Obstacle" width = 300px>
     </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/spike.png?raw=true" alt="Spike">
    </td>
    <td>
      <b>Spike:</b> Sends R1 back to its starting position. <br>
    </td>
     <td>
        <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/spikes.gif?raw=true" alt="Obstacle" width = 300px>
     </td>
  </tr>
     <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/spike.png?raw=true" alt="Blocks">
    </td>
    <td>
         <table>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/moveRight.png?raw=true" alt="Icon 1" width="20"></td>
             <td><b>Movement Blocks:</b> Change R1’s direction automatically.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/sand.png?raw=true" alt="Icon 2" width="20"></td>
             <td><b>Sand:</b> Slows R1 and costs -5 energy per step.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/water.png?raw=true" alt="Icon 3" width="20"></td>
             <td><b>Water:</b> Slows R1 and costs -10 energy per step.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/glass.png?raw=true" alt="Icon 4" width="20"></td>
             <td><b>Glass:</b> Costs -20 energy per step.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/box.png?raw=true" alt="Icon 5" width="20"></td>
             <td><b>Box:</b> Can be picked up and placed.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/finish.png?raw=true" alt="Icon 6" width="20"></td>
             <td><b>Finish Line:</b> Ends the level and shows R1’s performance.</td>
           </tr>
           <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/battery.png?raw=true" alt="Icon 7" width="20"></td>
             <td><b>Battery:</b> Recharges +20 energy.</td>
           </tr>
            <tr>
             <td><img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/generate.png?raw=true" alt="Icon 8" width="20"></td>
             <td><b>Generate Level:</b> Generate Level.</td>
           </tr>
         </table>
    </td>
     <td>
        <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/blocks.gif?raw=true" alt="Obstacle" width = 300px>
     </td>
  </tr>
</table>

**Challenge**: Program R1 to navigate a generated level and reach the finish line!

### Example of Generate Level

![Generate Level](https://github.com/felioncactus/SPEX/blob/main/screenshots/generatelevel.gif?raw=true)

---

### Game Controls

<table>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/reloadPosBTN.png?raw=true" alt="Your Robot" width = 50px>
    </td>
    <td>
      Restart R1’s position. <br>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/reloadGameBTN.png?raw=true" alt="Your Robot" width = 50px>
    </td>
    <td>
      Restart the game. <br>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/felioncactus/SPEX/blob/main/screenshots/exitBTN.png?raw=true" alt="Your Robot" width = 50px>
    </td>
    <td>
      Exit the game. <br>
    </td>
  </tr>
</table>

---

### This Project Needs a Hero!

As a beginner programmer, I’ve made plenty of mistakes creating this game—from not organizing files to leaving bugs in the code. The graphics aren’t perfect, and there’s a lot to improve. But I’m proud of what I’ve built and hope you enjoy it too!

If you fell in love with this project and want to contribute, bring your joy and creativity. We need you to make this game even better!

---

### How to play it?
1. **Install Python**  
   Download and install Python
   
3. **Download VS Code**  
   Download and install Visual Studio Code

4. **Download My Files**  
   Obtain the project files and save them to your desired location.

5. **Open VS Code Under This Folder**  
   Launch VS Code and open the folder containing the downloaded files.

6. **Open the Main File and Press Run**  
   Open the main Python file in VS Code and press the "Run" button to execute it.

---
### Technologies Used

The following technologies were used to create this project:

- **Python**: The core programming language powering the game.
- **Pygame**: Used for creating the graphical user interface and handling game logic.
- **Tkinter**: Integrated for managing additional UI components, such as input dialogs and tool windows.

