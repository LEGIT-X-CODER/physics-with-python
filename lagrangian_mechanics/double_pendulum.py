"""
Double Pendulum Simulation
==========================
Simulation of a double pendulum using Lagrangian mechanics.

The double pendulum is a classic example of a chaotic system.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

class DoublePendulum:
    """
    Double Pendulum system using Lagrangian mechanics.
    
    Generalized coordinates: θ1, θ2 (angles of both pendulums)
    """
    def __init__(self, m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81):
        """
        Initialize double pendulum.
        
        Parameters:
        -----------
        m1, m2 : float
            Masses of the two pendulums
        L1, L2 : float
            Lengths of the two pendulums
        g : float
            Gravitational acceleration
        """
        self.m1 = m1
        self.m2 = m2
        self.L1 = L1
        self.L2 = L2
        self.g = g
    
    def lagrangian(self, theta1, theta2, theta1_dot, theta2_dot):
        """
        Compute the Lagrangian L = T - V for double pendulum.
        
        Kinetic Energy:
        T = (1/2)m1(L1θ̇1)² + (1/2)m2[(L1θ̇1)² + (L2θ̇2)² + 2L1L2θ̇1θ̇2cos(θ1-θ2)]
        
        Potential Energy:
        V = -m1gL1cos(θ1) - m2g[L1cos(θ1) + L2cos(θ2)]
        """
        # Kinetic energy
        T = (0.5 * self.m1 * self.L1**2 * theta1_dot**2 +
             0.5 * self.m2 * (self.L1**2 * theta1_dot**2 +
                             self.L2**2 * theta2_dot**2 +
                             2 * self.L1 * self.L2 * theta1_dot * theta2_dot *
                             np.cos(theta1 - theta2)))
        
        # Potential energy
        V = (-self.m1 * self.g * self.L1 * np.cos(theta1) -
             self.m2 * self.g * (self.L1 * np.cos(theta1) + self.L2 * np.cos(theta2)))
        
        return T - V
    
    def equations_of_motion(self, state, t):
        """
        Compute derivatives for ODE solver.
        
        From Euler-Lagrange equations, we get:
        θ̈1 = f1(θ1, θ2, θ̇1, θ̇2)
        θ̈2 = f2(θ1, θ2, θ̇1, θ̇2)
        
        Parameters:
        -----------
        state : array
            [θ1, θ2, θ̇1, θ̇2]
        t : float
            Time
        
        Returns:
        --------
        derivatives : array
            [θ̇1, θ̇2, θ̈1, θ̈2]
        """
        theta1, theta2, theta1_dot, theta2_dot = state
        
        # Intermediate calculations
        delta = theta2 - theta1
        sin_delta = np.sin(delta)
        cos_delta = np.cos(delta)
        
        # Denominators for the equations
        denom = (2 * self.m1 + self.m2 - self.m2 * np.cos(2 * delta))
        
        # Angular accelerations (derived from Euler-Lagrange equations)
        theta1_ddot = (-self.g * (2 * self.m1 + self.m2) * np.sin(theta1) -
                       self.m2 * self.g * np.sin(theta1 - 2 * theta2) -
                       2 * np.sin(delta) * self.m2 *
                       (theta2_dot**2 * self.L2 + theta1_dot**2 * self.L1 * cos_delta)) / \
                      (self.L1 * denom)
        
        theta2_ddot = (2 * np.sin(delta) *
                      (theta1_dot**2 * self.L1 * (self.m1 + self.m2) +
                       self.g * (self.m1 + self.m2) * np.cos(theta1) +
                       theta2_dot**2 * self.L2 * self.m2 * cos_delta)) / \
                     (self.L2 * denom)
        
        return np.array([theta1_dot, theta2_dot, theta1_ddot, theta2_dot])
    
    def solve(self, theta1_0, theta2_0, theta1_dot0=0.0, theta2_dot0=0.0,
              t_span=(0, 20), n_points=2000):
        """
        Solve the double pendulum motion.
        
        Parameters:
        -----------
        theta1_0, theta2_0 : float
            Initial angles (radians)
        theta1_dot0, theta2_dot0 : float
            Initial angular velocities (rad/s)
        t_span : tuple
            (t_start, t_end)
        n_points : int
            Number of time points
        
        Returns:
        --------
        t : array
            Time points
        theta1, theta2 : arrays
            Angles at each time
        theta1_dot, theta2_dot : arrays
            Angular velocities at each time
        """
        t = np.linspace(t_span[0], t_span[1], n_points)
        initial_state = np.array([theta1_0, theta2_0, theta1_dot0, theta2_dot0])
        
        solution = odeint(self.equations_of_motion, initial_state, t)
        
        theta1 = solution[:, 0]
        theta2 = solution[:, 1]
        theta1_dot = solution[:, 2]
        theta2_dot = solution[:, 3]
        
        return t, theta1, theta2, theta1_dot, theta2_dot
    
    def get_positions(self, theta1, theta2):
        """
        Calculate Cartesian positions of both pendulums.
        
        Returns:
        --------
        x1, y1 : arrays
            Position of first pendulum
        x2, y2 : arrays
            Position of second pendulum (end of double pendulum)
        """
        x1 = self.L1 * np.sin(theta1)
        y1 = -self.L1 * np.cos(theta1)
        
        x2 = x1 + self.L2 * np.sin(theta2)
        y2 = y1 - self.L2 * np.cos(theta2)
        
        return x1, y1, x2, y2

def plot_double_pendulum(t, theta1, theta2, x1, y1, x2, y2, save_animation=False):
    """
    Plot double pendulum motion.
    """
    fig = plt.figure(figsize=(16, 10))
    
    # Plot 1: Angles vs time
    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(t, theta1, 'b-', linewidth=1.5, label='θ₁', alpha=0.7)
    ax1.plot(t, theta2, 'r-', linewidth=1.5, label='θ₂', alpha=0.7)
    ax1.set_xlabel('Time (s)', fontsize=11)
    ax1.set_ylabel('Angle (rad)', fontsize=11)
    ax1.set_title('Angles vs Time', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Trajectory of end point
    ax2 = plt.subplot(2, 3, 2)
    ax2.plot(x2, y2, 'g-', linewidth=0.5, alpha=0.6)
    ax2.set_xlabel('x (m)', fontsize=11)
    ax2.set_ylabel('y (m)', fontsize=11)
    ax2.set_title('Trajectory of End Point', fontsize=12)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Phase space for θ1
    ax3 = plt.subplot(2, 3, 3)
    ax3.plot(theta1, np.gradient(theta1, t), 'b-', linewidth=0.5, alpha=0.6)
    ax3.set_xlabel('θ₁ (rad)', fontsize=11)
    ax3.set_ylabel('θ̇₁ (rad/s)', fontsize=11)
    ax3.set_title('Phase Space: θ₁', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Phase space for θ2
    ax4 = plt.subplot(2, 3, 4)
    ax4.plot(theta2, np.gradient(theta2, t), 'r-', linewidth=0.5, alpha=0.6)
    ax4.set_xlabel('θ₂ (rad)', fontsize=11)
    ax4.set_ylabel('θ̇₂ (rad/s)', fontsize=11)
    ax4.set_title('Phase Space: θ₂', fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: 3D phase space (θ1, θ2, θ̇1)
    ax5 = plt.subplot(2, 3, 5, projection='3d')
    ax5.plot(theta1, theta2, np.gradient(theta1, t), 'b-', linewidth=0.5, alpha=0.6)
    ax5.set_xlabel('θ₁ (rad)', fontsize=10)
    ax5.set_ylabel('θ₂ (rad)', fontsize=10)
    ax5.set_zlabel('θ̇₁ (rad/s)', fontsize=10)
    ax5.set_title('3D Phase Space', fontsize=12)
    
    # Plot 6: Energy over time
    ax6 = plt.subplot(2, 3, 6)
    # Calculate energy (simplified - would need full calculation)
    # For visualization, use kinetic energy approximation
    theta1_dot = np.gradient(theta1, t)
    theta2_dot = np.gradient(theta2, t)
    L1, L2 = 1.0, 1.0  # Assuming unit lengths
    m1, m2 = 1.0, 1.0  # Assuming unit masses
    g = 9.81
    
    # Kinetic energy
    T = (0.5 * m1 * L1**2 * theta1_dot**2 +
         0.5 * m2 * (L1**2 * theta1_dot**2 + L2**2 * theta2_dot**2 +
                     2 * L1 * L2 * theta1_dot * theta2_dot * np.cos(theta1 - theta2)))
    
    # Potential energy
    V = (-m1 * g * L1 * np.cos(theta1) -
         m2 * g * (L1 * np.cos(theta1) + L2 * np.cos(theta2)))
    
    E = T + V
    ax6.plot(t, E, 'purple', linewidth=1.5)
    ax6.set_xlabel('Time (s)', fontsize=11)
    ax6.set_ylabel('Total Energy (J)', fontsize=11)
    ax6.set_title('Total Energy vs Time', fontsize=12)
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('double_pendulum_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Create animation
    fig_anim, ax_anim = plt.subplots(figsize=(10, 10))
    
    # Calculate limits
    max_range = max(np.abs(x2).max(), np.abs(y2).max()) * 1.2
    ax_anim.set_xlim(-max_range, max_range)
    ax_anim.set_ylim(-max_range, max_range)
    ax_anim.set_aspect('equal')
    ax_anim.set_xlabel('x (m)', fontsize=12)
    ax_anim.set_ylabel('y (m)', fontsize=12)
    ax_anim.set_title('Double Pendulum Animation', fontsize=14)
    ax_anim.grid(True, alpha=0.3)
    
    # Initialize lines
    line, = ax_anim.plot([], [], 'o-', lw=3, markersize=10, color='blue')
    trail, = ax_anim.plot([], [], '-', lw=1, alpha=0.3, color='green')
    
    # Store trail
    trail_x, trail_y = [], []
    
    def animate(frame):
        # Update pendulum positions
        line_x = [0, x1[frame], x2[frame]]
        line_y = [0, y1[frame], y2[frame]]
        line.set_data(line_x, line_y)
        
        # Update trail
        trail_x.append(x2[frame])
        trail_y.append(y2[frame])
        if len(trail_x) > 200:  # Limit trail length
            trail_x.pop(0)
            trail_y.pop(0)
        trail.set_data(trail_x, trail_y)
        
        return line, trail
    
    anim = FuncAnimation(fig_anim, animate, frames=len(t),
                        interval=20, blit=True, repeat=True)
    
    if save_animation:
        anim.save('double_pendulum_animation.gif', writer='pillow', fps=50)
    
    plt.show()
    return anim

if __name__ == "__main__":
    # Example 1: Small initial angles (near linear regime)
    print("Double Pendulum Simulation...")
    print("Example 1: Small initial angles")
    
    pendulum1 = DoublePendulum(m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81)
    t1, theta1_1, theta2_1, _, _ = pendulum1.solve(
        theta1_0=np.pi/6,   # 30 degrees
        theta2_0=np.pi/6,   # 30 degrees
        t_span=(0, 10),
        n_points=1000
    )
    x1_1, y1_1, x2_1, y2_1 = pendulum1.get_positions(theta1_1, theta2_1)
    plot_double_pendulum(t1, theta1_1, theta2_1, x1_1, y1_1, x2_1, y2_1)
    
    # Example 2: Large initial angles (chaotic regime)
    print("\nExample 2: Large initial angles (chaotic behavior)")
    
    pendulum2 = DoublePendulum(m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81)
    t2, theta1_2, theta2_2, _, _ = pendulum2.solve(
        theta1_0=np.pi/2,   # 90 degrees
        theta2_0=np.pi/2,   # 90 degrees
        t_span=(0, 20),
        n_points=2000
    )
    x1_2, y1_2, x2_2, y2_2 = pendulum2.get_positions(theta1_2, theta2_2)
    plot_double_pendulum(t2, theta1_2, theta2_2, x1_2, y1_2, x2_2, y2_2)
    
    # Example 3: Slightly different initial conditions (demonstrate sensitivity)
    print("\nExample 3: Sensitivity to initial conditions")
    
    pendulum3a = DoublePendulum(m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81)
    t3, theta1_3a, theta2_3a, _, _ = pendulum3a.solve(
        theta1_0=np.pi/2,
        theta2_0=np.pi/2,
        t_span=(0, 20),
        n_points=2000
    )
    
    pendulum3b = DoublePendulum(m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81)
    t3, theta1_3b, theta2_3b, _, _ = pendulum3b.solve(
        theta1_0=np.pi/2 + 0.001,  # Tiny difference
        theta2_0=np.pi/2,
        t_span=(0, 20),
        n_points=2000
    )
    
    # Plot comparison
    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t3, theta1_3a, 'b-', linewidth=1.5, alpha=0.7, label='θ₁ (original)')
    plt.plot(t3, theta1_3b, 'r--', linewidth=1.5, alpha=0.7, label='θ₁ (perturbed)')
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Angle (rad)', fontsize=12)
    plt.title('Sensitivity to Initial Conditions', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(t3, np.abs(theta1_3a - theta1_3b), 'g-', linewidth=1.5)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('|θ₁ difference| (rad)', fontsize=12)
    plt.title('Divergence of Trajectories', fontsize=14)
    plt.yscale('log')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('double_pendulum_chaos.png', dpi=150, bbox_inches='tight')
    plt.show()

