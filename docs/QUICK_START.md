# Quick Start Guide

Get started with Physics Simulations in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/physics-with-python.git
cd physics-with-python

# Install dependencies
pip install -r requirements.txt
```

## Your First Simulation

### 1. Heat Equation (1D)

```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d, plot_heat_equation_1d

# Create a hot rod
x, t, u = solve_heat_equation_1d(
    L=1.0, T=2.0, alpha=0.01, nx=100, nt=1000,
    base_temperature=25.0,
    boundary_left=100.0,    # Hot left end
    boundary_right=0.0      # Cold right end
)

# Visualize
plot_heat_equation_1d(x, t, u)
```

### 2. Newton's Second Law

```python
from newtons_law.newtons_second_law import example_1_constant_force

# Run constant force example
example_1_constant_force()
```

### 3. Thermal Inertia

```python
from thermal_inertia.thermal_inertia import example_1_different_materials

# Compare different materials
example_1_different_materials()
```

## Run All Examples

```bash
# Heat Equation
python heat_equation/heat_equation_1d.py
python heat_equation/heat_equation_2d.py

# Newton's Law
python newtons_law/newtons_second_law.py

# Thermal Inertia
python thermal_inertia/thermal_inertia.py
```

## Next Steps

1. Read the [main README](../README.md) for overview
2. Check [Heat Equation docs](HEAT_EQUATION.md) for details
3. Explore [Newton's Law docs](NEWTONS_LAW.md) for examples
4. Learn about [Thermal Inertia](THERMAL_INERTIA.md)

## Common Tasks

### Change Parameters

```python
# Faster heat transfer
x, t, u = solve_heat_equation_1d(alpha=0.05)  # Increase alpha

# More accurate (slower)
x, t, u = solve_heat_equation_1d(nx=200, nt=2000)  # More points
```

### Save Animations

```python
plot_heat_equation_1d(x, t, u, save_animation=True)  # Saves as GIF
```

### Custom Hot Spots

```python
# 1D: Hot spot at center
point_temperatures={'center': 100.0}

# 2D: Multiple hot spots
point_temperatures={
    (0.1, 0.1): 100.0,  # Bottom-left
    (0.9, 0.9): 80.0    # Top-right
}
```

## Troubleshooting

**Problem:** Module not found
```bash
# Make sure you're in the project directory
cd physics-with-python
python heat_equation/heat_equation_1d.py
```

**Problem:** Slow performance
```python
# Reduce grid points
nx=50, ny=50, nt=500  # Instead of 100, 100, 1000
```

**Problem:** Stability warning
```python
# Reduce thermal diffusivity
alpha=0.001  # Instead of 0.01
```

## Need Help?

- Check the [documentation](README.md)
- Read example code in each module
- Open an issue on GitHub

Happy Simulating! 🚀

