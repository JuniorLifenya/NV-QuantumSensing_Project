
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import os

os.makedirs('figures', exist_ok=True)

# Physical constants (SI)
hbar  = 1.054571817e-34
m_e   = 9.10938356e-31
c     = 2.99792458e8
G     = 6.67430e-11
eV    = 1.60217663e-19
alpha = 1/137.035999
a_0   = hbar/(m_e*alpha*c)
l_Pl  = np.sqrt(hbar*G/c**3)

# ─── Shared style ──────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':'serif',
    'font.serif':['Palatino','Georgia','Times New Roman','DejaVu Serif'],
    'font.size':11,
    'axes.labelsize':12,
    'axes.titlesize':11,
    'legend.fontsize':9.5,
    'axes.spines.top':False,
    'axes.spines.right':False,
    'axes.grid':True,
    'grid.alpha':0.22,
    'grid.linewidth':0.5,
    'figure.dpi':150,
    'lines.linewidth':2.0,
    'xtick.direction':'in',
    'ytick.direction':'in',
})

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Decoherence Budget vs. GW Phase Target
# ══════════════════════════════════════════════════════════════════════════════

def fig_decoherence_budget():
    """
    Shows the decoherence T₂ hierarchy for NV centers against the required
    integration time to detect a GW phase signal.
    The gap is the central experimental challenge of the thesis.
    """
    # NV center coherence times (seconds) — state-of-the-art literature values
    sources = [
        # (T2 in seconds, name, source, color)
        (3e-6,  r'$^{13}$C nuclear spin bath',    'Typ. NV in nat. diamond', '#e05a2b'),
        (1e-5,  r'Isotopically purified $^{12}$C', 'Balasubramanian+ 2009',  '#e08a2b'),
        (1e-3,  r'$T_2$ echo (dynamical decoup.)', 'Bar-Gill+ 2013',         '#e0c03a'),
        (1e-2,  r'$T_2$ (DD, 10ms record)',        'Herbschleb+ 2019',       '#6ec83a'),
        (0.1,   r'Nuclear spin $T_2$ (NV + $^{15}$N)', 'Maurer+ 2012',       '#3ab0e0'),
        (1e3,   r'Required: $\phi_{GW}\sim1$ rad', 'This thesis eq. (5.X)',  '#9060e0'),
    ]

    # Required coherence: φ = g*h/(hbar*omega)*T ~ 1 rad → T ~ hbar*omega/(g*h)
    # For NV electron, r~1nm, f=100Hz, h=1e-21
    omega_GW = 2*np.pi*100.0
    r_NV = 1e-9
    g_NV = m_e * omega_GW**2 * r_NV**2 / (4*hbar)  # rad/s per unit h
    T_required = hbar * omega_GW / (g_NV * 1e-21 * omega_GW)  # to get phi~1
    # Actually T for phi = 1: phi = g*h*T/(hbar) → T = hbar/(g*h)
    T_req_correct = hbar / (g_NV * 1e-21)
    print(f"  Required T for phi=1 (NV, r=1nm, h=1e-21): {T_req_correct:.2e} s")

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_facecolor('#fafaf8')

    T_vals = [s[0] for s in sources]
    names  = [s[1] for s in sources]
    refs   = [s[2] for s in sources]
    colors = [s[3] for s in sources]

    y = np.arange(len(sources))
    bars = ax.barh(y, [np.log10(t) for t in T_vals],
                   color=colors, edgecolor='white', lw=0.5, height=0.65, alpha=0.88)

    # Annotate values
    for i, (t, c) in enumerate(zip(T_vals, colors)):
        ax.text(np.log10(t)+0.12, i, f'{t:.0e} s', va='center', fontsize=9, color=c)

    # Vertical line at T2=10ms (best NV echo)
    ax.axvline(np.log10(1e-2), color='#6ec83a', lw=1.5, ls='--', alpha=0.7)
    ax.text(np.log10(1e-2)+0.06, 5.5, 'Best NV\n$T_2$=10ms', fontsize=8.5, color='#6ec83a', va='top')

    # Vertical line at required
    ax.axvline(np.log10(T_req_correct), color='#9060e0', lw=2, ls='--', alpha=0.8)
    ax.text(np.log10(T_req_correct)+0.06, 5.5,
            f'Required\nT≈{T_req_correct:.0e}s', fontsize=8.5, color='#9060e0', va='top')

    # Gap annotation
    gap_x1 = np.log10(1e-2)
    gap_x2 = np.log10(T_req_correct)
    gap_y  = -0.65
    ax.annotate('', xy=(gap_x2, gap_y), xytext=(gap_x1, gap_y),
                arrowprops=dict(arrowstyle='<->', color='#cc4444', lw=1.8))
    ax.text((gap_x1+gap_x2)/2, gap_y-0.3,
            f'Gap: {abs(gap_x2-gap_x1):.0f} orders of magnitude',
            ha='center', fontsize=9.5, color='#cc4444', fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels([f'{n}\n{r}' for n,r in zip(names,refs)], fontsize=9)
    ax.set_xlabel(r'$\log_{10}(T_2\;[\mathrm{s}])$', fontsize=11)
    ax.set_title('NV center decoherence budget vs. required GW integration time\n'
                 r'($h_+=10^{-21}$, $f=100$ Hz, $\langle r\rangle=1$ nm, NV electron)',
                 fontsize=11)

    # Reference comparison
    ref_colors = {'#e05a2b':'Literature','#6ec83a':'State-of-art','#9060e0':'GW target'}
    patches = [mpatches.Patch(color=c, label=l) for c,l in ref_colors.items()]
    ax.legend(handles=patches, fontsize=9, loc='lower right')

    ax.set_xlim(-7, 8)
    ax.set_ylim(-1.2, len(sources)-0.3)
    ax.grid(axis='x', alpha=0.25)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.tight_layout()
    plt.savefig('figures/decoherence_budget.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('saved: figures/decoherence_budget.png')
if __name__ == '__main__':
    print('Generating new thesis figures...')
    fig_decoherence_budget()
