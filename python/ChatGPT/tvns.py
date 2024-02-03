import numpy as np
import matplotlib.pyplot as plt

# Constants
gamma = 7 / 5
k = (gamma + 1) / (gamma - 1)
A = 1  # You can choose an appropriate value for A
B = 1  # You can choose an appropriate value for B
n = 3;

# Function to calculate density, velocity, and pressure
def density(xi, t):
    return A * xi**(-k) / s(t)**k

def velocity(xi, t):
    return s_dot(t) / s(t) * xi

def pressure(xi, t):
    return B * (1 - 1 / xi**2)**3.5

# Function to calculate shock front radius as a function of time
def s(t):
    # Implement the function for s(t) based on your specific problem
    return t**n  # Replace with the appropriate expression

# Function to calculate the time derivative of shock front radius
def s_dot(t):
    # Implement the function for the time derivative of s(t) based on your specific problem
    return n * t**(n-1)  # Replace with the appropriate expression

# Time values
t_values = np.linspace(0.1, 2, 100)

# Plotting the self-similar solution
for t in t_values:
    xi_values = np.linspace(0.01, 5, 100)
    rho_values = density(xi_values, t)
    u_values = velocity(xi_values, t)
    P_values = pressure(xi_values, t)

    plt.plot(xi_values, rho_values, label=f't={t:.2f}')
    plt.xlabel(r'$\xi$')
    plt.ylabel(r'$\rho$')
    plt.title('Self-similar solution of TVNS blast wave')
    plt.legend()

plt.show()