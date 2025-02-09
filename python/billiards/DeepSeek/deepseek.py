import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle
import datetime
import os
import pwd
import platform
import sys


# ========================
# Execution Provenance
# ========================
def pr_provenance():
    print("\nExecution Provenance:")
    print("---------------------")
    print(datetime.datetime.now())
    print(f"source:  {os.getcwd()}/{os.path.basename(__file__)}")

    try:
        import getpass

        print(f"user:    {getpass.getuser()}")
    except Exception as e:
        print(f"user:    [could not determine: {str(e)}]")

    print("platform info:")
    print(f"    system:   {platform.system()}")
    print(f"    release:  {platform.release()}")
    print(f"    version:  {platform.version()}")

    print("version info:")
    print(f"    python:   {sys.version.split()[0]}")
    print(f"    numpy:    {np.__version__}")

    try:
        import matplotlib

        print(f"    matplotlib: {matplotlib.__version__}")
    except ImportError:
        print("    matplotlib: [not installed]")

    return


pr_provenance()

# ========================
# Physics Constants
# ========================
TABLE_WIDTH = 2.84
TABLE_HEIGHT = 1.42
BALL_RADIUS = 0.0285
POCKET_RADIUS = 0.038
FRICTION = 0.995  # Reduced friction for more collisions
SIMULATION_SPEED = 0.05  # More frequent updates


# ========================
# Ball Class
# ========================
class Ball:
    def __init__(self, x, y, vx=0, vy=0, color=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = BALL_RADIUS
        self.mass = 1.0
        self.pocketed = False
        self.color = color if color else np.random.rand(3)
        self.collided = False

    def update_position(self):
        if not self.pocketed:
            self.x += self.vx * SIMULATION_SPEED
            self.y += self.vy * SIMULATION_SPEED
            self.vx *= FRICTION
            self.vy *= FRICTION


# ========================
# Initialize System
# ========================
pockets = [
    (POCKET_RADIUS, POCKET_RADIUS),
    (TABLE_WIDTH - POCKET_RADIUS, POCKET_RADIUS),
    (TABLE_WIDTH - POCKET_RADIUS, TABLE_HEIGHT - POCKET_RADIUS),
    (POCKET_RADIUS, TABLE_HEIGHT - POCKET_RADIUS),
    (TABLE_WIDTH / 2, POCKET_RADIUS),
    (TABLE_WIDTH / 2, TABLE_HEIGHT - POCKET_RADIUS),
]

# Controlled initial conditions
balls = [
    Ball(TABLE_WIDTH / 2, TABLE_HEIGHT / 2, 0, 0, color=[0, 0.5, 1]),  # Blue cue ball
    Ball(
        TABLE_WIDTH / 2 - 0.5, TABLE_HEIGHT / 2, 2.0, 0, color=[1, 0.5, 0]
    ),  # Orange target ball
]

# ========================
# Visualization Setup
# ========================
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, TABLE_WIDTH)
ax.set_ylim(0, TABLE_HEIGHT)
ax.set_aspect("equal")
table = Rectangle(
    (0, 0), TABLE_WIDTH, TABLE_HEIGHT, facecolor="#2d5a27", edgecolor="black"
)
ax.add_patch(table)
for pocket in pockets:
    ax.add_patch(Circle(pocket, POCKET_RADIUS, color="black"))

# Add collision counter text
collision_text = ax.text(
    0.1, 0.95, "", transform=ax.transAxes, color="white", fontsize=12
)
collision_count = 0

ball_artists = [
    ax.add_patch(Circle((b.x, b.y), BALL_RADIUS, color=b.color)) for b in balls
]


# ========================
# Physics Functions
# ========================
def detect_collisions():
    global collision_count
    collision_occurred = False
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if balls[i].pocketed or balls[j].pocketed:
                continue

            dx = balls[j].x - balls[i].x
            dy = balls[j].y - balls[i].y
            distance = np.hypot(dx, dy)

            if distance < 2 * BALL_RADIUS:
                # Mark collision and handle physics
                collision_occurred = True
                balls[i].collided = True
                balls[j].collided = True

                # Elastic collision calculation
                nx = dx / distance
                ny = dy / distance
                p = 2 * (
                    balls[i].vx * nx
                    + balls[i].vy * ny
                    - balls[j].vx * nx
                    - balls[j].vy * ny
                )
                p /= 1 / balls[i].mass + 1 / balls[j].mass

                balls[i].vx -= p * nx / balls[i].mass
                balls[i].vy -= p * ny / balls[i].mass
                balls[j].vx += p * nx / balls[j].mass
                balls[j].vy += p * ny / balls[j].mass

    if collision_occurred:
        collision_count += 1
        collision_text.set_text(f"Collisions: {collision_count}")


def detect_pockets():
    for ball in balls:
        if ball.pocketed:
            continue
        for px, py in pockets:
            if np.hypot(ball.x - px, ball.y - py) < POCKET_RADIUS:
                ball.pocketed = True
                ball.vx = ball.vy = 0


# ========================
# Animation Update
# ========================
def update(frame):
    # Update positions and handle boundaries
    for ball in balls:
        if not ball.pocketed:
            # Wall collisions with edge check
            if ball.x < BALL_RADIUS or ball.x > TABLE_WIDTH - BALL_RADIUS:
                ball.vx *= -1
                ball.x = np.clip(ball.x, BALL_RADIUS, TABLE_WIDTH - BALL_RADIUS)
            if ball.y < BALL_RADIUS or ball.y > TABLE_HEIGHT - BALL_RADIUS:
                ball.vy *= -1
                ball.y = np.clip(ball.y, BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS)

            ball.update_position()

    detect_collisions()
    detect_pockets()

    # Update visualization
    for artist, ball in zip(ball_artists, balls):
        if ball.pocketed:
            artist.set_visible(False)
        else:
            artist.set_center((ball.x, ball.y))
            if ball.collided:
                artist.set_color("red")
            else:
                artist.set_color(ball.color)
            ball.collided = False  # Reset collision state

    return ball_artists + [collision_text]


# ========================
# Run Animation
# ========================
ani = FuncAnimation(fig, update, frames=200, interval=30, blit=True)
plt.show()
