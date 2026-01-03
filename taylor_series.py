"""
Taylor Series Implementation
============================
Implementation of Taylor series expansion for function approximation.

Taylor series: f(x) = Σ(n=0 to ∞) [fⁿ(a)/n!] * (x-a)ⁿ

where fⁿ(a) is the nth derivative of f evaluated at point a.
"""

import numpy as np
import matplotlib.pyplot as plt
import math

def numerical_derivative(func, x, n=1, dx=1e-5):
    """
    Compute nth derivative of a function at point x using finite differences.
    
    Parameters:
    -----------
    func : callable
        Function to differentiate
    x : float
        Point at which to compute derivative
    n : int
        Order of derivative
    dx : float
        Step size for finite differences
    
    Returns:
    --------
    derivative : float
        nth derivative at x
    """
    if n == 0:
        return func(x)
    elif n == 1:
        return (func(x + dx) - func(x - dx)) / (2 * dx)
    else:
        # Recursive: compute derivative of (n-1)th derivative
        def df(x_val):
            return numerical_derivative(func, x_val, n-1, dx)
        return numerical_derivative(df, x, 1, dx)

def taylor_series(func, a, n_terms, x_range):
    """
    Compute Taylor series approximation of a function.
    
    Parameters:
    -----------
    func : callable
        Function to approximate
    a : float
        Point around which to expand (center of expansion)
    n_terms : int
        Number of terms in the series
    x_range : array
        x values at which to evaluate the series
    
    Returns:
    --------
    approximation : array
        Taylor series approximation at each x
    """
    approximation = np.zeros_like(x_range)
    
    for n in range(n_terms):
        # Compute nth derivative at point a
        f_n = numerical_derivative(func, a, n=n, dx=1e-5)
        
        # Compute term: [fⁿ(a)/n!] * (x-a)ⁿ
        term = (f_n / math.factorial(n)) * (x_range - a)**n
        approximation += term
    
    return approximation

def taylor_sin(x, a=0, n_terms=10):
    """
    Taylor series for sin(x) around point a.
    
    sin(x) = Σ(n=0 to ∞) [(-1)ⁿ/(2n+1)!] * (x-a)^(2n+1)
    For a=0: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
    """
    result = np.zeros_like(x)
    for n in range(n_terms):
        term = ((-1)**n / math.factorial(2*n + 1)) * (x - a)**(2*n + 1)
        result += term
    return result

def taylor_cos(x, a=0, n_terms=10):
    """
    Taylor series for cos(x) around point a.
    
    cos(x) = Σ(n=0 to ∞) [(-1)ⁿ/(2n)!] * (x-a)^(2n)
    For a=0: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
    """
    result = np.zeros_like(x)
    for n in range(n_terms):
        term = ((-1)**n / math.factorial(2*n)) * (x - a)**(2n)
        result += term
    return result

def taylor_exp(x, a=0, n_terms=10):
    """
    Taylor series for exp(x) around point a.
    
    exp(x) = Σ(n=0 to ∞) [1/n!] * (x-a)ⁿ
    For a=0: exp(x) = 1 + x + x²/2! + x³/3! + ...
    """
    result = np.zeros_like(x)
    for n in range(n_terms):
        term = (1.0 / math.factorial(n)) * (x - a)**n
        result += term
    return result

def taylor_ln(x, a=1, n_terms=20):
    """
    Taylor series for ln(x) around point a.
    
    ln(x) = ln(a) + Σ(n=1 to ∞) [(-1)^(n+1)/(n*aⁿ)] * (x-a)ⁿ
    For a=1: ln(x) = (x-1) - (x-1)²/2 + (x-1)³/3 - ...
    """
    result = np.zeros_like(x)
    result += math.log(a)  # ln(a) term
    
    for n in range(1, n_terms):
        term = ((-1)**(n+1) / (n * a**n)) * (x - a)**n
        result += term
    
    return result

