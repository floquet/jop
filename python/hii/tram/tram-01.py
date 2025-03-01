import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import pwd
import platform
import sys
from scipy.stats import gaussian_kde
from sklearn.neighbors import KNeighborsClassifier

# === Provenance Function ===
def pr_provenance():
    """
    Print the provenance information of the script including execution
    details, user information, platform details, and package versions.
    """
    print("\nExecution Provenance")
    print("=" * 40)
    print("Execution Time:", datetime.datetime.now())
    print("Source Path:   {}/{}".format(os.getcwd(), os.path.basename(__file__)))
    print("User ID:       {}".format(pwd.getpwuid(os.getuid()).pw_name))
    print("\nPlatform Information:")
    print("    Platform:  {}".format(platform.platform()))
    print("    System:    {}".format(platform.uname().system))
    print("    Node:      {}".format(platform.uname().node))
    print("    Release:   {}".format(platform.uname().release))
    print("    Version:   {}".format(platform.uname().version))
    print("    Machine:   {}".format(platform.uname().machine))
    print("    Processor: {}".format(platform.uname().processor))
    print("\nVersion Information:")
    print("    Python:    {}".format(sys.version.splitlines()[0]))
    print("    NumPy:     {}".format(np.__version__))
    print("    SciPy:     {}".format(gaussian_kde.__module__))
    print("    Scikit-learn: {}".format(KNeighborsClassifier.__module__))
    print("=" * 40)

# === Monte Carlo Data Generation ===
def generate_data(num_samples=500, threshold=0.9):
    """ Generate Monte Carlo samples and classify success/failure. """
    # seed = 1 
    np.random.seed(1)
    x_samples = np.random.uniform(0, np.pi, num_samples)
    y_samples = np.random.uniform(0, np.pi, num_samples)
    z_samples = np.cos(3 * x_samples) * np.sin(y_samples)
    success = z_samples >= threshold
    return x_samples, y_samples, success

# === Kernel Density Estimation (KDE) ===
def compute_kde(x_samples, y_samples, success):
    """ Compute KDE for success and failure distributions. """
    kde_success = gaussian_kde(np.vstack([x_samples[success], y_samples[success]]))
    kde_failure = gaussian_kde(np.vstack([x_samples[~success], y_samples[~success]]))
    
    x_grid = np.linspace(0, np.pi, 100)
    y_grid = np.linspace(0, np.pi, 100)
    X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
    positions = np.vstack([X_grid.ravel(), Y_grid.ravel()])
    
    Z_success = np.reshape(kde_success(positions), X_grid.shape)
    Z_failure = np.reshape(kde_failure(positions), X_grid.shape)
    
    return X_grid, Y_grid, Z_success, Z_failure

# === k-Nearest Neighbors Classification ===
def knn_classification(x_samples, y_samples, success):
    """ Train k-NN classifier and predict failure regions. """
    X_train = np.vstack([x_samples, y_samples]).T
    y_train = success.astype(int)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    
    x_grid = np.linspace(0, np.pi, 100)
    y_grid = np.linspace(0, np.pi, 100)
    X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
    Z_knn = knn.predict(np.vstack([X_grid.ravel(), Y_grid.ravel()]).T).reshape(X_grid.shape)
    
    return X_grid, Y_grid, Z_knn

# === Visualization ===
def plot_results(X_grid, Y_grid, Z_success, Z_failure, Z_knn, x_samples, y_samples, success):
    """ Plot KDE for success, failure, and k-NN classification. """
    plt.figure(figsize=(12, 5))

    # KDE for Success
    plt.subplot(1, 3, 1)
    plt.contourf(X_grid, Y_grid, Z_success, cmap="Greens", levels=15)
    plt.scatter(x_samples[success], y_samples[success], color='green', edgecolors='k', label="Success", alpha=0.7)
    plt.scatter(x_samples[~success], y_samples[~success], color='red', edgecolors='k', alpha=0.3, label="Failure")
    plt.title("KDE: Success Density")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    # KDE for Failure
    plt.subplot(1, 3, 2)
    plt.contourf(X_grid, Y_grid, Z_failure, cmap="Reds", levels=15)
    plt.scatter(x_samples[success], y_samples[success], color='green', edgecolors='k', alpha=0.3, label="Success")
    plt.scatter(x_samples[~success], y_samples[~success], color='red', edgecolors='k', label="Failure")
    plt.title("KDE: Failure Density")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    # k-NN Failure Region
    plt.subplot(1, 3, 3)
    plt.contourf(X_grid, Y_grid, Z_knn, cmap="coolwarm", alpha=0.5, levels=[-0.5, 0.5, 1.5])
    plt.scatter(x_samples[success], y_samples[success], color='green', edgecolors='k', label="Success", alpha=0.7)
    plt.scatter(x_samples[~success], y_samples[~success], color='red', edgecolors='k', label="Failure")
    plt.title("k-NN Failure Region")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()

    plt.tight_layout()
    plt.show()

# === Main Execution ===
def main():
    """ Main function to execute TRAM-like analysis. """
    pr_provenance()  # Print execution provenance

    # Step 1: Generate Monte Carlo data
    x_samples, y_samples, success = generate_data()

    # Step 2: Compute KDE
    X_grid, Y_grid, Z_success, Z_failure = compute_kde(x_samples, y_samples, success)

    # Step 3: Perform k-NN classification
    X_grid, Y_grid, Z_knn = knn_classification(x_samples, y_samples, success)

    # Step 4: Plot results
    plot_results(X_grid, Y_grid, Z_success, Z_failure, Z_knn, x_samples, y_samples, success)

# === Run the Script ===
if __name__ == "__main__":
    main()
