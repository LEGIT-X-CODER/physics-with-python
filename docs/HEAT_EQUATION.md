# Heat Equation Documentation

Complete guide for 1D and 2D Heat Equation solvers with examples, parameters, and visualization options.

## Table of Contents

- [Overview](#overview)
- [1D Heat Equation](#1d-heat-equation)
- [2D Heat Equation](#2d-heat-equation)
- [Parameters Reference](#parameters-reference)
- [Examples](#examples)
- [Visualization](#visualization)
- [Mathematical Background](#mathematical-background)

## Overview

The heat equation describes how temperature changes over time in a material. This implementation uses the **Finite Difference Method** with the **FTCS (Forward Time, Centered Space)** scheme to solve the equation numerically.

### Mathematical Formulation

**1D Heat Equation:**
```
∂u/∂t = α(∂²u/∂x²)
```

**2D Heat Equation:**
```
∂u/∂t = α(∂²u/∂x² + ∂²u/∂y²)
```

where:
- `u(x,t)` = temperature at position x and time t
- `α` = thermal diffusivity coefficient
- `x`, `y` = spatial coordinates
- `t` = time

## 1D Heat Equation

### Function: `solve_heat_equation_1d()`

Solves the 1D heat equation for a rod of length L.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `L` | float | 1.0 | Length of the rod (meters) |
| `T` | float | 0.5 | Total simulation time (seconds) |
| `alpha` | float | 0.01 | Thermal diffusivity coefficient |
| `nx` | int | 100 | Number of spatial grid points |
| `nt` | int | 1000 | Number of time steps |
| `initial_condition` | function/array | None | Initial temperature distribution |
| `boundary_left` | float | None | Left boundary temperature (°C) |
| `boundary_right` | float | None | Right boundary temperature (°C) |
| `boundary_type` | str | 'dirichlet' | 'dirichlet' or 'neumann' |
| `base_temperature` | float | 25.0 | Base/ambient temperature (°C) |
| `point_temperatures` | dict | None | Hot spots: {'left': 100.0, 'center': 80.0, 'right': 50.0} |

#### Returns

- `x` (array): Spatial grid points
- `t` (array): Time points
- `u` (array): Temperature distribution u(x, t) of shape (nt, nx)

#### Example

```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d

# Rod with hot left end and cold right end
x, t, u = solve_heat_equation_1d(
    L=1.0,                    # 1 meter rod
    T=2.0,                    # Simulate for 2 seconds
    alpha=0.01,               # Thermal diffusivity
    nx=100,                   # 100 spatial points
    nt=1000,                  # 1000 time steps
    base_temperature=25.0,    # Base temperature 25°C
    boundary_left=100.0,      # Left end at 100°C
    boundary_right=0.0,       # Right end at 0°C
    boundary_type='dirichlet' # Fixed temperature boundaries
)
```

### Function: `plot_heat_equation_1d()`

Visualizes the 1D heat equation solution with multiple plots and animations.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | array | Required | Spatial grid points |
| `t` | array | Required | Time points |
| `u` | array | Required | Temperature distribution |
| `save_animation` | bool | False | Save animation as GIF |
| `rod_height` | float | 0.1 | Height of rod visualization |

#### Output

Creates 4 plots:
1. **Rod Visualization** - Colored rod at different times
2. **Temperature Distribution** - Line plots over time
3. **Space-Time Heat Map** - Temperature evolution
4. **Heat Balance** - Average temperature over time

Plus an animated rod visualization.

#### Example

```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d, plot_heat_equation_1d

x, t, u = solve_heat_equation_1d(
    L=1.0, T=2.0, alpha=0.01, nx=100, nt=1000,
    base_temperature=25.0,
    point_temperatures={'center': 100.0}
)

plot_heat_equation_1d(x, t, u, save_animation=False)
```

### Hot Spots

You can create localized hot spots using `point_temperatures`:

```python
point_temperatures={
    'left': 100.0,    # Hot spot at left end
    'center': 80.0,   # Hot spot at center
    'right': 50.0     # Hot spot at right end
}
```

Hot spots are created using Gaussian distributions (not single points) for realistic temperature profiles.

## 2D Heat Equation

### Function: `solve_heat_equation_2d()`

Solves the 2D heat equation for a plate of dimensions Lx × Ly.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Lx` | float | 1.0 | Plate width (meters) |
| `Ly` | float | 1.0 | Plate height (meters) |
| `T` | float | 0.1 | Total simulation time (seconds) |
| `alpha` | float | 0.01 | Thermal diffusivity coefficient |
| `nx` | int | 50 | Number of grid points in x direction |
| `ny` | int | 50 | Number of grid points in y direction |
| `nt` | int | 200 | Number of time steps |
| `initial_condition` | function/array | None | Initial temperature distribution |
| `boundary_conditions` | str/dict | 'zero' | Boundary conditions |
| `base_temperature` | float | 25.0 | Base/ambient temperature (°C) |
| `point_temperatures` | dict | None | Hot spots: {(x, y): temperature} |

#### Boundary Conditions

**String options:**
- `'zero'` - Base temperature at all boundaries
- `'insulated'` - Zero heat flux (Neumann boundary)

**Dictionary option:**
```python
boundary_conditions={
    'left': 100.0,    # Left boundary temperature
    'right': 0.0,     # Right boundary temperature
    'top': 25.0,      # Top boundary temperature
    'bottom': 25.0    # Bottom boundary temperature
}
```

#### Returns

- `x` (array): X spatial grid points
- `y` (array): Y spatial grid points
- `t` (array): Time points
- `u` (array): Temperature distribution u(x, y, t) of shape (nt, ny, nx)

#### Example

```python
from heat_equation.heat_equation_2d import solve_heat_equation_2d

# Plate with hot spots at corners
x, y, t, u = solve_heat_equation_2d(
    Lx=1.0, Ly=1.0,           # 1m × 1m plate
    T=0.5,                    # Simulate for 0.5 seconds
    alpha=0.01,               # Thermal diffusivity
    nx=100, ny=100,           # 100×100 grid
    nt=500,                   # 500 time steps
    base_temperature=25.0,    # Base temperature 25°C
    point_temperatures={
        (0.1, 0.1): 100.0,   # Bottom-left hot spot
        (0.9, 0.9): 80.0     # Top-right hot spot
    },
    boundary_conditions={
        'left': 25.0,
        'right': 25.0,
        'top': 25.0,
        'bottom': 25.0
    }
)
```

### Function: `plot_heat_equation_2d()`

Visualizes the 2D heat equation solution with contour plots and heat flow vectors.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | array | Required | X spatial grid points |
| `y` | array | Required | Y spatial grid points |
| `t` | array | Required | Time points |
| `u` | array | Required | Temperature distribution |
| `save_animation` | bool | False | Save animation as GIF |
| `show_heat_flow` | bool | True | Show heat flow vectors |

#### Output

Creates 6 plots:
1-4. **Temperature Contours** - At different times with heat flow arrows
5. **Heat Balance** - Average temperature over time
6. **Temperature Range** - Min/max temperature over time

Plus an animated contour plot with heat flow visualization.

#### Example

```python
from heat_equation.heat_equation_2d import solve_heat_equation_2d, plot_heat_equation_2d

x, y, t, u = solve_heat_equation_2d(
    Lx=1.0, Ly=1.0, T=0.5, alpha=0.01,
    nx=100, ny=100, nt=500,
    base_temperature=25.0,
    point_temperatures={
        (0.1, 0.1): 100.0,
        (0.9, 0.9): 80.0
    }
)

plot_heat_equation_2d(x, y, t, u, show_heat_flow=True, save_animation=False)
```

### Multiple Hot Spots

You can create multiple hot spots at different locations:

```python
point_temperatures={
    (0.1, 0.1): 100.0,   # Bottom-left corner
    (0.9, 0.1): 100.0,   # Bottom-right corner
    (0.1, 0.9): 80.0,    # Top-left corner
    (0.9, 0.9): 80.0,    # Top-right corner
    (0.5, 0.5): 60.0     # Center
}
```

## Parameters Reference

### Critical Parameters

#### Thermal Diffusivity (`alpha`)

Controls how fast heat spreads:
- **Small α (0.001-0.01)**: Slow heat transfer
- **Large α (0.05-0.1)**: Fast heat transfer

**Typical values:**
- Air: ~0.00002 m²/s
- Water: ~0.000001 m²/s
- Steel: ~0.00001 m²/s

#### Grid Points (`nx`, `ny`)

Affects accuracy and performance:
- **Few points (50-100)**: Faster, less accurate
- **Many points (200+)**: Slower, more accurate

#### Time Steps (`nt`)

Affects animation smoothness:
- **Few steps (500)**: Choppy animation
- **Many steps (2000+)**: Smooth animation

### Stability Condition

The solver automatically checks stability:

**1D:** `dt ≤ dx²/(2α)`

**2D:** `dt ≤ min(dx², dy²)/(4α)`

If violated, a warning is displayed. To fix:
- Reduce `alpha`
- Increase `nx`/`ny`
- Reduce `T` (simulation time)

## Examples

### Example 1: Hot Rod with Cold Ends

```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d, plot_heat_equation_1d

x, t, u = solve_heat_equation_1d(
    L=1.0, T=2.0, alpha=0.01, nx=100, nt=1000,
    base_temperature=25.0,
    boundary_left=100.0,    # Hot left
    boundary_right=0.0,     # Cold right
    boundary_type='dirichlet'
)

plot_heat_equation_1d(x, t, u)
```

### Example 2: Hot Center Spot

```python
x, t, u = solve_heat_equation_1d(
    L=1.0, T=1.5, alpha=0.01, nx=100, nt=800,
    base_temperature=25.0,
    point_temperatures={'center': 100.0}
)

plot_heat_equation_1d(x, t, u)
```

### Example 3: Four Corner Hot Spots

```python
from heat_equation.heat_equation_2d import solve_heat_equation_2d, plot_heat_equation_2d

x, y, t, u = solve_heat_equation_2d(
    Lx=1.0, Ly=1.0, T=0.6, alpha=0.01,
    nx=100, ny=100, nt=600,
    base_temperature=25.0,
    point_temperatures={
        (0.1, 0.1): 100.0,  # Bottom-left
        (0.9, 0.1): 100.0,  # Bottom-right
        (0.1, 0.9): 100.0,  # Top-left
        (0.9, 0.9): 100.0   # Top-right
    }
)

plot_heat_equation_2d(x, y, t, u, show_heat_flow=True)
```

### Example 4: Custom Initial Condition

```python
import numpy as np

def custom_initial(x):
    """Gaussian hot spot at center"""
    L = x[-1] - x[0]
    center = L / 2
    return 25.0 + 75.0 * np.exp(-((x - center)**2) / (2 * 0.1**2))

x, t, u = solve_heat_equation_1d(
    L=1.0, T=1.5, alpha=0.01, nx=100, nt=800,
    initial_condition=custom_initial,
    base_temperature=25.0
)

plot_heat_equation_1d(x, t, u)
```

## Visualization

### Color Scheme

**1D Heat Equation:**
- Dark Blue → Blue → Cyan → Green → Yellow → Orange → Red → Dark Red
- Blue = Cold, Red = Hot

**2D Heat Equation:**
- Same color scheme with contour plots
- White arrows show heat flow direction

### Animation

Animations show real-time temperature evolution:
- **1D:** Rod colors change as heat spreads
- **2D:** Contour plots update with heat flow vectors

To save animations:
```python
plot_heat_equation_1d(x, t, u, save_animation=True)  # Saves as GIF
```

## Mathematical Background

### Finite Difference Method

The heat equation is discretized using:

**1D:**
```
u[i]^(n+1) = u[i]^n + r * (u[i+1]^n - 2*u[i]^n + u[i-1]^n)
```

where `r = α * dt / dx²`

**2D:**
```
u[i,j]^(n+1) = u[i,j]^n + rx * d²u/dx² + ry * d²u/dy²
```

where:
- `rx = α * dt / dx²`
- `ry = α * dt / dy²`

### Boundary Conditions

**Dirichlet (Fixed Temperature):**
```
u(0, t) = T_left
u(L, t) = T_right
```

**Neumann (Fixed Heat Flux):**
```
∂u/∂x(0, t) = q_left
∂u/∂x(L, t) = q_right
```

## Tips and Best Practices

1. **Start with default parameters** and adjust gradually
2. **Check stability warnings** - they indicate potential numerical issues
3. **Use appropriate grid sizes** - balance accuracy and speed
4. **Experiment with hot spots** - try different locations and temperatures
5. **Save animations** for presentations or documentation

## Troubleshooting

### Issue: Stability Warning

**Solution:** Reduce `alpha` or increase `nx`/`ny`

### Issue: Slow Performance

**Solution:** Reduce `nx`, `ny`, or `nt`

### Issue: Heat Not Spreading

**Solution:** Check `alpha` value - might be too small

### Issue: Animation Not Smooth

**Solution:** Increase `nt` (time steps)

---

For more examples, see the main [README.md](../README.md) file.

