## **Project Overview**
### The Snake Game is a classic arcade-style game built with Python (Pygame).
### This project demonstrates game development logic, event handling, collision detection, and UI design using Python.
## **Features**
- Smooth snake movement with keyboard controls (↑ ↓ ← →)
- Random food generation
- Game over when snake hits wall or itself 
- Score tracking system 
- Sound effects and background blue square
- Simple interface
- unextendable with Flask backend for leaderboard
## **Project Structure**
![alt text](<Screenshot 2025-11-03 155702.png>)
## **Installation & Setup**
1. Prerequisites
- Python 3.10+
- Pygame installed
2. Installation

- ```https://github.com/phornya/snake-game```

- ```pip install -r requirements.txt```
3. Run the Game
- ```python main.py```
## **How to play**
1. Key & Action
- ↑ / W      Move Up
- ↓ / S      Move Down
- ← / A      Move Left
- → / D      Move Right
### **Gameplay Rule**
- Eat food to increase score
- Don't hit yourself, but can hit the wall or it's Game Over!
- Try to beat your high score!
## **Developer**
```snake.py``` Contains the snake class handles position, direction and growth logic

``` food.py``` Food random position

```main.py``` Controls the main loop, rendering, input events, and collisoin.

```setting.py``` Defines constants such as cell_size and cell_number