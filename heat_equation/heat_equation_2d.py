"""
2D Heat Equation Solver
========================
Solves the 2D heat equation: ∂u/∂t = α(∂²u/∂x² + ∂²u/∂y²)

Using Finite Difference Method with Forward Time, Centered Space (FTCS) scheme.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable

def solve_heat_equation_2d(Lx=1.0, Ly=1.0, T=0.1, alpha=0.01, 
                           nx=50, ny=50, nt=200,
                           initial_condition=None,
                           boundary_conditions='zero',
                           base_temperature=25.0,
                           point_temperatures=None):
    """
    Solve 2D heat equation using finite difference method.
    
    Parameters:
    -----------
    Lx, Ly : float
        Domain dimensions in x and y directions
    T : float
        Total time to simulate
    alpha : float
        Thermal diffusivity coefficient
    nx, ny : int
        Number of grid points in x and y directions
    nt : int
        Number of time steps
    initial_condition : function or array, optional
        Initial temperature distribution u(x, y, t=0)
        If function, should accept (x, y) and return temperature
        If None, uses a Gaussian distribution
    boundary_conditions : str or dict
        'zero' for zero temperature at all boundaries
        'insulated' for zero flux (Neumann) at boundaries
        dict with keys 'left', 'right', 'top', 'bottom' for custom values
    base_temperature : float
        Base/ambient temperature of the plate (default: 25°C)
    point_temperatures : dict, optional
        Dictionary with point positions and temperatures, e.g. {(0.3, 0.3): 100.0, (0.7, 0.7): 80.0}
    
    Returns:
    --------
    x, y : arrays
        Spatial grid points
    t : array
        Time points
    u : array
        Temperature distribution u(x, y, t) of shape (nt, ny, nx)
    """
    # Spatial and time discretization
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Ly, ny)
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)
    t = np.linspace(0, T, nt)
    dt = T / (nt - 1)
    
    # Create meshgrid
    X, Y = np.meshgrid(x, y)
    
    # Stability condition: dt <= min(dx², dy²)/(4*alpha)
    stability_dt = min(dx**2, dy**2) / (4 * alpha)
    if dt > stability_dt:
        print(f"Warning: Stability condition may be violated!")
        print(f"dt = {dt:.6f}, required dt <= {stability_dt:.6f}")
    
    # Initialize solution array with base temperature: u[time, y, x]
    u = np.full((nt, ny, nx), base_temperature)
    
    # Set initial condition
    if initial_condition is None:
        # Start with base temperature everywhere
        u[0, :, :] = base_temperature
    elif callable(initial_condition):
        u[0, :, :] = initial_condition(X, Y)
    else:
        u[0, :, :] = initial_condition
    
    # Apply point temperatures if specified
    # Create hot spots (small area) instead of single point spikes
    if point_temperatures is not None:
        # Hot spot width (as fraction of domain size)
        hot_spot_width = 0.15  # 5% of domain size for hot spot area
        sigma_x = hot_spot_width * Lx  # Standard deviation for Gaussian in x direction
        sigma_y = hot_spot_width * Ly  # Standard deviation for Gaussian in y direction
        
        for (px, py), temp in point_temperatures.items():
            # Create 2D Gaussian hot spot around the point (px, py)
            # Distance squared from each grid point to the hot spot center
            X_centered = X - px
            Y_centered = Y - py
            distance_sq = (X_centered**2) / (sigma_x**2) + (Y_centered**2) / (sigma_y**2)
            
            # 2D Gaussian distribution
            gaussian = np.exp(-distance_sq / 2)
            
            # Apply hot spot: blend between base temperature and target temperature
            hot_spot_temp = base_temperature + (temp - base_temperature) * gaussian
            
            # Update initial condition with hot spot (take maximum to preserve other hot spots)
            u[0, :, :] = np.maximum(u[0, :, :], hot_spot_temp)
    
    # Apply boundary conditions to initial condition
    if boundary_conditions == 'zero':
        u[0, 0, :] = base_temperature   # bottom
        u[0, -1, :] = base_temperature  # top
        u[0, :, 0] = base_temperature   # left
        u[0, :, -1] = base_temperature  # right
    elif isinstance(boundary_conditions, dict):
        # Set boundaries, defaulting to base_temperature if not specified
        u[0, 0, :] = boundary_conditions.get('bottom', base_temperature)
        u[0, -1, :] = boundary_conditions.get('top', base_temperature)
        u[0, :, 0] = boundary_conditions.get('left', base_temperature)
        u[0, :, -1] = boundary_conditions.get('right', base_temperature)
    
    # Finite difference coefficients
    rx = alpha * dt / (dx**2)
    ry = alpha * dt / (dy**2)
    
    # Time stepping using FTCS scheme
    for n in range(0, nt - 1):
        # Interior points: 5-point stencil
        # u[i,j]^(n+1) = u[i,j]^n + rx*(u[i,j+1]^n - 2*u[i,j]^n + u[i,j-1]^n)
        #                  + ry*(u[i+1,j]^n - 2*u[i,j]^n + u[i-1,j]^n)
        
        # Second derivative in x direction (for interior points only)
        d2u_dx2 = (u[n, 1:-1, 2:] - 2*u[n, 1:-1, 1:-1] + u[n, 1:-1, :-2])
        
        # Second derivative in y direction (for interior points only)
        d2u_dy2 = (u[n, 2:, 1:-1] - 2*u[n, 1:-1, 1:-1] + u[n, :-2, 1:-1])
        
        # Update interior points
        u[n+1, 1:-1, 1:-1] = (u[n, 1:-1, 1:-1] + 
                              rx * d2u_dx2 + 
                              ry * d2u_dy2)
        
        # Apply boundary conditions
        if boundary_conditions == 'zero':
            # Base temperature at all boundaries
            u[n+1, 0, :] = base_temperature   # bottom
            u[n+1, -1, :] = base_temperature  # top
            u[n+1, :, 0] = base_temperature   # left
            u[n+1, :, -1] = base_temperature  # right
        elif isinstance(boundary_conditions, dict):
            # Custom boundary temperatures
            if 'bottom' in boundary_conditions:
                u[n+1, 0, :] = boundary_conditions['bottom']
            if 'top' in boundary_conditions:
                u[n+1, -1, :] = boundary_conditions['top']
            if 'left' in boundary_conditions:
                u[n+1, :, 0] = boundary_conditions['left']
            if 'right' in boundary_conditions:
                u[n+1, :, -1] = boundary_conditions['right']
        elif boundary_conditions == 'insulated':
            # Zero flux (Neumann): derivative = 0
            # Use forward/backward differences
            u[n+1, 0, :] = u[n+1, 1, :]      # bottom
            u[n+1, -1, :] = u[n+1, -2, :]   # top
            u[n+1, :, 0] = u[n+1, :, 1]     # left
            u[n+1, :, -1] = u[n+1, :, -2]   # right
        elif isinstance(boundary_conditions, dict):
            # Custom boundary conditions
            if 'bottom' in boundary_conditions:
                u[n+1, 0, :] = boundary_conditions['bottom']
            if 'top' in boundary_conditions:
                u[n+1, -1, :] = boundary_conditions['top']
            if 'left' in boundary_conditions:
                u[n+1, :, 0] = boundary_conditions['left']
            if 'right' in boundary_conditions:
                u[n+1, :, -1] = boundary_conditions['right']
    
    return x, y, t, u

def plot_heat_equation_2d(x, y, t, u, save_animation=False, show_heat_flow=True):
    """
    Plot the solution of 2D heat equation with custom colormap and heat flow visualization.
    
    Parameters:
    -----------
    x, y : arrays
        Spatial grid points
    t : array
        Time points
    u : array
        Temperature distribution of shape (nt, ny, nx)
    save_animation : bool
        Whether to save animation as GIF
    show_heat_flow : bool
        Whether to show heat flow vectors (gradient arrows)
    """
    X, Y = np.meshgrid(x, y)
    
    # Custom colormap: Dark Blue (coldest) -> Blue -> Cyan -> Green -> Yellow -> Orange -> Red -> Dark Red (hottest)
    # No black, darkest is dark blue and dark red
    from matplotlib.colors import LinearSegmentedColormap
    colors_list = ['darkblue', 'blue', 'cyan', 'lightgreen', 'yellow', 'orange', 'red', 'darkred']
    n_bins = 256
    cmap = LinearSegmentedColormap.from_list('custom_heat_2d', colors_list, N=n_bins)
    vmin, vmax = u.min(), u.max()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 12))
    
    # Plot 1-4: Temperature distribution at different times with heat flow
    time_indices = np.linspace(0, len(t)-1, 4, dtype=int)
    
    for i, idx in enumerate(time_indices):
        ax = fig.add_subplot(2, 3, i+1)
        im = ax.contourf(X, Y, u[idx, :, :], levels=30, cmap=cmap, 
                        vmin=vmin, vmax=vmax, extend='both')
        
        # Add heat flow vectors (gradient shows direction of heat flow)
        if show_heat_flow:
            # Calculate temperature gradient (heat flows from hot to cold, opposite to gradient)
            grad_y, grad_x = np.gradient(u[idx, :, :])
            # Heat flows opposite to gradient (from hot to cold)
            # Downsample for clarity
            skip = max(1, len(x) // 15)  # Show ~15 arrows in each direction
            X_sub = X[::skip, ::skip]
            Y_sub = Y[::skip, ::skip]
            grad_x_sub = -grad_x[::skip, ::skip]  # Negative for heat flow direction
            grad_y_sub = -grad_y[::skip, ::skip]
            
            # Normalize arrow lengths
            magnitude = np.sqrt(grad_x_sub**2 + grad_y_sub**2)
            max_mag = magnitude.max() if magnitude.max() > 0 else 1
            scale = 0.3 / max_mag  # Scale factor for arrow length
            
            ax.quiver(X_sub, Y_sub, grad_x_sub * scale, grad_y_sub * scale,
                     angles='xy', scale_units='xy', scale=1, 
                     color='white', alpha=0.6, width=0.003, headwidth=3, headlength=4)
        
        ax.set_xlabel('x (m)', fontsize=11)
        ax.set_ylabel('y (m)', fontsize=11)
        ax.set_title(f't = {t[idx]:.4f} s', fontsize=12)
        ax.set_aspect('equal')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Temperature (°C)', fontsize=10)
    
    # Plot 5: Heat balance - average temperature over time
    ax5 = fig.add_subplot(2, 3, 5)
    avg_temp = np.mean(u.reshape(len(t), -1), axis=1)
    ax5.plot(t, avg_temp, 'g-', linewidth=2, label='Average Temperature')
    ax5.axhline(y=vmin, color='b', linestyle='--', alpha=0.5, label='Min Temp')
    ax5.axhline(y=vmax, color='r', linestyle='--', alpha=0.5, label='Max Temp')
    ax5.set_xlabel('Time t (s)', fontsize=12)
    ax5.set_ylabel('Temperature', fontsize=12)
    ax5.set_title('Heat Balance: Average Temperature', fontsize=12)
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Temperature range over time
    ax6 = fig.add_subplot(2, 3, 6)
    min_temp = np.min(u.reshape(len(t), -1), axis=1)
    max_temp = np.max(u.reshape(len(t), -1), axis=1)
    ax6.fill_between(t, min_temp, max_temp, alpha=0.3, color='purple', label='Temp Range')
    ax6.plot(t, min_temp, 'b-', linewidth=1.5, label='Min Temp', alpha=0.7)
    ax6.plot(t, max_temp, 'r-', linewidth=1.5, label='Max Temp', alpha=0.7)
    ax6.set_xlabel('Time t (s)', fontsize=12)
    ax6.set_ylabel('Temperature', fontsize=12)
    ax6.set_title('Temperature Range Over Time', fontsize=12)
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.suptitle('2D Heat Equation: Temperature Distribution and Heat Balance', 
                 fontsize=14, y=0.995)
    plt.tight_layout()
    plt.savefig('heat_equation_2d_solution.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Create animation with heat flow
    fig_anim, ax_anim = plt.subplots(figsize=(12, 10))
    
    # Setup colorbar (persistent)
    divider = make_axes_locatable(ax_anim)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    # Initial plot
    im = ax_anim.contourf(X, Y, u[0, :, :], levels=30, cmap=cmap, 
                         vmin=vmin, vmax=vmax, extend='both')
    
    # Initial heat flow vectors
    if show_heat_flow:
        grad_y, grad_x = np.gradient(u[0, :, :])
        skip = max(1, len(x) // 15)
        X_sub = X[::skip, ::skip]
        Y_sub = Y[::skip, ::skip]
        grad_x_sub = -grad_x[::skip, ::skip]
        grad_y_sub = -grad_y[::skip, ::skip]
        magnitude = np.sqrt(grad_x_sub**2 + grad_y_sub**2)
        max_mag = magnitude.max() if magnitude.max() > 0 else 1
        scale = 0.3 / max_mag
        quiver = ax_anim.quiver(X_sub, Y_sub, grad_x_sub * scale, grad_y_sub * scale,
                               angles='xy', scale_units='xy', scale=1,
                               color='white', alpha=0.6, width=0.003, headwidth=3, headlength=4)
    
    ax_anim.set_xlabel('x (m)', fontsize=12)
    ax_anim.set_ylabel('y (m)', fontsize=12)
    ax_anim.set_title('2D Heat Equation Animation with Heat Flow', fontsize=14)
    ax_anim.set_aspect('equal')
    
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label('Temperature (°C)', fontsize=11)
    
    time_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes,
                            fontsize=12, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def animate(frame):
        # Clear only the contour and quiver, keep axes setup
        for coll in ax_anim.collections:
            coll.remove()
        for art in ax_anim.artists:
            art.remove()
        
        # Update contour
        im = ax_anim.contourf(X, Y, u[frame, :, :], levels=30, cmap=cmap,
                             vmin=vmin, vmax=vmax, extend='both')
        
        # Update heat flow vectors
        quiver_obj = None
        if show_heat_flow:
            grad_y, grad_x = np.gradient(u[frame, :, :])
            grad_x_sub = -grad_x[::skip, ::skip]
            grad_y_sub = -grad_y[::skip, ::skip]
            magnitude = np.sqrt(grad_x_sub**2 + grad_y_sub**2)
            max_mag = magnitude.max() if magnitude.max() > 0 else 1
            scale = 0.3 / max_mag
            quiver_obj = ax_anim.quiver(X_sub, Y_sub, grad_x_sub * scale, grad_y_sub * scale,
                                       angles='xy', scale_units='xy', scale=1,
                                       color='white', alpha=0.6, width=0.003, headwidth=3, headlength=4)
        
        # Update text with temperature info
        temp_min = u[frame, :, :].min()
        temp_max = u[frame, :, :].max()
        temp_avg = u[frame, :, :].mean()
        time_text.set_text(
            f'Time: t = {t[frame]:.4f} s\n'
            f'Min: {temp_min:.1f}°C\n'
            f'Max: {temp_max:.1f}°C\n'
            f'Avg: {temp_avg:.1f}°C'
        )
        if quiver_obj:
            return [im, quiver_obj]
        return [im]
    
    anim = FuncAnimation(fig_anim, animate, frames=len(t),
                        interval=100, blit=False, repeat=True)
    
    if save_animation:
        anim.save('heat_equation_2d_animation.gif', writer='pillow', fps=10)
    
    plt.tight_layout()
    plt.show()
    return anim

if __name__ == "__main__":
    # Example 1: Hot spots at corners with variable temperatures, Base: 25°C
    print("Solving 2D Heat Equation...")
    print("Example 1: Hot spots at corners with variable temperatures, Base: 25°C")
    
    x1, y1, t1, u1 = solve_heat_equation_2d(
        Lx=1.0, Ly=1.0, T=0.5, alpha=0.01,
        nx=100, ny=100, nt=500,
        base_temperature=25.0,
        point_temperatures={
            (0.1, 0.1): 100.0,    # Bottom-left: 100°C
            (0.9, 0.9): 80.0,     # Top-right: 80°C
            (0.1, 0.9): 60.0      # Top-left: 60°C
        },
        boundary_conditions={
            'left': 25.0,
            'right': 25.0,
            'top': 25.0,
            'bottom': 25.0
        }
    )
    
    plot_heat_equation_2d(x1, y1, t1, u1, show_heat_flow=True)
    
    # Example 2: Three hot spots at corners with different intensities, Base: 25°C
    print("\nExample 2: Three hot spots at corners (100°C, 70°C, 50°C), Base: 25°C")
    
    x2, y2, t2, u2 = solve_heat_equation_2d(
        Lx=1.0, Ly=1.0, T=0.6, alpha=0.01,
        nx=100, ny=100, nt=600,
        base_temperature=25.0,
        point_temperatures={
            (0.15, 0.15): 100.0,   # Bottom-left: 100°C (hottest)
            (0.85, 0.85): 70.0,    # Top-right: 70°C
            (0.85, 0.15): 50.0     # Bottom-right: 50°C
        },
        boundary_conditions={
            'left': 25.0,
            'right': 25.0,
            'top': 25.0,
            'bottom': 25.0
        }
    )
    plot_heat_equation_2d(x2, y2, t2, u2, show_heat_flow=True)
    
    # Example 3: Hot left, cold right, Base: 25°C
    print("\nExample 3: Hot left (100°C) to Cold right (0°C), Base: 25°C")
    
    x3, y3, t3, u3 = solve_heat_equation_2d(
        Lx=1.0, Ly=1.0, T=0.4, alpha=0.01,
        nx=100, ny=100, nt=400,
        base_temperature=25.0,
        boundary_conditions={
            'left': 100.0,   # Hot left
            'right': 0.0,    # Cold right
            'top': 25.0,     # Base temp
            'bottom': 25.0   # Base temp
        }
    )
    plot_heat_equation_2d(x3, y3, t3, u3, show_heat_flow=True)

