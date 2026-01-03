"""
1D Heat Equation Solver
========================
Solves the 1D heat equation: ∂u/∂t = α(∂²u/∂x²)

Using Finite Difference Method with Forward Time, Centered Space (FTCS) scheme.

Boundary Conditions:
- Dirichlet: Fixed temperature at boundaries
- Neumann: Fixed heat flux at boundaries
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def solve_heat_equation_1d(L=1.0, T=0.5, alpha=0.01, nx=100, nt=1000, 
                           initial_condition=None, boundary_left=None, 
                           boundary_right=None, boundary_type='dirichlet',
                           base_temperature=25.0, point_temperatures=None):
    """
    Solve 1D heat equation using finite difference method.
    
    Parameters:
    -----------
    L : float
        Length of the domain
    T : float
        Total time to simulate
    alpha : float
        Thermal diffusivity coefficient
    nx : int
        Number of spatial grid points
    nt : int
        Number of time steps
    initial_condition : function or array, optional
        Initial temperature distribution. If None, uses base_temperature.
    boundary_left : float, optional
        Left boundary condition value. If None, uses base_temperature.
    boundary_right : float, optional
        Right boundary condition value. If None, uses base_temperature.
    boundary_type : str
        'dirichlet' or 'neumann'
    base_temperature : float
        Base/ambient temperature of the rod (default: 25°C)
    point_temperatures : dict, optional
        Dictionary with point locations and temperatures.
        Keys: 'left', 'center', 'right' (e.g. {'left': 100.0, 'center': 80.0, 'right': 50.0})
    
    Returns:
    --------
    x : array
        Spatial grid points
    t : array
        Time points
    u : array
        Temperature distribution u(x, t)
    """
    # Spatial and time discretization
    x = np.linspace(0, L, nx)
    dx = L / (nx - 1)
    t = np.linspace(0, T, nt)
    dt = T / (nt - 1)
    
    # Stability condition: dt <= dx²/(2*alpha)
    stability = dt <= dx**2 / (2 * alpha)
    if not stability:
        print(f"Warning: Stability condition may be violated!")
        print(f"dt = {dt:.6f}, required dt <= {dx**2/(2*alpha):.6f}")
    
    # Initialize solution array with base temperature
    u = np.full((nt, nx), base_temperature)
    
    # Set boundary defaults
    if boundary_left is None:
        boundary_left = base_temperature
    if boundary_right is None:
        boundary_right = base_temperature
    
    # Set initial condition
    if initial_condition is None:
        # Start with base temperature everywhere
        u[0, :] = base_temperature
    elif callable(initial_condition):
        u[0, :] = initial_condition(x)
    else:
        u[0, :] = initial_condition
    
    # Apply point temperatures if specified (left, center, right)
    # Create hot spots (small area) instead of single point spikes
    if point_temperatures is not None:
        # Hot spot width (as fraction of domain length)
        hot_spot_width = 0.05  # 5% of domain length for hot spot area
        sigma = hot_spot_width * L  # Standard deviation for Gaussian distribution
        
        for location, temp in point_temperatures.items():
            location = location.lower()
            
            # Determine center position for hot spot
            if location == 'left':
                center_pos = x[0]  # Left end
            elif location == 'center':
                center_pos = L / 2  # Center
            elif location == 'right':
                center_pos = x[-1]  # Right end
            else:
                print(f"Warning: Unknown location '{location}'. Use 'left', 'center', or 'right'.")
                continue
            
            # Create Gaussian hot spot around the center position
            # Temperature distribution: base_temp + (temp - base_temp) * Gaussian
            distance_sq = (x - center_pos)**2
            gaussian = np.exp(-distance_sq / (2 * sigma**2))
            
            # Apply hot spot: blend between base temperature and target temperature
            hot_spot_temp = base_temperature + (temp - base_temperature) * gaussian
            
            # Update initial condition with hot spot (take maximum to preserve other hot spots)
            u[0, :] = np.maximum(u[0, :], hot_spot_temp)
    
    # Apply boundary conditions to initial condition
    if boundary_type == 'dirichlet':
        u[0, 0] = boundary_left
        u[0, -1] = boundary_right
    
    # Finite difference coefficient
    r = alpha * dt / (dx**2)
    
    # Time stepping using FTCS scheme
    for n in range(0, nt - 1):
        # Interior points: u[i]^(n+1) = u[i]^n + r*(u[i+1]^n - 2*u[i]^n + u[i-1]^n)
        u[n+1, 1:-1] = u[n, 1:-1] + r * (u[n, 2:] - 2*u[n, 1:-1] + u[n, :-2])
        
        # Apply boundary conditions
        if boundary_type == 'dirichlet':
            # Fixed temperature at boundaries
            u[n+1, 0] = boundary_left
            u[n+1, -1] = boundary_right
        elif boundary_type == 'neumann':
            # Fixed heat flux (derivative) at boundaries
            # Using forward/backward difference for boundaries
            u[n+1, 0] = u[n+1, 1] - boundary_left * dx
            u[n+1, -1] = u[n+1, -2] + boundary_right * dx
    
    return x, t, u

def plot_heat_equation_1d(x, t, u, save_animation=False, rod_height=0.1):
    """
    Plot the solution of 1D heat equation with rod visualization.
    
    Parameters:
    -----------
    x : array
        Spatial grid points
    t : array
        Time points
    u : array
        Temperature distribution
    save_animation : bool
        Whether to save animation as GIF
    rod_height : float
        Height of the rod visualization (for visual effect)
    """
    # Custom colormap: Dark Blue (coldest) -> Blue -> Cyan -> Green -> Yellow -> Orange -> Red -> Dark Red (hottest)
    # No black, darkest is dark blue and dark red
    from matplotlib.colors import LinearSegmentedColormap
    colors_list = ['darkblue', 'blue', 'cyan', 'lightgreen', 'yellow', 'orange', 'red', 'darkred']
    n_bins = 256
    cmap = LinearSegmentedColormap.from_list('custom_heat_1d', colors_list, N=n_bins)
    
    # Normalize temperature for colormap
    vmin, vmax = u.min(), u.max()
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    
    fig = plt.figure(figsize=(16, 10))
    
    # Plot 1: Rod visualization at different times
    ax1 = plt.subplot(2, 2, 1)
    time_indices = np.linspace(0, len(t)-1, 6, dtype=int)
    
    # Draw continuous rod (no section boundaries) colored by temperature
    for idx in time_indices:
        # Create continuous rod using fill_between for smooth gradient
        y_bottom = np.full_like(x, -rod_height/2)
        y_top = np.full_like(x, rod_height/2)
        colors_rod = [cmap(norm(temp)) for temp in u[idx, :]]
        
        # Draw rod as continuous filled area
        for i in range(len(x) - 1):
            x_segment = [x[i], x[i+1], x[i+1], x[i]]
            y_segment = [y_bottom[i], y_bottom[i+1], y_top[i+1], y_top[i]]
            ax1.fill(x_segment, y_segment, color=colors_rod[i], edgecolor='none', alpha=0.9)
    
    ax1.set_xlim(x[0] - 0.05, x[-1] + 0.05)
    ax1.set_ylim(-rod_height*2, rod_height*2)
    ax1.set_xlabel('Position x (m)', fontsize=12)
    ax1.set_ylabel('Rod Cross-section', fontsize=12)
    ax1.set_title('Rod Temperature Visualization (Multiple Times)', fontsize=14)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar1 = plt.colorbar(sm, ax=ax1)
    cbar1.set_label('Temperature', fontsize=11)
    
    # Plot 2: Temperature distribution line plot
    ax2 = plt.subplot(2, 2, 2)
    colors_plot = cmap(np.linspace(0, 1, len(time_indices)))
    for i, idx in enumerate(time_indices):
        ax2.plot(x, u[idx, :], color=colors_plot[i], 
                label=f't = {t[idx]:.3f}s', linewidth=2, alpha=0.8)
    
    ax2.set_xlabel('Position x (m)', fontsize=12)
    ax2.set_ylabel('Temperature', fontsize=12)
    ax2.set_title('Temperature Distribution Over Time', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Space-time heat map
    ax3 = plt.subplot(2, 2, 3)
    im = ax3.imshow(u.T, aspect='auto', origin='lower', 
                    extent=[t[0], t[-1], x[0], x[-1]], 
                    cmap=cmap, interpolation='bilinear', vmin=vmin, vmax=vmax)
    ax3.set_xlabel('Time t (s)', fontsize=12)
    ax3.set_ylabel('Position x (m)', fontsize=12)
    ax3.set_title('Space-Time Heat Map', fontsize=14)
    cbar3 = plt.colorbar(im, ax=ax3)
    cbar3.set_label('Temperature', fontsize=11)
    
    # Plot 4: Heat balance - average temperature over time
    ax4 = plt.subplot(2, 2, 4)
    avg_temp = np.mean(u, axis=1)
    ax4.plot(t, avg_temp, 'g-', linewidth=2, label='Average Temperature')
    ax4.axhline(y=vmin, color='b', linestyle='--', alpha=0.5, label='Min Temp')
    ax4.axhline(y=vmax, color='r', linestyle='--', alpha=0.5, label='Max Temp')
    ax4.set_xlabel('Time t (s)', fontsize=12)
    ax4.set_ylabel('Temperature', fontsize=12)
    ax4.set_title('Heat Balance: Average Temperature', fontsize=14)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('heat_equation_1d_solution.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Create animated rod visualization
    fig_anim, ax_anim = plt.subplots(figsize=(12, 6))
    ax_anim.set_xlim(x[0] - 0.05, x[-1] + 0.05)
    ax_anim.set_ylim(-rod_height*1.5, rod_height*1.5)
    ax_anim.set_xlabel('Position x (m)', fontsize=12)
    ax_anim.set_ylabel('Rod Cross-section', fontsize=12)
    ax_anim.set_title('1D Heat Equation: Rod Animation', fontsize=14)
    ax_anim.set_aspect('equal')
    ax_anim.grid(True, alpha=0.3)
    
    # Initialize continuous rod (no segments, will use fill_between)
    rod_polygons = []
    y_bottom = np.full_like(x, -rod_height/2)
    y_top = np.full_like(x, rod_height/2)
    
    # Create initial rod visualization
    for i in range(len(x) - 1):
        x_segment = [x[i], x[i+1], x[i+1], x[i]]
        y_segment = [y_bottom[i], y_bottom[i+1], y_top[i+1], y_top[i]]
        poly = plt.Polygon(list(zip(x_segment, y_segment)), 
                          facecolor='blue', edgecolor='none', alpha=0.9)
        ax_anim.add_patch(poly)
        rod_polygons.append(poly)
    
    # Add colorbar
    sm_anim = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm_anim.set_array([])
    cbar_anim = plt.colorbar(sm_anim, ax=ax_anim)
    cbar_anim.set_label('Temperature', fontsize=11)
    
    time_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes, 
                            fontsize=12, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def animate(frame):
        # Update continuous rod colors
        for i, poly in enumerate(rod_polygons):
            temp = u[frame, i]
            color = cmap(norm(temp))
            poly.set_facecolor(color)
        time_text.set_text(f'Time: t = {t[frame]:.4f} s\nTemp Range: [{u[frame].min():.1f}°C, {u[frame].max():.1f}°C]\nBase: 25°C')
        return rod_polygons + [time_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=len(t), 
                        interval=50, blit=False, repeat=True)
    
    if save_animation:
        anim.save('heat_equation_1d_animation.gif', writer='pillow', fps=20)
    
    plt.tight_layout()
    plt.show()
    return anim

if __name__ == "__main__":
    # Example 1: Hot left end (100°C), Cold right end (0°C), Base 25°C
    print("Solving 1D Heat Equation...")
    print("Example 1: Hot left (100°C) to Cold right (0°C), Base: 25°C")
    
    x1, t1, u1 = solve_heat_equation_1d(
        L=1.0, T=2.0, alpha=0.01, nx=100, nt=1000,
        boundary_left=100.0, boundary_right=100.0,
        base_temperature=25.0,
        boundary_type='dirichlet'
    )
    plot_heat_equation_1d(x1, t1, u1)
    
    # Example 2: Point temperatures at left, center, right
    print("\nExample 2: Point temperatures - Left: 100°C, Center: 80°C, Base: 25°C")
    
    x2, t2, u2 = solve_heat_equation_1d(
        L=1.0, T=1.5, alpha=0.01, nx=100, nt=800,
        base_temperature=25.0,
        point_temperatures={'left': 100.0, 'center': 100.0},  # Left and center hot spots
        boundary_type='dirichlet'
    )
    plot_heat_equation_1d(x2, t2, u2)
    
    # Example 3: Hot center with base temperature
    print("\nExample 3: Hot center (100°C), Base: 25°C")
    
    def hot_center(x):
        """Hot center, base temperature elsewhere"""
        L = x[-1] - x[0]
        center = L / 2
        return 25.0 + 75.0 * np.exp(-((x - center)**2) / (2 * 0.1**2))
    
    x3, t3, u3 = solve_heat_equation_1d(
        L=1.0, T=1.5, alpha=0.01, nx=100, nt=800,
        initial_condition=hot_center,
        base_temperature=25.0,
        boundary_type='dirichlet'
    )
    plot_heat_equation_1d(x3, t3, u3)

