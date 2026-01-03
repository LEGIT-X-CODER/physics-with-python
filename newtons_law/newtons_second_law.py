"""
Newton's Second Law of Motion
=============================
F = ma (Force = mass × acceleration)

This module demonstrates Newton's Second Law with various examples:
1. Constant force
2. Variable force
3. Multiple forces
4. Projectile motion with air resistance
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

class NewtonsSecondLaw:
    """
    Solver for Newton's Second Law: F = ma
    """
    def __init__(self, mass=1.0):
        """
        Initialize with mass.
        
        Parameters:
        -----------
        mass : float
            Mass of the object (kg)
        """
        self.mass = mass
    
    def solve_motion(self, force_func, initial_position=0.0, initial_velocity=0.0,
                    t_span=(0, 10), n_points=1000):
        """
        Solve motion using F = ma.
        
        Parameters:
        -----------
        force_func : callable
            Function F(t, x, v) that returns force at time t, position x, velocity v
        initial_position : float
            Initial position (m)
        initial_velocity : float
            Initial velocity (m/s)
        t_span : tuple
            (t_start, t_end)
        n_points : int
            Number of time points
        
        Returns:
        --------
        t : array
            Time points
        x : array
            Position at each time
        v : array
            Velocity at each time
        a : array
            Acceleration at each time
        """
        t = np.linspace(t_span[0], t_span[1], n_points)
        initial_state = np.array([initial_position, initial_velocity])
        
        def derivatives(state, t_val):
            x_val, v_val = state
            # Calculate force
            F = force_func(t_val, x_val, v_val)
            # Acceleration from F = ma
            a_val = F / self.mass
            # Derivatives: dx/dt = v, dv/dt = a
            return np.array([v_val, a_val])
        
        solution = odeint(derivatives, initial_state, t)
        x = solution[:, 0]
        v = solution[:, 1]
        
        # Calculate acceleration
        a = np.array([force_func(t[i], x[i], v[i]) / self.mass for i in range(len(t))])
        
        return t, x, v, a

def example_1_constant_force():
    """
    Example 1: Constant Force
    A constant force of 10N applied to a 2kg object.
    """
    print("Example 1: Constant Force (F = 10N, m = 2kg)")
    
    system = NewtonsSecondLaw(mass=2.0)
    
    def constant_force(t, x, v):
        return 10.0  # Constant 10N force
    
    t, x, v, a = system.solve_motion(
        force_func=constant_force,
        initial_position=0.0,
        initial_velocity=0.0,
        t_span=(0, 5),
        n_points=500
    )
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].plot(t, x, 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Time (s)', fontsize=12)
    axes[0, 0].set_ylabel('Position (m)', fontsize=12)
    axes[0, 0].set_title('Position vs Time', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(t, v, 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[0, 1].set_title('Velocity vs Time', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(t, a, 'g-', linewidth=2)
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Acceleration (m/s²)', fontsize=12)
    axes[1, 0].set_title('Acceleration vs Time', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=10.0/2.0, color='orange', linestyle='--', 
                       label=f'Expected: F/m = {10.0/2.0:.1f} m/s²')
    axes[1, 0].legend()
    
    # Phase space: velocity vs position
    axes[1, 1].plot(x, v, 'purple', linewidth=2)
    axes[1, 1].set_xlabel('Position (m)', fontsize=12)
    axes[1, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[1, 1].set_title('Phase Space (Velocity vs Position)', fontsize=14)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle("Newton's Second Law: Constant Force", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('newtons_law_example1_constant_force.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Visual demonstration: Box with force vector (separate text area)
    fig_anim = plt.figure(figsize=(14, 8))
    gs = fig_anim.add_gridspec(3, 1, height_ratios=[1, 4, 1], hspace=0.3)
    
    # Text area at top
    ax_text = fig_anim.add_subplot(gs[0])
    ax_text.axis('off')
    info_text = ax_text.text(0.5, 0.5, '', transform=ax_text.transAxes,
                            fontsize=12, ha='center', va='center',
                            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Main animation area
    ax_anim = fig_anim.add_subplot(gs[1])
    ax_anim.set_xlim(-1, max(x) + 2)
    ax_anim.set_ylim(-0.5, 1.5)
    ax_anim.set_xlabel('Position (m)', fontsize=12)
    ax_anim.set_ylabel('Height', fontsize=12)
    ax_anim.set_title("Visual: Box with Constant Force", fontsize=14)
    ax_anim.grid(True, alpha=0.3)
    ax_anim.set_aspect('equal')
    
    # Ground line
    ax_anim.axhline(y=0, color='brown', linewidth=3, label='Ground')
    
    # Box
    box_width = 0.5
    box_height = 0.5
    box = Rectangle((x[0], 0), box_width, box_height, 
                    facecolor='lightblue', edgecolor='black', linewidth=2)
    ax_anim.add_patch(box)
    
    # Force vector
    force_arrow = FancyArrowPatch((x[0] + box_width, box_height/2), 
                                  (x[0] + box_width + 1.0, box_height/2),
                                  arrowstyle='->', mutation_scale=20, 
                                  color='red', linewidth=3, label='Force F=10N')
    ax_anim.add_patch(force_arrow)
    
    def animate(frame):
        idx = frame * (len(t) // 200)  # Sample for animation
        if idx < len(t):
            box.set_x(x[idx])
            force_arrow.set_positions((x[idx] + box_width, box_height/2),
                                     (x[idx] + box_width + 1.0, box_height/2))
            info_text.set_text(f'Time: {t[idx]:.2f} s  |  Position: {x[idx]:.2f} m  |  '
                             f'Velocity: {v[idx]:.2f} m/s  |  Acceleration: {a[idx]:.2f} m/s²')
        return [box, force_arrow, info_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=50, blit=False, repeat=True)
    ax_anim.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

def example_2_spring_force():
    """
    Example 2: Spring Force (Hooke's Law)
    F = -kx (restoring force)
    """
    print("\nExample 2: Spring Force (F = -kx, k = 10 N/m, m = 1kg)")
    
    system = NewtonsSecondLaw(mass=1.0)
    k = 10.0  # Spring constant
    
    def spring_force(t, x, v):
        return -k * x  # Hooke's law
    
    t, x, v, a = system.solve_motion(
        force_func=spring_force,
        initial_position=1.0,  # Stretched 1m
        initial_velocity=0.0,
        t_span=(0, 5),
        n_points=1000
    )
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].plot(t, x, 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Time (s)', fontsize=12)
    axes[0, 0].set_ylabel('Position (m)', fontsize=12)
    axes[0, 0].set_title('Oscillatory Motion (Simple Harmonic)', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    axes[0, 1].plot(t, v, 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[0, 1].set_title('Velocity vs Time', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(t, a, 'g-', linewidth=2)
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Acceleration (m/s²)', fontsize=12)
    axes[1, 0].set_title('Acceleration vs Time', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Phase space: elliptical orbit
    axes[1, 1].plot(x, v, 'purple', linewidth=2)
    axes[1, 1].set_xlabel('Position (m)', fontsize=12)
    axes[1, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[1, 1].set_title('Phase Space (Elliptical Orbit)', fontsize=14)
    axes[1, 1].set_aspect('equal')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle("Newton's Second Law: Spring Force (Simple Harmonic Motion)", 
                 fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('newtons_law_example2_spring_force.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Visual demonstration: Spring compression and extension
    fig_anim, ax_anim = plt.subplots(figsize=(14, 6))
    equilibrium_x = 2.0  # Equilibrium position
    ax_anim.set_xlim(-1, 5)
    ax_anim.set_ylim(-0.5, 1.5)
    ax_anim.set_xlabel('Position (m)', fontsize=12)
    ax_anim.set_ylabel('Height', fontsize=12)
    ax_anim.set_title("Visual: Spring Compression and Extension", fontsize=14)
    ax_anim.grid(True, alpha=0.3)
    ax_anim.set_aspect('equal')
    
    # Wall (fixed point)
    wall = Rectangle((equilibrium_x - 0.1, 0), 0.1, 1.0, 
                    facecolor='gray', edgecolor='black', linewidth=2)
    ax_anim.add_patch(wall)
    
    # Spring (will be drawn as lines)
    spring_lines = []
    
    # Mass
    mass_size = 0.4
    mass = Circle((equilibrium_x + x[0], mass_size/2), mass_size/2,
                 facecolor='lightblue', edgecolor='black', linewidth=2)
    ax_anim.add_patch(mass)
    
    def draw_spring(ax, x_start, x_end, y, num_coils=5):
        """Draw a spring between two points"""
        for line in spring_lines:
            line.remove()
        spring_lines.clear()
        
        if x_end < x_start:
            x_start, x_end = x_end, x_start
        
        length = x_end - x_start
        coil_width = length / num_coils
        spring_x = [x_start]
        spring_y = [y]
        
        for i in range(num_coils):
            spring_x.append(x_start + (i + 0.5) * coil_width)
            spring_y.append(y + 0.2 if i % 2 == 0 else y - 0.2)
            spring_x.append(x_start + (i + 1) * coil_width)
            spring_y.append(y)
        
        line, = ax.plot(spring_x, spring_y, 'brown', linewidth=3)
        spring_lines.append(line)
        return spring_lines
    
    draw_spring(ax_anim, equilibrium_x, equilibrium_x + x[0], mass_size/2)
    
    time_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes,
                            fontsize=12, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def animate(frame):
        idx = frame * (len(t) // 200)
        if idx < len(t):
            mass_x = equilibrium_x + x[idx]
            mass.center = (mass_x, mass_size/2)
            draw_spring(ax_anim, equilibrium_x, mass_x, mass_size/2)
            
            # Color based on compression/extension
            if x[idx] > 0:
                mass.set_facecolor('red')  # Extended
            elif x[idx] < 0:
                mass.set_facecolor('blue')  # Compressed
            else:
                mass.set_facecolor('lightgreen')  # Equilibrium
            
            time_text.set_text(f'Time: {t[idx]:.2f} s\nDisplacement: {x[idx]:.3f} m\n'
                             f'Velocity: {v[idx]:.2f} m/s\n'
                             f'{"Extended" if x[idx] > 0 else "Compressed" if x[idx] < 0 else "Equilibrium"}')
        return spring_lines + [mass, time_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=50, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()

def example_3_pendulum_swing():
    """
    Example 3: Pendulum Swing
    Using Lagrangian: θ̈ = -(g/L) sin(θ)
    """
    print("\nExample 3: Pendulum Swing")
    
    g = 9.81  # Gravity
    L = 1.0   # Pendulum length
    initial_angle = np.pi / 4  # 45 degrees
    
    # Solve pendulum equation: θ̈ = -(g/L) sin(θ)
    t = np.linspace(0, 10, 1000)
    
    def pendulum_derivatives(state, t_val):
        theta, theta_dot = state
        theta_ddot = -(g / L) * np.sin(theta)
        return [theta_dot, theta_ddot]
    
    initial_state = [initial_angle, 0.0]  # [angle, angular velocity]
    solution = odeint(pendulum_derivatives, initial_state, t)
    theta = solution[:, 0]
    theta_dot = solution[:, 1]
    
    # Convert to position
    x = L * np.sin(theta)  # Horizontal displacement
    y = -L * np.cos(theta)  # Vertical displacement (negative because y increases upward)
    v = L * theta_dot  # Tangential velocity
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].plot(t, theta * 180/np.pi, 'b-', linewidth=2)  # Convert to degrees
    axes[0, 0].set_xlabel('Time (s)', fontsize=12)
    axes[0, 0].set_ylabel('Angle (degrees)', fontsize=12)
    axes[0, 0].set_title('Pendulum Angle vs Time', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    axes[0, 1].plot(t, v, 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Angular Velocity (m/s)', fontsize=12)
    axes[0, 1].set_title('Velocity vs Time', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Energy (kinetic + potential)
    mass = 1.0
    kinetic_energy = 0.5 * mass * (L * theta_dot)**2
    potential_energy = mass * g * L * (1 - np.cos(theta))
    total_energy = kinetic_energy + potential_energy
    
    axes[1, 0].plot(t, kinetic_energy, 'g-', linewidth=2, label='Kinetic Energy', alpha=0.7)
    axes[1, 0].plot(t, potential_energy, 'orange', linewidth=2, label='Potential Energy', alpha=0.7)
    axes[1, 0].plot(t, total_energy, 'purple', linewidth=2, label='Total Energy', alpha=0.7)
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Energy (J)', fontsize=12)
    axes[1, 0].set_title('Energy (Conserved)', fontsize=14)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Phase space
    axes[1, 1].plot(theta * 180/np.pi, v, 'purple', linewidth=2)
    axes[1, 1].set_xlabel('Angle (degrees)', fontsize=12)
    axes[1, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[1, 1].set_title('Phase Space', fontsize=14)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle("Newton's Second Law: Pendulum Swing", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('newtons_law_example3_pendulum.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Visual demonstration: Pendulum swing
    fig_anim, ax_anim = plt.subplots(figsize=(10, 10))
    pivot_x, pivot_y = 0, 2.0
    ax_anim.set_xlim(-2.5, 2.5)
    ax_anim.set_ylim(-0.5, 2.5)
    ax_anim.set_xlabel('x (m)', fontsize=12)
    ax_anim.set_ylabel('y (m)', fontsize=12)
    ax_anim.set_title("Visual: Pendulum Swing", fontsize=14)
    ax_anim.set_aspect('equal')
    ax_anim.grid(True, alpha=0.3)
    
    # Pivot point
    pivot = Circle((pivot_x, pivot_y), 0.05, facecolor='black', edgecolor='black')
    ax_anim.add_patch(pivot)
    
    # Pendulum rod
    rod_line, = ax_anim.plot([], [], 'brown', linewidth=3, label='Rod')
    
    # Pendulum bob
    bob = Circle((0, 0), 0.1, facecolor='blue', edgecolor='black', linewidth=2)
    ax_anim.add_patch(bob)
    
    # Trajectory trail
    trail_x, trail_y = [], []
    trail_line, = ax_anim.plot([], [], 'gray', linewidth=1, alpha=0.5, label='Trajectory')
    
    info_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes,
                            fontsize=11, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def animate(frame):
        idx = frame * (len(t) // 200)
        if idx < len(t):
            # Calculate pendulum position
            angle = theta[idx]
            bob_x = pivot_x + L * np.sin(angle)
            bob_y = pivot_y - L * np.cos(angle)
            
            # Update rod
            rod_line.set_data([pivot_x, bob_x], [pivot_y, bob_y])
            
            # Update bob
            bob.center = (bob_x, bob_y)
            
            # Update trail
            trail_x.append(bob_x)
            trail_y.append(bob_y)
            if len(trail_x) > 100:
                trail_x.pop(0)
                trail_y.pop(0)
            trail_line.set_data(trail_x, trail_y)
            
            info_text.set_text(f'Time: {t[idx]:.2f} s\n'
                             f'Angle: {theta[idx]*180/np.pi:.1f}°\n'
                             f'Velocity: {v[idx]:.2f} m/s\n'
                             f'Energy: {total_energy[idx]:.2f} J')
        return [rod_line, bob, trail_line, info_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=50, blit=False, repeat=True)
    ax_anim.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

def solve_1d_projectile(v0, g=9.81, k=0.1, t_span=(0, 10), n_points=1000):
    """
    Solve 1D projectile motion (vertical) with air resistance.
    
    Parameters:
    -----------
    v0 : float
        Initial velocity (m/s) - positive upward
    g : float
        Gravity (m/s²)
    k : float
        Air resistance coefficient
    t_span : tuple
        Time span
    n_points : int
        Number of points
    
    Returns:
    --------
    t, y, v : arrays
        Time, y position, y velocity
    """
    t = np.linspace(t_span[0], t_span[1], n_points)
    dt = t[1] - t[0]
    
    # Initialize arrays
    y = np.zeros(n_points)
    v = np.zeros(n_points)
    
    y[0] = 0.0
    v[0] = v0
    
    # Numerical integration
    for i in range(n_points - 1):
        # Check for invalid values (NaN or Inf)
        if np.isnan(v[i]) or np.isinf(v[i]):
            break
        
        # Air resistance force (opposes motion)
        if abs(v[i]) > 1e-6:
            F_drag = -k * abs(v[i]) * np.sign(v[i])
        else:
            F_drag = 0
        
        # Total force: gravity + air resistance
        F = -g + F_drag
        
        # Update velocity
        v_new = v[i] + F * dt
        
        # Limit velocity to prevent overflow
        max_vel = 1e4
        v_new = np.clip(v_new, -max_vel, max_vel)
        
        v[i+1] = v_new
        
        # Update position
        y[i+1] = y[i] + v[i] * dt
        
        # Check for invalid positions
        if np.isnan(y[i+1]) or np.isinf(y[i+1]):
            break
        
        # Stop if hits ground
        if y[i+1] < 0:
            y[i+1] = 0
            break
    
    # Trim arrays - find last valid index
    valid_indices = np.where((y >= 0) & np.isfinite(y))[0]
    if len(valid_indices) > 0:
        last_idx = valid_indices[-1] + 1
        last_idx = min(last_idx, len(t))
    else:
        last_idx = 1
    
    return t[:last_idx], y[:last_idx], v[:last_idx]

def example_4_projectile_with_air_resistance():
    """
    Example 4: 1D Projectile Motion (Vertical) with Air Resistance
    Shows actual trajectory vs theoretical (no air resistance)
    """
    print("\nExample 4: 1D Projectile with Air Resistance")
    
    v0 = 30.0  # Initial velocity (upward)
    g = 9.81
    k = 0.1  # Air resistance coefficient
    
    # Case 1: With air resistance
    t1, y1, v1 = solve_1d_projectile(
        v0=v0, k=k, t_span=(0, 6), n_points=1000
    )
    
    # Case 2: No air resistance (for comparison)
    t2, y2, v2 = solve_1d_projectile(
        v0=v0, k=0.0, t_span=(0, 6), n_points=1000
    )
    
    # Theoretical trajectory (no air resistance)
    t_theory = np.linspace(0, 2*v0/g, 1000)
    y_theory = v0 * t_theory - 0.5 * g * t_theory**2
    y_theory = y_theory[y_theory >= 0]
    t_theory = t_theory[:len(y_theory)]
    
    # Plot trajectories comparison
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Height vs time comparison
    axes[0, 0].plot(t_theory, y_theory, 'k--', linewidth=2, label='Theoretical (No Air)', alpha=0.7)
    axes[0, 0].plot(t1, y1, 'b-', linewidth=2, label='With Air Resistance', alpha=0.8)
    axes[0, 0].plot(t2, y2, 'g-', linewidth=2, label='No Air Resistance', alpha=0.8)
    axes[0, 0].set_xlabel('Time (s)', fontsize=12)
    axes[0, 0].set_ylabel('Height (m)', fontsize=12)
    axes[0, 0].set_title('Height vs Time Comparison', fontsize=14)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='brown', linewidth=2, alpha=0.5)
    
    # Plot 2: Velocity vs time
    axes[0, 1].plot(t1, v1, 'b-', linewidth=2, label='With Air Resistance', alpha=0.8)
    axes[0, 1].plot(t2, v2, 'g-', linewidth=2, label='No Air Resistance', alpha=0.8)
    axes[0, 1].axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[0, 1].set_title('Velocity vs Time', fontsize=14)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Maximum height comparison
    max_heights = [np.nanmax(y1) if len(y1) > 0 else 0, 
                   np.nanmax(y2) if len(y2) > 0 else 0, 
                   np.nanmax(y_theory) if len(y_theory) > 0 else 0]
    # Replace NaN with 0
    max_heights = [h if not (np.isnan(h) or np.isinf(h)) else 0 for h in max_heights]
    labels = ['With Air Resistance', 'No Air Resistance', 'Theoretical']
    colors_bar = ['blue', 'green', 'gray']
    bars = axes[1, 0].bar(labels, max_heights, color=colors_bar, alpha=0.7, edgecolor='black')
    axes[1, 0].set_ylabel('Max Height (m)', fontsize=12)
    axes[1, 0].set_title('Maximum Height Comparison', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    for bar, h in zip(bars, max_heights):
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                       f'{h:.1f}m', ha='center', va='bottom', fontsize=10)
    
    # Plot 4: Time to reach max height
    time_to_max = []
    for y_arr, t_arr in [(y1, t1), (y2, t2), (y_theory, t_theory)]:
        if len(y_arr) > 0:
            max_idx = np.nanargmax(y_arr)
            time_to_max.append(t_arr[max_idx] if max_idx < len(t_arr) else 0)
        else:
            time_to_max.append(0)
    # Replace NaN with 0
    time_to_max = [t if not (np.isnan(t) or np.isinf(t)) else 0 for t in time_to_max]
    bars = axes[1, 1].bar(labels, time_to_max, color=colors_bar, alpha=0.7, edgecolor='black')
    axes[1, 1].set_ylabel('Time to Max Height (s)', fontsize=12)
    axes[1, 1].set_title('Time to Reach Maximum Height', fontsize=14)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    for bar, t in zip(bars, time_to_max):
        height = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{t:.2f}s', ha='center', va='bottom', fontsize=10)
    
    plt.suptitle("Newton's Second Law: 1D Projectile with Air Resistance", 
                 fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('newtons_law_example4_projectile.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Visual demonstration: 1D Projectile with air resistance
    fig_anim, ax_anim = plt.subplots(figsize=(14, 8))
    # Use nanmax to handle NaN values safely
    max_y = max(np.nanmax(y1), np.nanmax(y2), np.nanmax(y_theory))
    max_t = max(np.nanmax(t1), np.nanmax(t2), np.nanmax(t_theory))
    # Ensure valid limits (fallback if all are NaN)
    if np.isnan(max_y) or np.isinf(max_y):
        max_y = 50
    if np.isnan(max_t) or np.isinf(max_t):
        max_t = 6
    
    ax_anim.set_xlim(-0.5, max_t + 0.5)
    ax_anim.set_ylim(-1, max_y + 2)
    ax_anim.set_xlabel('Time (s)', fontsize=12)
    ax_anim.set_ylabel('Height (m)', fontsize=12)
    ax_anim.set_title("Visual: 1D Projectile with Air Resistance", fontsize=14)
    ax_anim.grid(True, alpha=0.3)
    
    # Ground
    ax_anim.axhline(y=0, color='brown', linewidth=3, label='Ground')
    
    # Theoretical trajectory (dotted)
    theory_line, = ax_anim.plot(t_theory, y_theory, 'k--', linewidth=2, 
                               alpha=0.5, label='Theoretical Path (No Air)', zorder=1)
    
    # Actual trajectory with air resistance (will be drawn as trail)
    actual_trail, = ax_anim.plot([], [], 'b-', linewidth=2, 
                                alpha=0.7, label='Actual Path (With Air)', zorder=2)
    
    # Projectile (shown as a circle at current position)
    projectile = Circle((t1[0], y1[0]), 0.1, facecolor='red', 
                       edgecolor='black', linewidth=2, zorder=3)
    ax_anim.add_patch(projectile)
    
    # Velocity vector (vertical arrow)
    vel_arrow = FancyArrowPatch((t1[0], y1[0]), 
                               (t1[0], y1[0] + v1[0]*0.1),
                               arrowstyle='->', mutation_scale=20,
                               color='blue', linewidth=2, label='Velocity', zorder=4)
    ax_anim.add_patch(vel_arrow)
    
    info_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes,
                            fontsize=11, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    trail_t_actual, trail_y_actual = [], []
    
    def animate(frame):
        idx = frame * (len(t1) // 200) if len(t1) > 0 else 0
        if idx < len(t1) and not (np.isnan(t1[idx]) or np.isnan(y1[idx])):
            # Update projectile position
            projectile.center = (t1[idx], y1[idx])
            
            # Update velocity vector
            if idx < len(v1) and not np.isnan(v1[idx]):
                vel_arrow.set_positions((t1[idx], y1[idx]),
                                       (t1[idx], y1[idx] + v1[idx]*0.1))
            
            # Update trail
            trail_t_actual.append(t1[idx])
            trail_y_actual.append(y1[idx])
            if len(trail_t_actual) > 100:
                trail_t_actual.pop(0)
                trail_y_actual.pop(0)
            actual_trail.set_data(trail_t_actual, trail_y_actual)
            
            # Color based on height
            if y1[idx] > max_y * 0.7:
                projectile.set_facecolor('red')  # High
            elif y1[idx] > max_y * 0.3:
                projectile.set_facecolor('orange')  # Medium
            else:
                projectile.set_facecolor('yellow')  # Low
            
            v_mag = abs(v1[idx]) if idx < len(v1) and not np.isnan(v1[idx]) else 0
            direction = "Up" if v1[idx] > 0 else "Down" if idx < len(v1) else ""
            info_text.set_text(f'Time: {t1[idx]:.2f} s\n'
                             f'Height: {y1[idx]:.1f} m\n'
                             f'Velocity: {v_mag:.1f} m/s ({direction})\n'
                             f'Air Resistance: ON (k={k})')
        return [projectile, vel_arrow, actual_trail, info_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=50, blit=False, repeat=True)
    ax_anim.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Newton's Second Law Demonstrations")
    print("=" * 50)
    
    example_1_constant_force()
    example_2_spring_force()
    example_3_pendulum_swing()
    example_4_projectile_with_air_resistance()

