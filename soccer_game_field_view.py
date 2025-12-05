"""
View File responsible for displaying the
view of the game and updates of the
variables and instances through the
Pygame window
"""

import sys
import math
import json
import os
import pygame
from soccer_game_field_model import defend_move  # kept for compatibility
from soccer_game_field_model import initialize_def
from soccer_game_field_model import ball_move  # kept for compatibility / tests
from soccer_game_field_model import Level
from soccer_game_field_model import make_def_dict
from soccer_game_field_model import level_images
from soccer_game_field_model import make_level_rect
from soccer_game_field_controller import get_ball_move

HIGHSCORE_FILE = "highscore.json"


def load_high_score():
    """
    Load the saved high score from disk if it exists.
    Returns 0 if the file is missing or invalid.
    """
    if not os.path.exists(HIGHSCORE_FILE):
        return 0

    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("high_score", 0))
    except (json.JSONDecodeError, ValueError, OSError):
        # If file is corrupted or unreadable, reset to 0
        return 0


def save_high_score(score: int):
    """
    Save the given high score to disk as JSON.
    """
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump({"high_score": int(score)}, f)
    except OSError:
        # If something goes wrong writing the file, ignore silently
        # (game should still be playable)
        pass


class UpFieldView:
    """
    Soccer field view displaying the updated
    instances and variables on the Pygame Window
    """

    def __init__(self):
        # Initialize mixer first for more reliable audio timing
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
        except Exception as e:
            print("Mixer pre_init failed:", e)

        pygame.init()
        pygame.display.set_caption("Mini Soccer Game")

        # Main screen
        self.screen = pygame.display.set_mode((1000, 1000))

        # Level graphics
        self.level_dict = level_images()

        # HUD fonts
        self.font = pygame.font.SysFont("arial", 32, bold=True)
        self.big_font = pygame.font.SysFont("arial", 72, bold=True)
        self.small_font = pygame.font.SysFont("arial", 24)

        # Game state
        self.score = 0
        self.lives = 3
        self.high_score = load_high_score()  # load saved high score if exists

        # Ball physics state (center position & velocity)
        self.ball_x = 500.0
        self.ball_y = 950.0
        self.ball_vx = 0.0
        self.ball_vy = 0.0

        # Sound placeholders
        self.goal_sound = None
        self.hit_sound = None

        # Global animation counter for smooth animation
        self.anim_counter = 0

    # -----------------------
    # ASSET LOADING HELPERS
    # -----------------------

    def _load_goal(self):
        """
        Load goal image and rect
        """
        goal = pygame.image.load("images/soccergoal.png")
        goal = pygame.transform.scale(goal, (200, 200))
        goal_rect = goal.get_rect(center=(500, 100))
        return [goal, goal_rect]

    def _load_background(self):
        """
        Load background field and rect
        """
        background = pygame.image.load("images/background.png")
        background = pygame.transform.scale(background, (1000, 1000))
        background_rect = background.get_rect()
        return [background, background_rect]

    def _load_level_up(self):
        """
        Load level up graphic and rect
        """
        level_up = pygame.image.load("images/level_up.png")
        level_up = pygame.transform.scale(level_up, (600, 600))
        level_up_rect = level_up.get_rect(center=(500, 500))
        return [level_up, level_up_rect]

    def _load_ball_pic(self):
        """
        Load soccer ball image
        """
        ball = pygame.image.load("images/soccerball.png")
        ball = pygame.transform.scale(ball, (50, 50))
        return ball

    def _load_sounds(self):
        """
        Load background music and sound effects.
        Uses WAV files (more reliable than MP3 on Linux/WSL).
        """
        try:
            pygame.mixer.init()
            print("Mixer initialized successfully.")
        except Exception as e:
            print("Error initializing mixer:", e)
            return

        # Background crowd ambience (looping)
        try:
            print("Loading music: sounds/crowd-cheering-379666.wav")
            pygame.mixer.music.load("sounds/crowd-cheering-379666.wav")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            print("Background music started.")
        except Exception as e:
            print("Error loading/playing background music:", e)

        # Goal sound
        try:
            print("Loading goal sound: sounds/west-ham-bubbles-77370.wav")
            self.goal_sound = pygame.mixer.Sound("sounds/west-ham-bubbles-77370.wav")
            self.goal_sound.set_volume(0.8)
        except Exception as e:
            print("Error loading goal sound:", e)
            self.goal_sound = None

        # Hit / tackle sound
        try:
            print("Loading hit sound: sounds/kick-362036.wav")
            self.hit_sound = pygame.mixer.Sound("sounds/kick-362036.wav")
            self.hit_sound.set_volume(0.7)
        except Exception as e:
            print("Error loading hit sound:", e)
            self.hit_sound = None

    # -----------------------
    # UI HELPERS
    # -----------------------

    def _draw_hud(self, level):
        """
        Draws the HUD at the top: Level, Score, High Score, Lives
        """
        # Semi-transparent black bar
        hud_bg = pygame.Surface((1000, 60))
        hud_bg.set_alpha(160)
        hud_bg.fill((0, 0, 0))
        self.screen.blit(hud_bg, (0, 0))

        level_text = self.font.render(f"Level: {level}", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_text = self.font.render(f"High: {self.high_score}", True, (255, 255, 255))
        lives_hearts = "♥" * self.lives if self.lives > 0 else "0"
        lives_text = self.font.render(f"Lives: {lives_hearts}", True, (255, 0, 0))

        self.screen.blit(level_text, (20, 15))
        self.screen.blit(score_text, (260, 15))
        self.screen.blit(high_text, (520, 15))
        self.screen.blit(lives_text, (800, 15))

    def _reset_ball_position(self):
        """
        Reset ball to starting position and stop movement
        """
        self.ball_x = 500.0
        self.ball_y = 900.0
        self.ball_vx = 0.0
        self.ball_vy = 0.0

    def _start_menu(self):
        """
        Simple start menu where the player chooses starting level
        using LEFT / RIGHT and presses ENTER to start.
        Returns the chosen starting level (1–5).
        """
        level = 1
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        level = min(5, level + 1)
                    elif event.key == pygame.K_LEFT:
                        level = max(1, level - 1)
                    elif event.key == pygame.K_RETURN:
                        # Reset core game state before starting
                        self.score = 0
                        self.lives = 3
                        self._reset_ball_position()
                        return level

            # Draw menu screen
            self.screen.fill((0, 100, 0))

            title = self.big_font.render("Mini Soccer Game", True, (255, 255, 255))
            subtitle = self.small_font.render(
                "Use LEFT / RIGHT to choose starting level, ENTER to start",
                True,
                (255, 255, 255),
            )
            level_text = self.font.render(
                f"Starting Level: {level}", True, (255, 215, 0)
            )
            hint = self.small_font.render(
                "Use arrow keys in game to move the ball and score!",
                True,
                (255, 255, 255),
            )

            title_rect = title.get_rect(center=(500, 300))
            subtitle_rect = subtitle.get_rect(center=(500, 380))
            level_rect = level_text.get_rect(center=(500, 450))
            hint_rect = hint.get_rect(center=(500, 520))

            self.screen.blit(title, title_rect)
            self.screen.blit(subtitle, subtitle_rect)
            self.screen.blit(level_text, level_rect)
            self.screen.blit(hint, hint_rect)

            pygame.display.update()
            clock.tick(30)

    def _ball_defend_collide(self):
        """
        Handle collision between ball and defender:
        lose a life, reset ball, or game over.
        Returns True if this collision caused game over, else False.
        """
        self.lives -= 1
        if self.hit_sound:
            self.hit_sound.play()

        if self.lives <= 0:
            # Update high score if needed
            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)
            return True  # signal game over
        else:
            # Show "life lost" message and reset ball
            msg = self.font.render("You were tackled! Life -1", True, (255, 255, 255))
            msg_rect = msg.get_rect(center=(500, 500))
            self.screen.blit(msg, msg_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            self._reset_ball_position()
            return False

    def _game_over_screen(self):
        """
        Show a Game Over screen and let the player choose:
        R = restart,  Q or ESC = quit.
        Returns True if the player wants to restart, False to quit.
        """
        clock = pygame.time.Clock()
        glow_color = (239, 68, 68)  # red

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        return False

            # Dark overlay
            overlay = pygame.Surface((1000, 1000))
            overlay.set_alpha(215)
            overlay.fill((3, 7, 18))  # very dark navy
            self.screen.blit(overlay, (0, 0))

            # Glowing frame
            frame = pygame.Surface((700, 420), pygame.SRCALPHA)
            pygame.draw.rect(frame, (15, 23, 42, 230), frame.get_rect(), border_radius=24)
            pygame.draw.rect(frame, (248, 113, 113, 180), frame.get_rect(), 2, border_radius=24)
            self.screen.blit(frame, (150, 260))

            title = self.big_font.render("GAME OVER", True, glow_color)
            score_text = self.font.render(
                f"Final Score: {self.score}", True, (248, 250, 252)
            )
            high_text = self.font.render(
                f"High Score: {self.high_score}", True, (190, 242, 100)
            )
            prompt = self.small_font.render(
                "Press R to play again, or Q / ESC to quit",
                True,
                (209, 213, 219),
            )

            title_rect = title.get_rect(center=(500, 320))
            score_rect = score_text.get_rect(center=(500, 395))
            high_rect = high_text.get_rect(center=(500, 440))
            prompt_rect = prompt.get_rect(center=(500, 505))

            self.screen.blit(title, title_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(high_text, high_rect)
            self.screen.blit(prompt, prompt_rect)

            pygame.display.update()
            clock.tick(30)

    def _quit_game(self):
        """
        Handle QUIT events during the main game loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # -----------------------
    # MAIN GAME LOOP
    # -----------------------

    def display_game(self):
        """
        Runs the game loop, allowing multiple runs:
        - Start menu
        - Play until game over
        - Game Over screen: restart or quit
        """

        clock = pygame.time.Clock()

        # Load assets once
        goal_list = self._load_goal()
        background_list = self._load_background()
        level_up_list = self._load_level_up()
        ball = self._load_ball_pic()
        self._load_sounds()

        # How the striker reacts to defenders
        danger_radius = 180.0      # pixels
        max_escape_force = 1.2     # how strong the "dribble away" assist is

        while True:  # Outer loop: allows replay without restarting Python
            # --- Start menu to choose level ---
            level = self._start_menu()

            # Initialize level, defenders, and difficulty
            level_stats = Level(level)
            number_def = level_stats.create_numdef()
            base_vel = level_stats.create_newvel()
            max_speed = base_vel / 2.0

            new_defend_dict = make_def_dict(number_def)
            stats_dict = initialize_def(new_defend_dict)

            # Defender velocities: move horizontally AND vertically, always moving
            defender_vel = {}
            for i in stats_dict:
                # vary speed a bit per defender & level
                vx = (1.5 + 0.2 * level) * (1 if i % 2 == 0 else -1)
                vy = (1.0 + 0.15 * level) * (1 if i % 3 == 0 else -1)
                defender_vel[i] = [vx, vy]

            # defender animation frames (simple 2-frame "run" cycle)
            defender_anim = {}
            for i, entry in stats_dict.items():
                base_img = entry[0]
                # Slightly rotated version for "step" frame
                alt_img = pygame.transform.rotate(base_img, 8 if i % 2 == 0 else -8)
                defender_anim[i] = {
                    "frames": [base_img, alt_img],
                }

            # Ensure ball is reset at the start of each run
            self._reset_ball_position()

            # -------- One full run of the game --------
            running = True
            while running:
                self._quit_game()
                self.anim_counter += 1

                # --- Ball physics with smooth motion ---
                user_input = get_ball_move()
                acceleration = 1.0
                if user_input[pygame.K_LEFT]:
                    self.ball_vx -= acceleration
                if user_input[pygame.K_RIGHT]:
                    self.ball_vx += acceleration
                if user_input[pygame.K_UP]:
                    self.ball_vy -= acceleration
                if user_input[pygame.K_DOWN]:
                    self.ball_vy += acceleration

                # Apply friction
                friction = 0.90
                self.ball_vx *= friction
                self.ball_vy *= friction

                # Limit maximum speed
                speed = (self.ball_vx ** 2 + self.ball_vy ** 2) ** 0.5
                if speed > max_speed and speed > 0:
                    scale = max_speed / speed
                    self.ball_vx *= scale
                    self.ball_vy *= scale

                # Update ball position
                self.ball_x += self.ball_vx
                self.ball_y += self.ball_vy

                # Keep ball within field bounds
                self.ball_x = max(100, min(self.ball_x, 900))
                self.ball_y = max(150, min(self.ball_y, 950))

                # --- Drawing section ---
                self.screen.blit(background_list[0], background_list[1])
                self.screen.blit(goal_list[0], goal_list[1])

                # Level graphic (cap at 6 in case level > 6)
                display_level = min(level, 6)
                level_list = make_level_rect(display_level, self.level_dict)
                self.screen.blit(level_list[0], level_list[1])

                # Ball
                ball_coord = ball.get_rect(
                    center=(int(self.ball_x), int(self.ball_y))
                )
                self.screen.blit(ball, ball_coord)

                # Track nearest defender to the ball each frame
                nearest_def_x = None
                nearest_def_y = None
                nearest_dist_sq = None

                # Defenders: CONSTANT PATTERNS (horizontal + vertical) + ANIMATION
                for i in stats_dict:
                    defender_entry = stats_dict[i]
                    defender_x = defender_entry[1]
                    defender_y = defender_entry[2]
                    vx, vy = defender_vel[i]

                    # Move defender
                    defender_x += vx
                    defender_y += vy

                    # Bounce horizontally between 150 and 850
                    if defender_x <= 150 or defender_x >= 850:
                        vx = -vx
                        defender_x += vx  # move back inside after bounce

                    # Bounce vertically between 200 and 800
                    if defender_y <= 200 or defender_y >= 800:
                        vy = -vy
                        defender_y += vy

                    defender_entry[1] = defender_x
                    defender_entry[2] = defender_y
                    defender_vel[i] = [vx, vy]

                    # --- Animation: choose frame + bobbing ---
                    anim = defender_anim[i]
                    # Switch frame every 10 ticks
                    frame_id = 0 if (self.anim_counter // 10) % 2 == 0 else 1
                    current_img = anim["frames"][frame_id]

                    # Bobbing offset (small up/down sine wave)
                    bob_offset = int(
                        3 * math.sin((self.anim_counter + i * 7) / 12.0)
                    )
                    draw_y = defender_y + bob_offset

                    # Track nearest defender (using bobbed draw_y for realism)
                    dx_ball = self.ball_x - defender_x
                    dy_ball = self.ball_y - draw_y
                    dist_sq = dx_ball * dx_ball + dy_ball * dy_ball
                    if nearest_dist_sq is None or dist_sq < nearest_dist_sq:
                        nearest_dist_sq = dist_sq
                        nearest_def_x = defender_x
                        nearest_def_y = draw_y

                    # Draw defender
                    self.screen.blit(current_img, (defender_x, draw_y))
                    defender_coord = current_img.get_rect(
                        center=(defender_x, draw_y)
                    )

                    # Collision check
                    if ball_coord.colliderect(defender_coord):
                        game_over = self._ball_defend_collide()
                        if game_over:
                            running = False
                        # Either way, stop processing defenders this frame
                        break

                # If game ended this frame, skip the rest and go to Game Over screen
                if not running:
                    # Draw HUD once more behind the Game Over overlay
                    self._draw_hud(level)
                    pygame.display.update()
                    continue

                # --- Auto-escape / dribble assist when defender is close ---
                if nearest_def_x is not None:
                    dx = self.ball_x - nearest_def_x
                    dy = self.ball_y - nearest_def_y
                    dist_sq = dx * dx + dy * dy

                    if dist_sq > 0 and dist_sq < danger_radius * danger_radius:
                        dist = dist_sq ** 0.5
                        ux = dx / dist
                        uy = dy / dist

                        # Stronger escape when they are very close
                        closeness = (danger_radius - dist) / danger_radius  # 0..1
                        escape_strength = max_escape_force * closeness

                        # Add escape force to ball velocity
                        self.ball_vx += ux * escape_strength
                        self.ball_vy += uy * escape_strength

                # Goal collision: level up
                if ball_coord.colliderect(goal_list[1]):
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                        save_high_score(self.high_score)
                    if self.goal_sound:
                        self.goal_sound.play()

                    self.screen.blit(level_up_list[0], level_up_list[1])
                    pygame.display.update()
                    pygame.time.wait(800)

                    # Increase difficulty: next level, more defenders + faster
                    level += 1
                    level_stats = Level(level)
                    number_def = level_stats.create_numdef()
                    base_vel = level_stats.create_newvel()
                    max_speed = base_vel / 2.0

                    new_defend_dict = make_def_dict(number_def)
                    stats_dict = initialize_def(new_defend_dict)

                    # Rebuild defender velocities for new defenders
                    defender_vel = {}
                    for i in stats_dict:
                        vx = (1.5 + 0.2 * level) * (1 if i % 2 == 0 else -1)
                        vy = (1.0 + 0.15 * level) * (1 if i % 3 == 0 else -1)
                        defender_vel[i] = [vx, vy]

                    # Rebuild animation frames for new defenders
                    defender_anim = {}
                    for i, entry in stats_dict.items():
                        base_img = entry[0]
                        alt_img = pygame.transform.rotate(
                            base_img, 8 if i % 2 == 0 else -8
                        )
                        defender_anim[i] = {"frames": [base_img, alt_img]}

                    self._reset_ball_position()

                # HUD: now shows Level, Score, High Score, Lives
                self._draw_hud(level)

                pygame.display.update()
                clock.tick(60)

            # -------- After a run ends (GAME OVER) --------
            want_restart = self._game_over_screen()
            if not want_restart:
                pygame.quit()
                sys.exit()
            # else: loop back to outer while True and show start menu again
