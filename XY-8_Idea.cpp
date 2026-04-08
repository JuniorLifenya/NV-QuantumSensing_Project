// XY8 filter function — from Degen, Reinhard, Cappellaro (Rev. Mod. Phys. 2017)
// W(f, tau, n) peaks when f = k/(2*tau), k = 1,3,5,...
// Plot for a publication-quality figure.

#include <cmath>
#include <vector>
#include <iostream>

double xy8_filter(double f_ac, double tau, int n_pulses) {
    double numerator   = std::sin(M_PI * f_ac * n_pulses * tau);
    double denominator = M_PI * f_ac * n_pulses * tau;
    double sinc_term   = (denominator < 1e-12) ? 1.0 : numerator / denominator;
    double sec_term    = 1.0 / std::cos(M_PI * f_ac * tau); // diverges at resonance
    return std::abs(sinc_term * sec_term);
}

int main() {
    double tau = 0.5e-3;        // 0.5 ms → resonant at f = 1/(2*tau) = 1 kHz
    int    N   = 64;             // 64 pulses, like the paper
    
    for (double f = 100; f < 5000; f += 10) {  // sweep 100 Hz to 5 kHz
        std::cout << f << "\t" << xy8_filter(f, tau, N) << "\n";
    }
    // Redirect this output to a file, plot with Python/gnuplot
    // You will see a SHARP PEAK at f = 1 kHz — this is your "detector tuned to 1 kHz"
}