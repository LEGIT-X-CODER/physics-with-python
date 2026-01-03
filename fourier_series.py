"""
Fourier Series Implementation
==============================
Implementation of Fourier series for periodic function decomposition.

Fourier series: f(x) = a₀/2 + Σ(n=1 to ∞) [aₙcos(nx) + bₙsin(nx)]

where:
    a₀ = (1/π) ∫[-π to π] f(x) dx
    aₙ = (1/π) ∫[-π to π] f(x)cos(nx) dx
    bₙ = (1/π) ∫[-π to π] f(x)sin(nx) dx
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def fourier_coefficients(func, n_terms, period=2*np.pi):
    """
    Calculate Fourier coefficients for a periodic function.
    
    Parameters:
    -----------
    func : callable
        Periodic function f(x)
    n_terms : int
        Number of terms in the series
    period : float
        Period of the function (default 2π)
    
    Returns:
    --------
    a0 : float
        DC component
    a_n : array
        Cosine coefficients
    b_n : array
        Sine coefficients
    """
    # Normalize to [-π, π] range
    L = period / 2
    
    # a0 coefficient
    def integrand_a0(x):
        return func(x * L / np.pi)
    
    a0, _ = quad(integrand_a0, -np.pi, np.pi)
    a0 = a0 / np.pi
    
    # a_n and b_n coefficients
    a_n = np.zeros(n_terms)
    b_n = np.zeros(n_terms)
    
    for n in range(1, n_terms + 1):
        # a_n coefficient
        def integrand_an(x):
            return func(x * L / np.pi) * np.cos(n * x)
        
        a_n[n-1], _ = quad(integrand_an, -np.pi, np.pi)
        a_n[n-1] = a_n[n-1] / np.pi
        
        # b_n coefficient
        def integrand_bn(x):
            return func(x * L / np.pi) * np.sin(n * x)
        
        b_n[n-1], _ = quad(integrand_bn, -np.pi, np.pi)
        b_n[n-1] = b_n[n-1] / np.pi
    
    return a0, a_n, b_n

def fourier_series(x, a0, a_n, b_n, period=2*np.pi):
    """
    Evaluate Fourier series at given points.
    
    Parameters:
    -----------
    x : array
        Points at which to evaluate
    a0 : float
        DC component
    a_n : array
        Cosine coefficients
    b_n : array
        Sine coefficients
    period : float
        Period of the function
    
    Returns:
    --------
    result : array
        Fourier series approximation
    """
    L = period / 2
    result = a0 / 2 * np.ones_like(x)
    
    # Normalize x to [-π, π] range
    x_norm = (x % period - period/2) * np.pi / L
    
    for n in range(1, len(a_n) + 1):
        result += a_n[n-1] * np.cos(n * x_norm) + b_n[n-1] * np.sin(n * x_norm)
    
    return result

def square_wave(x):
    """
    Square wave function: f(x) = 1 for 0 < x < π, -1 for π < x < 2π
    """
    return np.sign(np.sin(x))

def sawtooth_wave(x):
    """
    Sawtooth wave function: f(x) = (x mod 2π) / π - 1
    """
    return 2 * (x / (2*np.pi) - np.floor(x / (2*np.pi) + 0.5))

def triangle_wave(x):
    """
    Triangle wave function.
    """
    x_mod = x % (2*np.pi)
    return 2 * np.abs(2 * (x_mod / (2*np.pi) - np.floor(x_mod / (2*np.pi) + 0.5))) - 1

def plot_fourier_series(func, func_name, period=2*np.pi, 
                        n_terms_list=[1, 3, 5, 10, 20, 50]):
    """
    Plot Fourier series approximation with increasing number of terms.
    
    Parameters:
    -----------
    func : callable
        Periodic function to approximate
    func_name : str
        Name of the function (for labels)
    period : float
        Period of the function
    n_terms_list : list
        List of number of terms to show
    """
    # Generate x values over multiple periods
    x = np.linspace(-period, 3*period, 2000)
    y_actual = func(x)
    
    # Calculate Fourier coefficients for maximum terms
    max_terms = max(n_terms_list)
    a0, a_n, b_n = fourier_coefficients(func, max_terms, period)
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: All approximations
    ax1 = axes[0, 0]
    ax1.plot(x, y_actual, 'k-', linewidth=3, label='Actual', alpha=0.8)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(n_terms_list)))
    for i, n_terms in enumerate(n_terms_list):
        y_fourier = fourier_series(x, a0, a_n[:n_terms], b_n[:n_terms], period)
        ax1.plot(x, y_fourier, '--', linewidth=1.5,
                color=colors[i], alpha=0.7, label=f'{n_terms} terms')
    
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('f(x)', fontsize=12)
    ax1.set_title(f'Fourier Series Approximation: {func_name}', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(x[0], x[-1])
    
    # Plot 2: Error analysis
    ax2 = axes[0, 1]
    for i, n_terms in enumerate(n_terms_list):
        y_fourier = fourier_series(x, a0, a_n[:n_terms], b_n[:n_terms], period)
        error = np.abs(y_actual - y_fourier)
        ax2.semilogy(x, error, linewidth=1.5,
                    color=colors[i], label=f'{n_terms} terms')
    
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('|Error|', fontsize=12)
    ax2.set_title('Error Analysis (Log Scale)', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(x[0], x[-1])
    
    # Plot 3: Fourier coefficients
    ax3 = axes[1, 0]
    n_range = np.arange(1, len(a_n) + 1)
    ax3.stem(n_range, np.abs(a_n), basefmt=' ', label='|aₙ|', markerfmt='bo')
    ax3.stem(n_range, np.abs(b_n), basefmt=' ', label='|bₙ|', markerfmt='ro')
    ax3.set_xlabel('n (harmonic number)', fontsize=12)
    ax3.set_ylabel('|Coefficient|', fontsize=12)
    ax3.set_title('Fourier Coefficients', fontsize=14)
    ax3.set_yscale('log')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Convergence (RMS error vs number of terms)
    ax4 = axes[1, 1]
    n_terms_range = np.arange(1, min(100, len(a_n) + 1))
    rms_errors = []
    
    for n in n_terms_range:
        y_fourier = fourier_series(x, a0, a_n[:n], b_n[:n], period)
        rms_error = np.sqrt(np.mean((y_actual - y_fourier)**2))
        rms_errors.append(rms_error)
    
    ax4.semilogy(n_terms_range, rms_errors, 'g-o', linewidth=2, markersize=4)
    ax4.set_xlabel('Number of Terms', fontsize=12)
    ax4.set_ylabel('RMS Error', fontsize=12)
    ax4.set_title('Convergence of Fourier Series', fontsize=14)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'fourier_series_{func_name.lower().replace(" ", "_")}.png', 
                dpi=150, bbox_inches='tight')
    plt.show()
    
    # Print some coefficients
    print(f"\nFourier coefficients for {func_name}:")
    print(f"a₀ = {a0:.6f}")
    print(f"First 5 aₙ coefficients: {a_n[:5]}")
    print(f"First 5 bₙ coefficients: {b_n[:5]}")

def plot_fourier_components(func, func_name, period=2*np.pi, n_terms=10):
    """
    Plot individual Fourier components.
    """
    a0, a_n, b_n = fourier_coefficients(func, n_terms, period)
    
    x = np.linspace(-period, 3*period, 2000)
    y_actual = func(x)
    y_fourier = fourier_series(x, a0, a_n, b_n, period)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: DC component
    ax1 = axes[0, 0]
    ax1.plot(x, y_actual, 'k-', linewidth=2, label='Actual', alpha=0.5)
    ax1.axhline(y=a0/2, color='r', linestyle='--', linewidth=2, label='DC component (a₀/2)')
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('f(x)', fontsize=12)
    ax1.set_title('DC Component', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: First few harmonics
    ax2 = axes[0, 1]
    ax2.plot(x, y_actual, 'k-', linewidth=2, label='Actual', alpha=0.5)
    
    # Build up approximation term by term
    y_partial = (a0 / 2) * np.ones_like(x)
    L = period / 2
    x_norm = (x % period - period/2) * np.pi / L
    
    for n in range(1, min(6, n_terms + 1)):
        y_partial += a_n[n-1] * np.cos(n * x_norm) + b_n[n-1] * np.sin(n * x_norm)
        ax2.plot(x, y_partial, '--', linewidth=1.5, 
                label=f'Up to {n} harmonics', alpha=0.7)
    
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('f(x)', fontsize=12)
    ax2.set_title('Cumulative Harmonics', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Individual cosine components
    ax3 = axes[1, 0]
    for n in range(1, min(6, len(a_n) + 1)):
        component = a_n[n-1] * np.cos(n * x_norm)
        ax3.plot(x, component, linewidth=1.5, label=f'aₙcos({n}x), aₙ={a_n[n-1]:.3f}', alpha=0.7)
    ax3.set_xlabel('x', fontsize=12)
    ax3.set_ylabel('Amplitude', fontsize=12)
    ax3.set_title('Cosine Components', fontsize=14)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Individual sine components
    ax4 = axes[1, 1]
    for n in range(1, min(6, len(b_n) + 1)):
        component = b_n[n-1] * np.sin(n * x_norm)
        ax4.plot(x, component, linewidth=1.5, label=f'bₙsin({n}x), bₙ={b_n[n-1]:.3f}', alpha=0.7)
    ax4.set_xlabel('x', fontsize=12)
    ax4.set_ylabel('Amplitude', fontsize=12)
    ax4.set_title('Sine Components', fontsize=14)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'fourier_components_{func_name.lower().replace(" ", "_")}.png',
                dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Example 1: Square Wave
    print("Fourier Series Implementation...")
    print("Example 1: Square Wave")
    plot_fourier_series(square_wave, "Square Wave", period=2*np.pi,
                       n_terms_list=[1, 3, 5, 10, 20, 50])
    plot_fourier_components(square_wave, "Square Wave", period=2*np.pi, n_terms=10)
    
    # Example 2: Sawtooth Wave
    print("\nExample 2: Sawtooth Wave")
    plot_fourier_series(sawtooth_wave, "Sawtooth Wave", period=2*np.pi,
                       n_terms_list=[1, 3, 5, 10, 20, 50])
    
    # Example 3: Triangle Wave
    print("\nExample 3: Triangle Wave")
    plot_fourier_series(triangle_wave, "Triangle Wave", period=2*np.pi,
                       n_terms_list=[1, 3, 5, 10, 20, 50])
    
    # Example 4: Custom periodic function
    print("\nExample 4: Custom function f(x) = sin(x) + 0.5*sin(3x)")
    def custom_periodic(x):
        return np.sin(x) + 0.5 * np.sin(3*x)
    
    plot_fourier_series(custom_periodic, "sin(x) + 0.5sin(3x)", period=2*np.pi,
                       n_terms_list=[1, 3, 5, 10, 20])

