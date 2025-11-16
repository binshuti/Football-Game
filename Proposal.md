1. The Big Idea

My project is a Mini Soccer Game built in Python using the Model–View–Controller (MVC) architecture and Pygame. It simulates a foosball-style soccer challenge where the player guides a ball through defenders to score goals, with difficulty increasing at each level.

* What I will explore
- Game development and real-time interaction using Python + Pygame
- Keyboard input handling and event loops
- Collision detection
- Clean architecture through MVC
- Level progression and state management
- Writing tests for game logic using pytest

* What I will accomplish
I will deliver a functional, polished single-player game where the player:
- Uses arrow keys to move
- Scores by reaching the goal
- Levels up with increased difficulty
- Loses by colliding with defenders

* MVP
My Minimum Viable Product will include:
- Complete game loop with MVC structure
- Player + defender movement
- Collision detection
- Level progression
- Game-over state
- Simple terminal-based level selection

* Stretch Goals
Time permitting, I may add:
- Scoreboard
- Sound effects
- More polished graphics/animations
- Multiple defender patterns
- Persistent high score saved locally
- Replay/restart option

2. Learning Objectives
Main Learning Objectives (Personal)
- Strengthen my understanding of Python game development
- Learn how to design software using the MVC architecture
- Improve my ability to write clean, testable code
- Become more comfortable with Pygame’s event loop, rendering, and collisions
- Practice version control through Git and GitHub
- Improve project documentation, including README and website

3. Implementation Plan
My game will be structured into four main files:
* Model (soccer_game_field_model.py)
 Game state, ball position, defender positions, speeds, and all collision logic.

* View (soccer_game_field_view.py)
 Renders the game window, ball, defenders, goal, text, and updates visuals.

* Controller (soccer_game_field_controller.py)
 Handles keyboard inputs, game updates, and transitions between states.

* Main (main.py)
 Initializes everything, prompts user for starting level, and runs the main loop.

Tools I will use
- Pygame — rendering, input, collisions
- Pytest — unit testing for model logic
- GitHub Pages — for hosting my project site
- Git + GitHub — version control

Uncertainties

I may need additional time to explore:

- Cleaner ways to organize defender patterns
- Best practices for testing graphical logic
- Using the Pygame mixer for sound features

4. Project Schedule
Week 1 (Nov 14–20):
- Finalize architecture
- Improve model logic
- Begin implementing clean movement + collision logic
- Add comments and docstrings

Week 2 (Nov 21–27):
- Improve view (graphics, layout)
- Add level progression + defender logic
- Start unit tests for the model

Week 3 (Nov 28–Dec 4):
- Add optional stretch features (scoreboard, sounds, animations)
- Polish UI
- Update project website

Week 4 (Dec 5–Dec 11):
- Debug and refine game
- Final testing
- Finalize documentation
- Prepare final submission

5. Collaboration Plan
Since I am working alone, my collaboration plan focuses on self-management and consistent workflow.

* My work strategy
- Break features into smaller tasks using GitHub Issues
- Use branches and pull requests to organize development, even solo
- Follow a lightweight personal agile workflow:
- Plan → build → test → refine → document
- Commit frequently with clear messages
- Maintain clean separation of Model, View, and Controller

* Why this approach?
It keeps the project organized, prevents messy code, and ensures I can track progress and debug effectively.

6. Risks and Limitations
The biggest risks to the project include:
- Complexity of Pygame: animations and collision handling can become tricky

- Time constraints: stretch goals may exceed the available timeline

- MVC discipline: ensuring strict separation between components may take extra effort

- Testing challenges: event-driven code can be harder to test with pytest

To mitigate these:
- I will focus on the MVP first
- Keep code modular
- Write tests for the model early
- Avoid over-engineering graphics/sound

7. Additional Course Content Needed
Topics that would help support my work:
- More examples of Python projects using MVC
- Unit testing for interactive or real-time applications
- Best practices for large project structure in Python
- Debugging tools and techniques for Pygame apps



