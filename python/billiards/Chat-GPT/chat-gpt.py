import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import os
import pwd
import platform
import sys

# Execution Provenance
def pr_provenance():
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("user id:", pwd.getpwuid(os.getuid()).pw_name)
    print("platform info:")
    print("    platform: ", platform.platform())
    print("    uname:    ", platform.uname())
    print("version info:")
    print("    python:   %s" % sys.version)
    print("    numpy:   ", np.__version__)
    print("    platform:", platform.__version__)
    return

# Call provenance function
pr_provenance()

# Pool table parameters
TABLE_WIDTH = 2.84  # meters
TABLE_HEIGHT = 1.42  # meters
BALL_RADIUS = 0.057  # meters
POCKET_RADIUS = 0.1   # meters (approx for visualization)
TIME_STEP = 0.01  # seconds per update
TOTAL_TIME = 10  # seconds
FRAMES = int(TOTAL_TIME / TIME_STEP)

# Define pockets (at corners)
pockets = np.array([
    [0, 0], [TABLE_WIDTH, 0],
    [0, TABLE_HEIGHT], [TABLE_WIDTH, TABLE_HEIGHT]
])

# Ball class
def random_velocity():
    """Generate a random velocity for a ball"""
    speed = np.random.uniform(1.5, 2.5)  # m/s
    angle = np.random.uniform(0, 2 * np.pi)
    return np.array([speed * np.cos(angle), speed * np.sin(angle)])

class Ball:
    def __init__(self, x, y, moving=True):
        self.position = np.array([x, y])
        self.velocity = random_velocity() if moving else np.array([0, 0])
        self.default_color = 'white' if moving else 'blue'
        self.color = self.default_color  # Change color on collision

    def update_position(self):
        self.position += self.velocity * TIME_STEP
        self.check_wall_collision()
        self.check_pocket()
        self.reset_color()

    def check_wall_collision(self):
        if self.position[0] - BALL_RADIUS < 0 or self.position[0] + BALL_RADIUS > TABLE_WIDTH:
            self.velocity[0] *= -1  # Reverse x velocity
        if self.position[1] - BALL_RADIUS < 0 or self.position[1] + BALL_RADIUS > TABLE_HEIGHT:
            self.velocity[1] *= -1  # Reverse y velocity

    def check_pocket(self):
        for pocket in pockets:
            if np.linalg.norm(self.position - pocket) < POCKET_RADIUS:
                self.velocity = np.array([0, 0])  # Stop ball
                self.position = pocket  # Set position to pocket center

    def check_collision(self, other):
        distance = np.linalg.norm(self.position - other.position)
        if distance < 2 * BALL_RADIUS:
            self.color = 'red'  # Change color on collision
            other.color = 'red'
            
            # Elastic collision response
            normal = (other.position - self.position) / distance
            relative_velocity = self.velocity - other.velocity
            speed_along_normal = np.dot(relative_velocity, normal)
            
            if speed_along_normal > 0:
                return  # Balls are moving apart
            
            self.velocity -= speed_along_normal * normal
            other.velocity += speed_along_normal * normal
    
    def reset_color(self):
        self.color = self.default_color

# Initialize balls
ball1 = Ball(TABLE_WIDTH / 2, TABLE_HEIGHT / 2, moving=False)  # Stationary ball in center
ball2 = Ball(TABLE_WIDTH / 3, TABLE_HEIGHT / 2)  # Moving ball to impact first

# Animation setup
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, TABLE_WIDTH)
ax.set_ylim(0, TABLE_HEIGHT)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')
ax.set_facecolor("green")

# Draw table boundaries
ax.plot([0, TABLE_WIDTH, TABLE_WIDTH, 0, 0], [0, 0, TABLE_HEIGHT, TABLE_HEIGHT, 0], 'black')

# Draw pockets
for pocket in pockets:
    ax.add_patch(plt.Circle(pocket, POCKET_RADIUS, color='black'))

# Draw balls
ball1_patch = plt.Circle(ball1.position, BALL_RADIUS, color=ball1.color)
ball2_patch = plt.Circle(ball2.position, BALL_RADIUS, color=ball2.color)
ax.add_patch(ball1_patch)
ax.add_patch(ball2_patch)

# Animation function
def update(frame):
    ball2.update_position()
    ball2.check_collision(ball1)
    ball1_patch.set_color(ball1.color)
    ball2_patch.set_color(ball2.color)
    ball1_patch.center = ball1.position
    ball2_patch.center = ball2.position
    return ball1_patch, ball2_patch

ani = animation.FuncAnimation(fig, update, frames=FRAMES, interval=TIME_STEP * 1000, blit=True)
plt.show()

