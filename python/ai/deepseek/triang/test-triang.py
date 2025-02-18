import numpy as np  

def triangulate(sensor_positions, theta_phi_angles):  
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
    p0 = np.linalg.pinv(A) @ b  
    return p0  
