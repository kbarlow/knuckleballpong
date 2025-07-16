
# Knuckleball Pong and Pong ML

## About

**Knuckleball Pong** is a classic Pong game with custom physics tweaks for more dynamic and unpredictable gameplay.

**Pong ML** is a classic Pong game where the right paddle is controlled by a Q-learning AI agent. The AI learns in real time, improving its play as it observes the ball, its own paddle, and the opponent's paddle. Q-learning is a reinforcement learning technique where the agent updates its strategy based on rewards for good actions and penalties for mistakes, gradually learning to play better over time.

This project was a collaboration with GitHub Copilot, your friendly AI coding assistant!


## Prerequisites

- Python 3.7 or higher must be installed. Check your version with:
  ```bash
  python3 --version
  ```
- [pip](https://pip.pypa.io/en/stable/) should be available (comes with Python 3).

## Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/kbarlow/knuckleballpong.git
   cd knuckleballpong
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


5. **Run the game:**
   - For classic Pong with custom physics:
     ```bash
     python3 pong.py
     ```
   - For Pong with Q-learning AI:
     ```bash
     python3 pongML.py
     ```

Enjoy playing Knuckleball Pong!
# knuckleballpong
Copilot experiment to write pong in python with some customization
