// Ramsey sweep: vary tau from 0 to T2*, plot P(|0>) vs tau
// A GW shifts the oscillation frequency by delta_f = gamma_e * h
// YOU WILL SEE: two curves (with/without GW) oscillating at slightly different rates
// The frequency difference IS the signal.

std::vector<double> ramsey_sweep(double tau_max, int n_points, double h_strain) {
    std::vector<double> signal;
    signal.reserve(n_points);
    
    for (int i = 0; i < n_points; ++i) {
        double tau = tau_max * i / n_points;
        
        // Apply pi/2 pulse: rotate |0> → superposition (|0> + |+1>)/√2
        Vector3cd psi = (psi_p0 + psi_p1) / std::sqrt(2.0);
        
        // Free precession under H0 + GW perturbation for time tau
        psi = rk4_integrate(psi, 0.0, tau, h_strain);
        
        // Apply second pi/2 pulse then measure P(|0>)
        psi = apply_pi2_pulse(psi);
        signal.push_back(std::norm(psi_p0.dot(psi)));
    }
    return signal;
}
// The FFT of this signal gives you the frequency shift.
// h_strain != 0  =>  peak shifts by delta_f = gamma_e * h  =>  DETECTION.