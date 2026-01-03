"""
Lorenz Attractor Simulation
============================
Simulation of the Lorenz attractor, a classic example of chaos theory.

The Lorenz system is described by:
    dx/dt = σ(y - x)
    dy/dt = x(ρ - z) - y
    dz/dt = xy - βz

where σ (sigma) is the Prandtl number,
      ρ (rho) is the Rayleigh number,
      β (beta) is a geometric factor.

For chaos, typical values are: σ=10, ρ=28, β=8/3
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

class LorenzSystem:
    """
    Lorenz attractor system.
    """
    def __init__(self, sigma=10.0, rho=28.0, beta=8.0/3.0):
        """
        Initialize Lorenz system.
        
        Parameters:
        -----------
        sigma : float
            Prandtl number (typically 10)
        rho : float
            Rayleigh number (typically 28 for chaos)
        beta : float
            Geometric factor (typically 8/3)
        """
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
    
    def equations(self, state, t):
        """
        Lorenz system of differential equations.
        
        Parameters:
        -----------
        state : array
            [x, y, z]
        t : float
            Time
        
        Returns:
        --------
        derivatives : array
            [dx/dt, dy/dt, dz/dt]
        """
        x, y, z = state
        
        dx_dt = self.sigma * (y - x)
        dy_dt = x * (self.rho - z) - y
        dz_dt = x * y - self.beta * z
        
        return np.array([dx_dt, dy_dt, dz_dt])
    
    def solve(self, x0, y0, z0, t_span=(0, 50), n_points=10000):
        """
        Solve the Lorenz system.
        
        Parameters:
        -----------
        x0, y0, z0 : float
            Initial conditions
        t_span : tuple
            (t_start, t_end)
        n_points : int
            Number of time points
        
        Returns:
        --------
        t : array
            Time points
        x, y, z : arrays
            State variables at each time
        """
        t = np.linspace(t_span[0], t_span[1], n_points)
        initial_state = np.array([x0, y0, z0])
        
        solution = odeint(self.equations, initial_state, t)
        
        x = solution[:, 0]
        y = solution[:, 1]
        z = solution[:, 2]
        
        return t, x, y, z
    
    def lyapunov_exponent_estimate(self, x, y, z, t):
        """
        Estimate the largest Lyapunov exponent (measure of chaos).
        This is a simplified estimation.
        """
        # Calculate distance between nearby trajectories
        # For a more accurate calculation, need to integrate the tangent space
        # This is a simplified version
        distances = np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)
        dt = t[1] - t[0]
        
        # Avoid division by zero
        distances = distances[distances > 1e-10]
        if len(distances) > 0:
            # Rough estimate
            lyap = np.mean(np.log(distances)) / dt
            return lyap
        return 0.0

def plot_lorenz_attractor(t, x, y, z, sigma, rho, beta):
    """
    Plot the Lorenz attractor in various ways.
    """
    fig = plt.figure(figsize=(18, 12))
    
    # Plot 1: 3D trajectory
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    ax1.plot(x, y, z, 'b-', linewidth=0.5, alpha=0.6)
    ax1.set_xlabel('x', fontsize=11)
    ax1.set_ylabel('y', fontsize=11)
    ax1.set_zlabel('z', fontsize=11)
    ax1.set_title('3D Lorenz Attractor', fontsize=12)
    
    # Plot 2: x vs time
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.plot(t, x, 'r-', linewidth=0.8, alpha=0.7)
    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('x', fontsize=11)
    ax2.set_title('x vs Time', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: y vs time
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.plot(t, y, 'g-', linewidth=0.8, alpha=0.7)
    ax3.set_xlabel('Time', fontsize=11)
    ax3.set_ylabel('y', fontsize=11)
    ax3.set_title('y vs Time', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: z vs time
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.plot(t, z, 'b-', linewidth=0.8, alpha=0.7)
    ax4.set_xlabel('Time', fontsize=11)
    ax4.set_ylabel('z', fontsize=11)
    ax4.set_title('z vs Time', fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: x-y projection
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.plot(x, y, 'purple', linewidth=0.5, alpha=0.6)
    ax5.set_xlabel('x', fontsize=11)
    ax5.set_ylabel('y', fontsize=11)
    ax5.set_title('x-y Projection (Butterfly Wings)', fontsize=12)
    ax5.set_aspect('equal')
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: x-z projection
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.plot(x, z, 'orange', linewidth=0.5, alpha=0.6)
    ax6.set_xlabel('x', fontsize=11)
    ax6.set_ylabel('z', fontsize=11)
    ax6.set_title('x-z Projection', fontsize=12)
    ax6.grid(True, alpha=0.3)
    
    plt.suptitle(f'Lorenz Attractor (σ={sigma}, ρ={rho}, β={beta:.2f})', 
                 fontsize=14, y=0.995)
    plt.tight_layout()
    plt.savefig('lorenz_attractor_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Create 3D animation
    fig_anim = plt.figure(figsize=(12, 10))
    ax_anim = fig_anim.add_subplot(111, projection='3d')
    
    # Set limits
    ax_anim.set_xlim(x.min(), x.max())
    ax_anim.set_ylim(y.min(), y.max())
    ax_anim.set_zlim(z.min(), z.max())
    ax_anim.set_xlabel('x', fontsize=12)
    ax_anim.set_ylabel('y', fontsize=12)
    ax_anim.set_zlabel('z', fontsize=12)
    ax_anim.set_title('Lorenz Attractor 3D Animation', fontsize=14)
    
    # Initialize line
    line, = ax_anim.plot([], [], [], 'b-', linewidth=1, alpha=0.6)
    point, = ax_anim.plot([], [], [], 'ro', markersize=8)
    
    # Store trajectory
    traj_x, traj_y, traj_z = [], [], []
    
    def animate(frame):
        # Add new point
        idx = frame * (len(t) // 1000)  # Sample points for animation
        if idx < len(t):
            traj_x.append(x[idx])
            traj_y.append(y[idx])
            traj_z.append(z[idx])
            
            # Limit trajectory length for performance
            if len(traj_x) > 500:
                traj_x.pop(0)
                traj_y.pop(0)
                traj_z.pop(0)
            
            line.set_data(traj_x, traj_y)
            line.set_3d_properties(traj_z)
            
            point.set_data([x[idx]], [y[idx]])
            point.set_3d_properties([z[idx]])
        
        return line, point
    
    anim = FuncAnimation(fig_anim, animate, frames=1000,
                        interval=50, blit=False, repeat=True)
    
    plt.show()
    return anim

def plot_parameter_sensitivity():
    """
    Demonstrate sensitivity to initial conditions (butterfly effect).
    """
    lorenz = LorenzSystem(sigma=10.0, rho=28.0, beta=8.0/3.0)
    
    # Two trajectories with slightly different initial conditions
    t1, x1, y1, z1 = lorenz.solve(1.0, 1.0, 1.0, t_span=(0, 30), n_points=5000)
    t2, x2, y2, z2 = lorenz.solve(1.001, 1.0, 1.0, t_span=(0, 30), n_points=5000)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: x comparison
    axes[0, 0].plot(t1, x1, 'b-', linewidth=1.5, alpha=0.7, label='x (original)')
    axes[0, 0].plot(t2, x2, 'r--', linewidth=1.5, alpha=0.7, label='x (perturbed)')
    axes[0, 0].set_xlabel('Time', fontsize=12)
    axes[0, 0].set_ylabel('x', fontsize=12)
    axes[0, 0].set_title('Sensitivity to Initial Conditions', fontsize=14)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Divergence
    axes[0, 1].plot(t1, np.abs(x1 - x2), 'g-', linewidth=1.5)
    axes[0, 1].set_xlabel('Time', fontsize=12)
    axes[0, 1].set_ylabel('|x₁ - x₂|', fontsize=12)
    axes[0, 1].set_title('Divergence of Trajectories', fontsize=14)
    axes[0, 1].set_yscale('log')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: 3D comparison
    ax3d = fig.add_subplot(2, 2, 3, projection='3d')
    ax3d.plot(x1, y1, z1, 'b-', linewidth=0.5, alpha=0.6, label='Original')
    ax3d.plot(x2, y2, z2, 'r--', linewidth=0.5, alpha=0.6, label='Perturbed')
    ax3d.set_xlabel('x', fontsize=11)
    ax3d.set_ylabel('y', fontsize=11)
    ax3d.set_zlabel('z', fontsize=11)
    ax3d.set_title('3D Trajectory Comparison', fontsize=12)
    ax3d.legend()
    
    # Plot 4: Phase space (x-y)
    axes[1, 1].plot(x1, y1, 'b-', linewidth=0.5, alpha=0.6, label='Original')
    axes[1, 1].plot(x2, y2, 'r--', linewidth=0.5, alpha=0.6, label='Perturbed')
    axes[1, 1].set_xlabel('x', fontsize=12)
    axes[1, 1].set_ylabel('y', fontsize=12)
    axes[1, 1].set_title('x-y Phase Space', fontsize=14)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('lorenz_sensitivity.png', dpi=150, bbox_inches='tight')
    plt.show()

def plot_parameter_variation():
    """
    Show how the attractor changes with different ρ (Rayleigh number) values.
    """
    rho_values = [14, 20, 28, 35]
    fig = plt.figure(figsize=(16, 12))
    
    for i, rho in enumerate(rho_values):
        lorenz = LorenzSystem(sigma=10.0, rho=rho, beta=8.0/3.0)
        t, x, y, z = lorenz.solve(1.0, 1.0, 1.0, t_span=(0, 30), n_points=5000)
        
        ax = fig.add_subplot(2, 2, i+1, projection='3d')
        ax.plot(x, y, z, linewidth=0.5, alpha=0.6)
        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('y', fontsize=10)
        ax.set_zlabel('z', fontsize=10)
        ax.set_title(f'ρ = {rho}', fontsize=12)
    
    plt.suptitle('Lorenz Attractor for Different ρ Values', fontsize=14, y=0.995)
    plt.tight_layout()
    plt.savefig('lorenz_parameter_variation.png', dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Example 1: Classic chaotic parameters
    print("Lorenz Attractor Simulation...")
    print("Example 1: Classic chaotic parameters (σ=10, ρ=28, β=8/3)")
    
    lorenz1 = LorenzSystem(sigma=10.0, rho=28.0, beta=8.0/3.0)
    t1, x1, y1, z1 = lorenz1.solve(
        x0=1.0, y0=1.0, z0=1.0,
        t_span=(0, 50),
        n_points=10000
    )
    plot_lorenz_attractor(t1, x1, y1, z1, 10.0, 28.0, 8.0/3.0)
    
    # Example 2: Sensitivity to initial conditions
    print("\nExample 2: Demonstrating sensitivity to initial conditions")
    plot_parameter_sensitivity()
    
    # Example 3: Parameter variation
    print("\nExample 3: Attractor shape for different ρ values")
    plot_parameter_variation()

