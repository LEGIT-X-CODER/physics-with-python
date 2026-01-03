"""
Basic Lagrangian Mechanics
==========================
Implementation of Lagrangian mechanics for solving equations of motion.

The Lagrangian is defined as: L = T - V
where T is kinetic energy and V is potential energy.

Euler-Lagrange equation: d/dt(∂L/∂q̇) - ∂L/∂q = 0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sympy as sp

class LagrangianSystem:
    """
    Base class for Lagrangian mechanical systems.
    """
    def __init__(self):
        self.q = None  # Generalized coordinates
        self.q_dot = None  # Generalized velocities
        self.t = None  # Time
        
    def lagrangian(self, q, q_dot, t):
        """
        Compute the Lagrangian L = T - V.
        
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement lagrangian method")
    
    def equations_of_motion(self, state, t):
        """
        Compute derivatives for ODE solver using Euler-Lagrange equations.
        
        Parameters:
        -----------
        state : array
            [q1, q2, ..., q1_dot, q2_dot, ...]
        t : float
            Time
        
        Returns:
        --------
        derivatives : array
            [q1_dot, q2_dot, ..., q1_ddot, q2_ddot, ...]
        """
        n = len(state) // 2
        q = state[:n]
        q_dot = state[n:]
        
        # For numerical computation, we use the fact that:
        # d/dt(∂L/∂q̇) - ∂L/∂q = 0
        # This gives us: q̈ = f(q, q̇, t)
        
        # Compute accelerations using numerical differentiation
        # For simple systems, we can derive analytically
        q_ddot = self.compute_accelerations(q, q_dot, t)
        
        return np.concatenate([q_dot, q_ddot])
    
    def compute_accelerations(self, q, q_dot, t):
        """
        Compute generalized accelerations from Euler-Lagrange equations.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement compute_accelerations method")

class SimplePendulum(LagrangianSystem):
    """
    Simple Pendulum using Lagrangian mechanics.
    
    Generalized coordinate: θ (angle from vertical)
    L = (1/2)ml²θ̇² - mgl(1 - cos(θ))
    """
    def __init__(self, length=1.0, mass=1.0, gravity=9.81):
        super().__init__()
        self.length = length
        self.mass = mass
        self.gravity = gravity
        
    def lagrangian(self, theta, theta_dot, t):
        """
        Lagrangian: L = T - V
        T = (1/2)ml²θ̇² (kinetic energy)
        V = mgl(1 - cos(θ)) (potential energy)
        """
        T = 0.5 * self.mass * self.length**2 * theta_dot**2
        V = self.mass * self.gravity * self.length * (1 - np.cos(theta))
        return T - V
    
    def compute_accelerations(self, q, q_dot, t):
        """
        From Euler-Lagrange: ml²θ̈ = -mgl sin(θ)
        Therefore: θ̈ = -(g/l) sin(θ)
        """
        theta = q[0]
        theta_ddot = -(self.gravity / self.length) * np.sin(theta)
        return np.array([theta_ddot])
    
    def solve(self, theta0, theta_dot0, t_span, n_points=1000):
        """
        Solve the pendulum motion.
        
        Parameters:
        -----------
        theta0 : float
            Initial angle (radians)
        theta_dot0 : float
            Initial angular velocity (rad/s)
        t_span : tuple
            (t_start, t_end)
        n_points : int
            Number of time points
        
        Returns:
        --------
        t : array
            Time points
        theta : array
            Angle at each time
        theta_dot : array
            Angular velocity at each time
        """
        t = np.linspace(t_span[0], t_span[1], n_points)
        initial_state = np.array([theta0, theta_dot0])
        
        solution = odeint(self.equations_of_motion, initial_state, t)
        theta = solution[:, 0]
        theta_dot = solution[:, 1]
        
        return t, theta, theta_dot

class MassSpringSystem(LagrangianSystem):
    """
    Mass-Spring System using Lagrangian mechanics.
    
    Generalized coordinate: x (displacement from equilibrium)
    L = (1/2)mẋ² - (1/2)kx²
    """
    def __init__(self, mass=1.0, spring_constant=1.0):
        super().__init__()
        self.mass = mass
        self.spring_constant = spring_constant
        
    def lagrangian(self, x, x_dot, t):
        """
        Lagrangian: L = T - V
        T = (1/2)mẋ² (kinetic energy)
        V = (1/2)kx² (potential energy)
        """
        T = 0.5 * self.mass * x_dot**2
        V = 0.5 * self.spring_constant * x**2
        return T - V
    
    def compute_accelerations(self, q, q_dot, t):
        """
        From Euler-Lagrange: mẍ = -kx
        Therefore: ẍ = -(k/m)x
        """
        x = q[0]
        x_ddot = -(self.spring_constant / self.mass) * x
        return np.array([x_ddot])
    
    def solve(self, x0, x_dot0, t_span, n_points=1000):
        """
        Solve the mass-spring motion.
        
        Parameters:
        -----------
        x0 : float
            Initial displacement
        x_dot0 : float
            Initial velocity
        t_span : tuple
            (t_start, t_end)
        n_points : int
            Number of time points
        
        Returns:
        --------
        t : array
            Time points
        x : array
            Displacement at each time
        x_dot : array
            Velocity at each time
        """
        t = np.linspace(t_span[0], t_span[1], n_points)
        initial_state = np.array([x0, x_dot0])
        
        solution = odeint(self.equations_of_motion, initial_state, t)
        x = solution[:, 0]
        x_dot = solution[:, 1]
        
        return t, x, x_dot

def plot_pendulum(t, theta, theta_dot, length=1.0):
    """
    Plot pendulum motion and phase space.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Angle vs time
    axes[0, 0].plot(t, theta, 'b-', linewidth=2)
    axes[0, 0].set_xlabel('Time (s)', fontsize=12)
    axes[0, 0].set_ylabel('Angle θ (rad)', fontsize=12)
    axes[0, 0].set_title('Pendulum Angle vs Time', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Angular velocity vs time
    axes[0, 1].plot(t, theta_dot, 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Angular Velocity θ̇ (rad/s)', fontsize=12)
    axes[0, 1].set_title('Angular Velocity vs Time', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Phase space (θ vs θ̇)
    axes[1, 0].plot(theta, theta_dot, 'g-', linewidth=1.5, alpha=0.7)
    axes[1, 0].set_xlabel('Angle θ (rad)', fontsize=12)
    axes[1, 0].set_ylabel('Angular Velocity θ̇ (rad/s)', fontsize=12)
    axes[1, 0].set_title('Phase Space Trajectory', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Pendulum animation (snapshot)
    # Show pendulum at different times
    time_indices = np.linspace(0, len(t)-1, 5, dtype=int)
    colors = plt.cm.viridis(np.linspace(0, 1, len(time_indices)))
    
    for i, idx in enumerate(time_indices):
        th = theta[idx]
        x_pend = length * np.sin(th)
        y_pend = -length * np.cos(th)
        
        axes[1, 1].plot([0, x_pend], [0, y_pend], 'o-', 
                        color=colors[i], linewidth=2, markersize=8,
                        label=f't = {t[idx]:.2f}s')
        axes[1, 1].plot(x_pend, y_pend, 'o', color=colors[i], markersize=12)
    
    axes[1, 1].plot(0, 0, 'ko', markersize=10)  # Pivot point
    axes[1, 1].set_xlim(-length*1.2, length*1.2)
    axes[1, 1].set_ylim(-length*1.2, length*0.2)
    axes[1, 1].set_xlabel('x (m)', fontsize=12)
    axes[1, 1].set_ylabel('y (m)', fontsize=12)
    axes[1, 1].set_title('Pendulum Positions', fontsize=14)
    axes[1, 1].set_aspect('equal')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('simple_pendulum_lagrangian.png', dpi=150, bbox_inches='tight')
    plt.show()

def plot_mass_spring(t, x, x_dot):
    """
    Plot mass-spring system motion and phase space.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot 1: Displacement vs time
    axes[0].plot(t, x, 'b-', linewidth=2)
    axes[0].set_xlabel('Time (s)', fontsize=12)
    axes[0].set_ylabel('Displacement x (m)', fontsize=12)
    axes[0].set_title('Mass-Spring: Displacement vs Time', fontsize=14)
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Velocity vs time
    axes[1].plot(t, x_dot, 'r-', linewidth=2)
    axes[1].set_xlabel('Time (s)', fontsize=12)
    axes[1].set_ylabel('Velocity ẋ (m/s)', fontsize=12)
    axes[1].set_title('Mass-Spring: Velocity vs Time', fontsize=14)
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Phase space (x vs ẋ)
    axes[2].plot(x, x_dot, 'g-', linewidth=1.5, alpha=0.7)
    axes[2].set_xlabel('Displacement x (m)', fontsize=12)
    axes[2].set_ylabel('Velocity ẋ (m/s)', fontsize=12)
    axes[2].set_title('Phase Space Trajectory', fontsize=14)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('mass_spring_lagrangian.png', dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Example 1: Simple Pendulum
    print("Solving Simple Pendulum using Lagrangian Mechanics...")
    pendulum = SimplePendulum(length=1.0, mass=1.0, gravity=9.81)
    
    # Initial conditions: 45 degrees, zero initial velocity
    t1, theta1, theta_dot1 = pendulum.solve(
        theta0=np.pi/4,  # 45 degrees
        theta_dot0=0.0,
        t_span=(0, 10),
        n_points=1000
    )
    plot_pendulum(t1, theta1, theta_dot1, length=1.0)
    
    # Example 2: Large amplitude pendulum (non-linear)
    print("\nLarge amplitude pendulum (non-linear regime)...")
    t2, theta2, theta_dot2 = pendulum.solve(
        theta0=np.pi * 0.9,  # Almost horizontal
        theta_dot0=0.0,
        t_span=(0, 10),
        n_points=1000
    )
    plot_pendulum(t2, theta2, theta_dot2, length=1.0)
    
    # Example 3: Mass-Spring System
    print("\nSolving Mass-Spring System using Lagrangian Mechanics...")
    spring = MassSpringSystem(mass=1.0, spring_constant=1.0)
    
    t3, x3, x_dot3 = spring.solve(
        x0=1.0,      # Initial displacement
        x_dot0=0.0,  # Zero initial velocity
        t_span=(0, 10),
        n_points=1000
    )
    plot_mass_spring(t3, x3, x_dot3)