def plot_taylor_approximation(func, func_name, taylor_func, a=0, 
                              x_range=None, n_terms_list=[1, 3, 5, 10, 20]):
    """
    Plot Taylor series approximation with increasing number of terms.
    
    Parameters:
    -----------
    func : callable
        Actual function to approximate
    func_name : str
        Name of the function (for labels)
    taylor_func : callable
        Taylor series function (x, a, n_terms) -> approximation
    a : float
        Expansion point
    x_range : array, optional
        x values to plot. If None, uses appropriate range.
    n_terms_list : list
        List of number of terms to show
    """
    if x_range is None:
        # Default range based on function
        if 'sin' in func_name.lower() or 'cos' in func_name.lower():
            x_range = np.linspace(-2*np.pi, 2*np.pi, 1000)
        elif 'exp' in func_name.lower():
            x_range = np.linspace(-2, 2, 1000)
        elif 'ln' in func_name.lower():
            x_range = np.linspace(0.1, 3, 1000)
        else:
            x_range = np.linspace(-3, 3, 1000)
    
    # Compute actual function
    try:
        y_actual = func(x_range)
    except:
        # Handle cases where function might fail (e.g., ln for x <= 0)
        valid_mask = np.isfinite(func(x_range))
        x_range = x_range[valid_mask]
        y_actual = func(x_range)
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: All approximations
    ax1 = axes[0, 0]
    ax1.plot(x_range, y_actual, 'k-', linewidth=3, label='Actual', alpha=0.8)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(n_terms_list)))
    for i, n_terms in enumerate(n_terms_list):
        y_taylor = taylor_func(x_range, a, n_terms)
        ax1.plot(x_range, y_taylor, '--', linewidth=1.5, 
               color=colors[i], alpha=0.7, label=f'{n_terms} terms')
    
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('f(x)', fontsize=12)
    ax1.set_title(f'Taylor Series Approximation: {func_name}', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Error analysis
    ax2 = axes[0, 1]
    for i, n_terms in enumerate(n_terms_list):
        y_taylor = taylor_func(x_range, a, n_terms)
        error = np.abs(y_actual - y_taylor)
        ax2.semilogy(x_range, error, linewidth=1.5, 
                    color=colors[i], label=f'{n_terms} terms')
    
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('|Error|', fontsize=12)
    ax2.set_title('Error Analysis (Log Scale)', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Convergence at specific point
    ax3 = axes[1, 0]
    test_x = a + 1.0  # Test point away from expansion center
    n_terms_range = np.arange(1, 30)
    
    try:
        actual_value = func(test_x)
    except:
        actual_value = func(a + 0.5)
        test_x = a + 0.5
    
    errors = []
    for n in n_terms_range:
        y_taylor = taylor_func(np.array([test_x]), a, n)
        error = np.abs(actual_value - y_taylor[0])
        errors.append(error)
    
    ax3.semilogy(n_terms_range, errors, 'b-o', linewidth=2, markersize=4)
    ax3.set_xlabel('Number of Terms', fontsize=12)
    ax3.set_ylabel('|Error|', fontsize=12)
    ax3.set_title(f'Convergence at x = {test_x:.2f}', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Radius of convergence visualization
    ax4 = axes[1, 1]
    # Show approximation quality vs distance from expansion point
    distances = np.linspace(0, 3, 100)
    n_terms_fixed = 10
    
    errors_at_distance = []
    for dist in distances:
        test_x = a + dist
        try:
            actual_value = func(test_x)
            y_taylor = taylor_func(np.array([test_x]), a, n_terms_fixed)
            error = np.abs(actual_value - y_taylor[0])
            errors_at_distance.append(error)
        except:
            errors_at_distance.append(np.nan)
    
    ax4.semilogy(distances, errors_at_distance, 'r-o', linewidth=2, markersize=3)
    ax4.set_xlabel('Distance from Expansion Point', fontsize=12)
    ax4.set_ylabel('|Error|', fontsize=12)
    ax4.set_title(f'Error vs Distance (n={n_terms_fixed} terms)', fontsize=14)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'taylor_series_{func_name.lower()}.png', dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Example 1: sin(x)
    print("Taylor Series Implementation...")
    print("Example 1: sin(x)")
    plot_taylor_approximation(
        func=np.sin,
        func_name='sin(x)',
        taylor_func=taylor_sin,
        a=0,
        n_terms_list=[1, 3, 5, 10, 20]
    )
    
    # Example 2: cos(x)
    print("\nExample 2: cos(x)")
    plot_taylor_approximation(
        func=np.cos,
        func_name='cos(x)',
        taylor_func=taylor_cos,
        a=0,
        n_terms_list=[1, 3, 5, 10, 20]
    )
    
    # Example 3: exp(x)
    print("\nExample 3: exp(x)")
    plot_taylor_approximation(
        func=np.exp,
        func_name='exp(x)',
        taylor_func=taylor_exp,
        a=0,
        n_terms_list=[1, 3, 5, 10, 20]
    )
    
    # Example 4: ln(x)
    print("\nExample 4: ln(x)")
    x_range_ln = np.linspace(0.1, 3, 1000)
    plot_taylor_approximation(
        func=np.log,
        func_name='ln(x)',
        taylor_func=taylor_ln,
        a=1,
        x_range=x_range_ln,
        n_terms_list=[1, 3, 5, 10, 20]
    )
    
    # Example 5: Custom function
    print("\nExample 5: Custom function f(x) = x² * exp(-x)")
    def custom_func(x):
        return x**2 * np.exp(-x)
    
    def taylor_custom(x, a=0, n_terms=10):
        # For f(x) = x² * exp(-x), we can compute derivatives analytically
        # or use numerical differentiation
        result = np.zeros_like(x)
        for n in range(n_terms):
            # Compute nth derivative at a
            def f(x_val):
                return x_val**2 * np.exp(-x_val)
            f_n = numerical_derivative(f, a, n=n, dx=1e-5)
            
            term = (f_n / math.factorial(n)) * (x - a)**n
            result += term
        return result
    
    plot_taylor_approximation(
        func=custom_func,
        func_name='x²exp(-x)',
        taylor_func=taylor_custom,
        a=1,
        x_range=np.linspace(0, 4, 1000),
        n_terms_list=[1, 3, 5, 10, 15]
    )

