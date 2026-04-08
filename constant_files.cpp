// include/nvgw/gw_params.hpp
#pragma once
namespace nvgw {

// Physical constants (SI)
constexpr double hbar        = 1.0545718e-34; // J·s
constexpr double gamma_e_Hz  = 28.024e9;      // Hz/T — NV electron gyromagnetic ratio
constexpr double D_ZFS_Hz    = 2.87e9;        // Hz — NV zero-field splitting

// GW scenario: millisecond pulsar, h ~ 10^-24 (speculative high-freq)
// For simulation we sweep h_strain and show the threshold
constexpr double h_strain_ligo     = 1e-21;  // LIGO event floor
constexpr double h_strain_pulsar   = 1e-24;  // continuous wave estimate
constexpr double f_gw_target_Hz    = 1e3;    // 1 kHz — tune τ to match

// XY8 resonance condition: f_gw = 1/(2*tau)
// => tau = 1/(2*f_gw) = 0.5 ms for f_gw = 1 kHz
inline double tau_from_freq(double f_gw) { return 0.5 / f_gw; }

// Accumulated phase after N pulses, sensing time T
// phi = gamma_e * h_strain * sqrt(N_pulses * T2)  [approximate]
inline double accumulated_phase(double h, int N, double T2) {
    return gamma_e_Hz * h * std::sqrt(static_cast<double>(N) * T2);
}

} // namespace nvgw