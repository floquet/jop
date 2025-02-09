import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Pool table parameters
TABLE_WIDTH = 2.84  # meters
TABLE_HEIGHT = 1.42  # meters
BALL_RADIUS = 0.057  # meters
POCKET_RADIUS = 0.1  # meters (approx for visualization)
TIME_STEP = 0.01  # seconds per update
TOTAL_TIME = 10  # seconds
FRAMES = int(TOTAL_TIME / TIME_STEP)

# Define pockets (at corners)
pockets = np.array(
    [[0, 0], [TABLE_WIDTH, 0], [0, TABLE_HEIGHT], [TABLE_WIDTH, TABLE_HEIGHT]]
)


# Ball class
def random_velocity():
    """Generate a random velocity for a ball"""
    speed = np.random.uniform(0.5, 2.0)  # m/s
    angle = np.random.uniform(0, 2 * np.pi)
    return np.array([speed * np.cos(angle), speed * np.sin(angle)])


class Ball:
    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.velocity = random_velocity()

    def update_position(self):
        self.position += self.velocity * TIME_STEP
        self.check_wall_collision()
        self.check_pocket()

    def check_wall_collision(self):
        if (
            self.position[0] - BALL_RADIUS < 0
            or self.position[0] + BALL_RADIUS > TABLE_WIDTH
        ):
            self.velocity[0] *= -1  # Reverse x velocity
        if (
            self.position[1] - BALL_RADIUS < 0
            or self.position[1] + BALL_RADIUS > TABLE_HEIGHT
        ):
            self.velocity[1] *= -1  # Reverse y velocity

    def check_pocket(self):
        for pocket in pockets:
            if np.linalg.norm(self.position - pocket) < POCKET_RADIUS:
                self.velocity = np.array([0, 0])  # Stop ball
                self.position = pocket  # Set position to pocket center


# Initialize two balls
ball1 = Ball(TABLE_WIDTH / 3, TABLE_HEIGHT / 2)
ball2 = Ball(2 * TABLE_WIDTH / 3, TABLE_HEIGHT / 2)

# Animation setup
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, TABLE_WIDTH)
ax.set_ylim(0, TABLE_HEIGHT)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.set_facecolor("green")

# Draw table boundaries
ax.plot(
    [0, TABLE_WIDTH, TABLE_WIDTH, 0, 0], [0, 0, TABLE_HEIGHT, TABLE_HEIGHT, 0], "black"
)

# Draw pockets
for pocket in pockets:
    ax.add_patch(plt.Circle(pocket, POCKET_RADIUS, color="black"))

# Draw balls
ball1_patch = plt.Circle(ball1.position, BALL_RADIUS, color="white")
ball2_patch = plt.Circle(ball2.position, BALL_RADIUS, color="red")
ax.add_patch(ball1_patch)
ax.add_patch(ball2_patch)


# Animation function
def update(frame):
    ball1.update_position()
    ball2.update_position()
    ball1_patch.center = ball1.position
    ball2_patch.center = ball2.position
    return ball1_patch, ball2_patch


ani = animation.FuncAnimation(
    fig, update, frames=FRAMES, interval=TIME_STEP * 1000, blit=True
)
plt.show()
