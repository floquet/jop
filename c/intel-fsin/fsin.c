#include <math.h>

void PiAddition() {
    double pi_d = 3.14159265358979323846;
    double sin_d = sin(pi_d);
        printf(“pi = %.33f\n + %.33f\n”, pi_d, sin_d);

    char pi_s[100]; char sin_s[100]; char result_s[100] = {};
        snprintf(pi_s, sizeof(pi_s), “%.33f”, pi_d);
        snprintf(sin_s, sizeof(sin_s), “%.33f”, sin_d);
        int carry = 0;
        for (int i = strlen(pi_s) – 1; i >= 0; –i) {
            result_s[i] = pi_s[i];
            if (pi_s[i] != ‘.’) {
                char d = pi_s[i] + sin_s[i] + carry – ‘0’ * 2;
                carry = d > 9;
                result_s[i] = d % 10 + ‘0’;
            }
        }
        printf(” = %s\n”, result_s);
}
