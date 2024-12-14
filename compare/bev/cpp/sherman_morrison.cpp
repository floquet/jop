#include <iostream>
#include <iomanip>
#include <array>
#include <cmath>

// Define constants
constexpr int n = 3;

// Function prototypes
void mat_vec_mul(const double mat[n][n], const double vec[n], double result[n]);
double dot_product(const double vec1[n], const double vec2[n]);
void outer_product(const double vec1[n], const double vec2[n], double result[n][n]);
void mat_mul(const double mat1[n][n], const double mat2[n][n], double result[n][n]);
void scalar_mat_mul(double scalar, const double mat[n][n], double result[n][n]);
void mat_subtract(const double mat1[n][n], const double mat2[n][n], double result[n][n]);
void print_matrix(const double mat[n][n]);

int main() {
    // Original matrix A (for reference)
    double A[n][n] = {
        {2.0, 1.0, 0.0},
        {1.0, 3.0, 1.0},
        {0.0, 1.0, 2.0}
    };

    // Precomputed inverse of A
    double A_inv[n][n] = {
        { 0.75, -0.25,  0.125},
        {-0.25,  0.50, -0.25},
        { 0.125, -0.25,  0.625}
    };

    // Vectors u and v
    double u[n] = {1.0, 0.5, 0.25};
    double v[n] = {0.5, 1.0, 0.75};

    // Compute denominator: 1 + v^T * A_inv * u
    double temp_vec[n];
    mat_vec_mul(A_inv, u, temp_vec); // temp_vec = A_inv * u
    double denominator = 1.0 + dot_product(v, temp_vec);
    if (std::abs(denominator) < 1e-12) {
        std::cerr << "Denominator is too small; update is not valid." << std::endl;
        return 1;
    }

    // Compute numerator: A_inv * u * v^T * A_inv
    double uvT[n][n], Avu[n][n];
    outer_product(temp_vec, v, uvT); // uvT = A_inv * u * v^T
    mat_mul(uvT, A_inv, Avu);        // Avu = uvT * A_inv

    // Scale numerator by 1 / denominator
    double scaled_numerator[n][n];
    scalar_mat_mul(1.0 / denominator, Avu, scaled_numerator);

    // Compute updated inverse: A_inv - scaled_numerator
    double A_updated_inv[n][n];
    mat_subtract(A_inv, scaled_numerator, A_updated_inv);

    // Output results
    std::cout << "Original matrix A:" << std::endl;
    print_matrix(A);
    std::cout << "Inverse of A:" << std::endl;
    print_matrix(A_inv);
    std::cout << "Updated inverse (A + uv^T)^-1:" << std::endl;
    print_matrix(A_updated_inv);

    return 0;
}

// Function to compute matrix-vector multiplication
void mat_vec_mul(const double mat[n][n], const double vec[n], double result[n]) {
    for (int i = 0; i < n; ++i) {
        result[i] = 0.0;
        for (int j = 0; j < n; ++j) {
            result[i] += mat[i][j] * vec[j];
        }
    }
}

// Function to compute dot product of two vectors
double dot_product(const double vec1[n], const double vec2[n]) {
    double result = 0.0;
    for (int i = 0; i < n; ++i) {
        result += vec1[i] * vec2[i];
    }
    return result;
}

// Function to compute outer product of two vectors
void outer_product(const double vec1[n], const double vec2[n], double result[n][n]) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            result[i][j] = vec1[i] * vec2[j];
        }
    }
}

// Function to compute matrix-matrix multiplication
void mat_mul(const double mat1[n][n], const double mat2[n][n], double result[n][n]) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            result[i][j] = 0.0;
            for (int k = 0; k < n; ++k) {
                result[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }
}

// Function to scale a matrix by a scalar
void scalar_mat_mul(double scalar, const double mat[n][n], double result[n][n]) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            result[i][j] = scalar * mat[i][j];
        }
    }
}

// Function to subtract two matrices
void mat_subtract(const double mat1[n][n], const double mat2[n][n], double result[n][n]) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            result[i][j] = mat1[i][j] - mat2[i][j];
        }
    }
}

// Function to print a matrix
void print_matrix(const double mat[n][n]) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cout << std::setw(10) << std::fixed << std::setprecision(4) << mat[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}
