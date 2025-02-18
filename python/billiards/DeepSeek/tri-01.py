import numpy as np

def triangulate(sensor_positions, theta_phi_angles):
    """Estimate target position from sensors and angles."""
    A = np.zeros((3, 3))
    b = np.zeros(3)
    for i in range(len(sensor_positions)):
        theta, phi = theta_phi_angles[i]
        di = np.array([
            np.cos(theta) * np.cos(phi),
            np.sin(theta) * np.cos(phi),
            np.sin(phi)
        ])
        Mi = np.eye(3) - np.outer(di, di)
        A += Mi
        b += Mi @ sensor_positions[i]
    return np.linalg.pinv(A) @ b

# Example usage (cube test case):
sensor_positions = np.array([
    [1, 1, -1],
    [-1, -1, -1],
    [-1, 1, 1]
])

theta_phi_angles = np.array([
    [3*np.pi/2, np.pi/4],   # Sensor 1
    [0, np.pi/4],           # Sensor 2
    [7*np.pi/4, 0]          # Sensor 3
])

p0 = triangulate(sensor_positions, theta_phi_angles)
print(f"Estimated target: {np.round(p0, 6)}")