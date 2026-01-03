# Newton's Second Law Documentation

Complete guide for Newton's Second Law (F = ma) simulations with multiple force scenarios and visual demonstrations.

## Table of Contents

- [Overview](#overview)
- [Class: NewtonsSecondLaw](#class-newtonssecondlaw)
- [Examples](#examples)
- [Parameters Reference](#parameters-reference)
- [Visualization](#visualization)
- [Mathematical Background](#mathematical-background)

## Overview

This module demonstrates Newton's Second Law of Motion: **F = ma** (Force = mass × acceleration) through various practical examples with interactive visualizations.

### Mathematical Formulation

**Newton's Second Law:**
```
F = ma
```

where:
- `F` = Force (N)
- `m` = Mass (kg)
- `a` = Acceleration (m/s²)

From this, we derive:
```
a = F/m
dv/dt = F/m
dx/dt = v
```

These are solved using numerical integration (scipy's `odeint`).

## Class: NewtonsSecondLaw

### Initialization

```python
from newtons_law.newtons_second_law import NewtonsSecondLaw

system = NewtonsSecondLaw(mass=2.0)  # Object with mass 2 kg
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mass` | float | 1.0 | Mass of the object (kg) |

### Method: `solve_motion()`

Solves the equation of motion using F = ma.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `force_func` | callable | Required | Function F(t, x, v) returning force |
| `initial_position` | float | 0.0 | Initial position (m) |
| `initial_velocity` | float | 0.0 | Initial velocity (m/s) |
| `t_span` | tuple | (0, 10) | Time span (t_start, t_end) |
| `n_points` | int | 1000 | Number of time points |

#### Returns

- `t` (array): Time points
- `x` (array): Position at each time
- `v` (array): Velocity at each time
- `a` (array): Acceleration at each time

#### Example

```python
system = NewtonsSecondLaw(mass=2.0)

def constant_force(t, x, v):
    return 10.0  # 10N constant force

t, x, v, a = system.solve_motion(
    force_func=constant_force,
    initial_position=0.0,
    initial_velocity=0.0,
    t_span=(0, 5),
    n_points=500
)
```

## Examples

### Example 1: Constant Force

A constant force applied to a box, demonstrating linear acceleration.

#### Code

```python
from newtons_law.newtons_second_law import example_1_constant_force

example_1_constant_force()
```

#### What It Shows

- **Physics:** Constant force → constant acceleration
- **Visualization:** Box moving with force vector arrow
- **Plots:**
  - Position vs Time (quadratic curve)
  - Velocity vs Time (linear)
  - Acceleration vs Time (constant)
  - Phase Space (velocity vs position)

#### Parameters

- Mass: 2.0 kg
- Force: 10.0 N
- Initial position: 0.0 m
- Initial velocity: 0.0 m/s

#### Expected Results

- Acceleration: `a = F/m = 10/2 = 5 m/s²`
- Velocity: `v = at = 5t m/s`
- Position: `x = ½at² = 2.5t² m`

### Example 2: Spring Force (Hooke's Law)

A mass attached to a spring, demonstrating simple harmonic motion.

#### Code

```python
from newtons_law.newtons_second_law import example_2_spring_force

example_2_spring_force()
```

#### What It Shows

- **Physics:** F = -kx (restoring force)
- **Visualization:** Spring compressing and extending, mass oscillating
- **Plots:**
  - Oscillatory position vs time
  - Velocity vs time (sinusoidal)
  - Acceleration vs time
  - Phase space (elliptical orbit)

#### Parameters

- Mass: 1.0 kg
- Spring constant: 10.0 N/m
- Initial displacement: 1.0 m (stretched)
- Initial velocity: 0.0 m/s

#### Expected Results

- **Angular frequency:** `ω = √(k/m) = √10 ≈ 3.16 rad/s`
- **Period:** `T = 2π/ω ≈ 1.99 s`
- **Oscillation:** Simple harmonic motion

#### Modifying Parameters

```python
# Stiffer spring (faster oscillation)
k = 50.0  # N/m

# Heavier mass (slower oscillation)
mass = 5.0  # kg

# Larger initial displacement (more amplitude)
initial_position = 2.0  # m
```

### Example 3: Pendulum Swing

A nonlinear pendulum demonstrating energy conservation and periodic motion.

#### Code

```python
from newtons_law.newtons_second_law import example_3_pendulum_swing

example_3_pendulum_swing()
```

#### What It Shows

- **Physics:** θ̈ = -(g/L) sin(θ) (nonlinear pendulum equation)
- **Visualization:** Pendulum swinging with rod and bob, trajectory trail
- **Plots:**
  - Angle vs time
  - Velocity vs time
  - Energy (kinetic + potential, conserved)
  - Phase space

#### Parameters

- Pendulum length: 1.0 m
- Initial angle: 45° (π/4 radians)
- Initial angular velocity: 0.0 rad/s
- Gravity: 9.81 m/s²

#### Expected Results

- **Period:** Depends on amplitude (nonlinear)
- **Energy:** Total energy conserved (kinetic + potential)
- **Motion:** Periodic oscillation

#### Modifying Parameters

```python
# Longer pendulum (slower swing)
L = 2.0  # m

# Larger initial angle (more amplitude)
initial_angle = np.pi / 2  # 90 degrees

# Different gravity (e.g., Moon)
g = 1.62  # m/s²
```

### Example 4: Projectile with Air Resistance

1D vertical projectile motion comparing with and without air resistance.

#### Code

```python
from newtons_law.newtons_second_law import example_4_projectile_with_air_resistance

example_4_projectile_with_air_resistance()
```

#### What It Shows

- **Physics:** Gravity + Air resistance (F_drag = -k|v|v)
- **Visualization:** Projectile trajectory with theoretical path (dotted)
- **Plots:**
  - Height vs time (with/without air resistance)
  - Velocity vs time
  - Maximum height comparison
  - Time to max height comparison

#### Parameters

- Initial velocity: 30.0 m/s (upward)
- Air resistance coefficient: 0.1
- Gravity: 9.81 m/s²

#### Expected Results

- **With air resistance:** Lower maximum height, shorter flight time
- **Without air resistance:** Higher maximum height (theoretical)
- **Comparison:** Shows effect of air resistance

#### Modifying Parameters

```python
# Higher initial velocity
v0 = 50.0  # m/s

# More air resistance
k = 0.2  # Stronger drag

# Less air resistance
k = 0.05  # Weaker drag
```

## Parameters Reference

### Force Function

The force function must accept three arguments: `(t, x, v)`

```python
def my_force(t, x, v):
    """
    Parameters:
    -----------
    t : float
        Current time
    x : float
        Current position
    v : float
        Current velocity
    
    Returns:
    --------
    float : Force at this instant
    """
    return 10.0  # Example: constant force
```

### Common Force Functions

#### Constant Force
```python
def constant_force(t, x, v):
    return 10.0  # 10N constant
```

#### Spring Force (Hooke's Law)
```python
k = 10.0  # Spring constant

def spring_force(t, x, v):
    return -k * x  # Restoring force
```

#### Damped Oscillator
```python
k = 10.0  # Spring constant
b = 0.5   # Damping coefficient

def damped_force(t, x, v):
    return -k * x - b * v  # Spring + damping
```

#### Time-Dependent Force
```python
def time_force(t, x, v):
    return 10.0 * np.sin(t)  # Sinusoidal force
```

#### Position-Dependent Force
```python
def position_force(t, x, v):
    return -x**2  # Nonlinear force
```

## Visualization

### Static Plots

Each example generates 4 plots:
1. **Position vs Time** - Object's position over time
2. **Velocity vs Time** - Object's velocity over time
3. **Acceleration vs Time** - Object's acceleration over time
4. **Phase Space** - Velocity vs Position (trajectory in phase space)

### Animations

Each example includes an interactive animation:
- **Example 1:** Box moving with force vector
- **Example 2:** Spring compressing/extending with color-coded mass
- **Example 3:** Pendulum swinging with trajectory trail
- **Example 4:** Projectile motion with theoretical path

### Animation Features

- Real-time parameter display (time, position, velocity, etc.)
- Color-coded states (e.g., spring compression/extension)
- Trajectory trails
- Force vectors
- Theoretical vs actual paths

## Mathematical Background

### Numerical Integration

The equations of motion are solved using **scipy.integrate.odeint**, which uses the LSODA method (adaptive step size).

### System of ODEs

From F = ma, we get:
```
dx/dt = v
dv/dt = F(t, x, v) / m
```

This is a system of first-order ODEs, solved numerically.

### Energy Conservation

For conservative forces (like spring and pendulum):
- **Total Energy = Kinetic + Potential**
- Energy is conserved (constant)

For non-conservative forces (like air resistance):
- Energy decreases over time (dissipated)

## Tips and Best Practices

1. **Start simple:** Begin with constant force to understand the basics
2. **Experiment with parameters:** Change mass, force, initial conditions
3. **Understand phase space:** Phase plots show system behavior
4. **Check energy:** For conservative systems, energy should be constant
5. **Use appropriate time spans:** Longer simulations for slow systems

## Troubleshooting

### Issue: Unstable Solutions

**Solution:** Reduce time step or use smaller time span

### Issue: Animation Too Fast/Slow

**Solution:** Adjust `interval` parameter in `FuncAnimation`

### Issue: Unexpected Behavior

**Solution:** Check force function - ensure it returns correct units (Newtons)

### Issue: Energy Not Conserved

**Solution:** For conservative forces, check if force function is correct

## Advanced Usage

### Custom Force Function

```python
def custom_force(t, x, v):
    # Gravity
    F_gravity = -9.81 * system.mass
    
    # Air resistance
    F_drag = -0.1 * v * abs(v)
    
    # External force
    F_external = 10.0 * np.sin(2 * np.pi * t)
    
    return F_gravity + F_drag + F_external

t, x, v, a = system.solve_motion(
    force_func=custom_force,
    initial_position=0.0,
    initial_velocity=10.0,
    t_span=(0, 10),
    n_points=1000
)
```

### Multiple Forces

```python
def combined_forces(t, x, v):
    # Spring force
    F_spring = -10.0 * x
    
    # Damping
    F_damping = -0.5 * v
    
    # External driving force
    F_driving = 5.0 * np.cos(2 * np.pi * 0.5 * t)
    
    return F_spring + F_damping + F_driving
```

---

For more examples, see the main [README.md](../README.md) file.

