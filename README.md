# Physics Simulations with Python 🚀

A comprehensive collection of physics simulations and numerical methods implemented in Python. This repository contains educational implementations of heat transfer, Newton's laws, thermal inertia, and mathematical series with beautiful visualizations and animations.

**Created by Aman Singh**

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Projects](#projects)
- [Documentation](#documentation)
- [Examples](#examples)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **1D & 2D Heat Equation Solvers** - Finite difference methods with animated visualizations
- **Newton's Second Law** - Multiple force scenarios with interactive demonstrations
- **Thermal Inertia** - Material property analysis and temperature response simulations
- **Beautiful Visualizations** - Custom colormaps, animations, and interactive plots
- **Well-Documented Code** - Comprehensive comments and docstrings
- **Educational Examples** - Ready-to-run examples for learning

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/LEGIT-X-CODER/physics-with-python.git
cd physics-with-python
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Required Packages

- `numpy >= 1.21.0` - Numerical computations
- `matplotlib >= 3.5.0` - Plotting and visualization
- `scipy >= 1.7.0` - Scientific computing and ODE solvers

## 🚀 Quick Start

### Run All Examples

Each module can be run directly to see example outputs:

```bash
# Heat Equation
python heat_equation/heat_equation_1d.py
python heat_equation/heat_equation_2d.py

# Newton's Second Law
python newtons_law/newtons_second_law.py

# Thermal Inertia
python thermal_inertia/thermal_inertia.py
```

### Use as a Library

```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d, plot_heat_equation_1d

# Solve 1D heat equation
x, t, u = solve_heat_equation_1d(
    L=1.0, T=2.0, alpha=0.01, nx=100, nt=1000,
    base_temperature=25.0,
    point_temperatures={'center': 100.0}
)

# Visualize results
plot_heat_equation_1d(x, t, u)
```

## 📚 Projects

### 1. Heat Equation

#### 1D Heat Equation
Simulates heat transfer in a one-dimensional rod using the finite difference method.

**Features:**
- Dirichlet and Neumann boundary conditions
- Point temperature sources (hot spots)
- Base temperature settings
- Animated rod visualization
- Space-time heat maps

**Example:**
```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d, plot_heat_equation_1d

x, t, u = solve_heat_equation_1d(
    L=1.0,                    # Rod length (m)
    T=2.0,                    # Simulation time (s)
    alpha=0.01,               # Thermal diffusivity
    nx=100,                   # Spatial grid points
    nt=1000,                  # Time steps
    base_temperature=25.0,    # Base temperature (°C)
    boundary_left=100.0,      # Left boundary temp (°C)
    boundary_right=0.0,      # Right boundary temp (°C)
    point_temperatures={'center': 100.0}  # Hot spot
)

plot_heat_equation_1d(x, t, u)
```

#### 2D Heat Equation
Simulates heat transfer in a two-dimensional plate with multiple hot spots.

**Features:**
- Multiple hot spot locations
- Custom boundary conditions
- Heat flow vector visualization
- Contour plots with custom colormaps
- Real-time animations

**Example:**
```python
from heat_equation.heat_equation_2d import solve_heat_equation_2d, plot_heat_equation_2d

x, y, t, u = solve_heat_equation_2d(
    Lx=1.0, Ly=1.0,           # Plate dimensions (m)
    T=0.5,                    # Simulation time (s)
    alpha=0.01,               # Thermal diffusivity
    nx=100, ny=100,           # Grid points
    nt=500,                   # Time steps
    base_temperature=25.0,    # Base temperature (°C)
    point_temperatures={
        (0.1, 0.1): 100.0,   # Bottom-left hot spot
        (0.9, 0.9): 80.0     # Top-right hot spot
    }
)

plot_heat_equation_2d(x, y, t, u, show_heat_flow=True)
```

### 2. Newton's Second Law

Demonstrates F = ma with various force scenarios and visual animations.

**Examples:**
1. **Constant Force** - Box pushed with constant force
2. **Spring Force** - Mass-spring system with Hooke's Law
3. **Pendulum Swing** - Nonlinear pendulum motion
4. **Projectile Motion** - 1D vertical motion with air resistance

**Example:**
```python
from newtons_law.newtons_second_law import NewtonsSecondLaw

# Create system
system = NewtonsSecondLaw(mass=2.0)

# Define force function
def constant_force(t, x, v):
    return 10.0  # 10N constant force

# Solve motion
t, x, v, a = system.solve_motion(
    force_func=constant_force,
    initial_position=0.0,
    initial_velocity=0.0,
    t_span=(0, 5),
    n_points=500
)
```

**Run all examples:**
```bash
python newtons_law/newtons_second_law.py
```

### 3. Thermal Inertia

Analyzes how different materials respond to temperature changes based on thermal properties.

**Features:**
- Material property comparison
- Heating and cooling cycles
- Response time analysis
- Practical applications (building materials)

**Thermal Inertia Formula:**
```
I = √(k × ρ × c)
where:
- k = thermal conductivity (W/m·K)
- ρ = density (kg/m³)
- c = specific heat capacity (J/kg·K)
```

**Example:**
```python
from thermal_inertia.thermal_inertia import ThermalInertia

# Create material
water = ThermalInertia(
    thermal_conductivity=0.6,
    density=1000,
    specific_heat=4180
)

# Calculate thermal inertia
inertia = water.calculate_inertia()
print(f"Thermal Inertia: {inertia:.2f}")

# Simulate temperature response
t, T = water.solve_temperature_response(
    initial_temp=25.0,
    ambient_temp=100.0,
    time_span=(0, 200),
    n_points=1000
)
```

**Run all examples:**
```bash
python thermal_inertia/thermal_inertia.py
```

## 📖 Documentation

Detailed documentation is available for each module:

- **[Heat Equation Documentation](docs/HEAT_EQUATION.md)** - Complete guide for 1D and 2D heat equation solvers
- **[Newton's Law Documentation](docs/NEWTONS_LAW.md)** - Guide for Newton's Second Law examples
- **[Thermal Inertia Documentation](docs/THERMAL_INERTIA.md)** - Thermal inertia concept and applications

## 📊 Examples

### Example 1: Hot Rod Simulation

```python
from heat_equation.heat_equation_1d import solve_heat_equation_1d, plot_heat_equation_1d

# Create a rod with hot left end and cold right end
x, t, u = solve_heat_equation_1d(
    L=1.0, T=2.0, alpha=0.01, nx=100, nt=1000,
    base_temperature=25.0,
    boundary_left=100.0,    # Hot left end
    boundary_right=0.0,     # Cold right end
    boundary_type='dirichlet'
)

plot_heat_equation_1d(x, t, u)
```

### Example 2: Multiple Hot Spots on Plate

```python
from heat_equation.heat_equation_2d import solve_heat_equation_2d, plot_heat_equation_2d

# Create plate with hot spots at corners
x, y, t, u = solve_heat_equation_2d(
    Lx=1.0, Ly=1.0, T=0.5, alpha=0.01,
    nx=100, ny=100, nt=500,
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

### Example 3: Spring Oscillation

```python
from newtons_law.newtons_second_law import example_2_spring_force

# Run spring force example
example_2_spring_force()
```

## 🖼️ Output

Running the scripts generates:

- **Static Plots** - PNG images saved automatically
- **Animations** - Interactive matplotlib animations
- **GIF Files** - Optional GIF exports (set `save_animation=True`)

### Output Files

- `heat_equation_1d_solution.png` - 1D heat equation plots
- `heat_equation_2d_solution.png` - 2D heat equation plots
- `newtons_law_example*.png` - Newton's law example plots
- `thermal_inertia_example*.png` - Thermal inertia plots
- `*_animation.gif` - Animation files (if saved)

## 📁 Project Structure

```
physics-with-python/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── heat_equation/
│   ├── heat_equation_1d.py      # 1D Heat Equation solver
│   └── heat_equation_2d.py      # 2D Heat Equation solver
├── newtons_law/
│   └── newtons_second_law.py    # Newton's Second Law examples
├── thermal_inertia/
│   └── thermal_inertia.py       # Thermal Inertia simulations
└── docs/
    ├── HEAT_EQUATION.md         # Heat equation documentation
    ├── NEWTONS_LAW.md           # Newton's law documentation
    └── THERMAL_INERTIA.md       # Thermal inertia documentation
```

## 🔬 Mathematical Background

### Heat Equation

**1D:** ∂u/∂t = α(∂²u/∂x²)

**2D:** ∂u/∂t = α(∂²u/∂x² + ∂²u/∂y²)

Solved using **Finite Difference Method** with **FTCS** (Forward Time, Centered Space) scheme.

**Stability Condition:** dt ≤ dx²/(2α) for 1D, dt ≤ min(dx², dy²)/(4α) for 2D

### Newton's Second Law

**F = ma** (Force = mass × acceleration)

Solved using **scipy.integrate.odeint** with LSODA method.

### Thermal Inertia

**I = √(k × ρ × c)**

- High inertia → Slow temperature change
- Low inertia → Fast temperature change

## 🎯 Key Parameters

### Heat Equation Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `L`, `Lx`, `Ly` | Domain size (m) | 0.5 - 5.0 |
| `T` | Simulation time (s) | 0.1 - 10.0 |
| `alpha` | Thermal diffusivity | 0.001 - 0.1 |
| `nx`, `ny` | Grid points | 50 - 200 |
| `nt` | Time steps | 500 - 2000 |
| `base_temperature` | Base temp (°C) | 0 - 100 |

### Newton's Law Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `mass` | Object mass (kg) | 0.1 - 10.0 |
| `force` | Applied force (N) | 1 - 100 |
| `k` | Spring constant (N/m) | 1 - 100 |
| `L` | Pendulum length (m) | 0.5 - 5.0 |

### Thermal Inertia Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `thermal_conductivity` | k (W/m·K) | 0.01 - 400 |
| `density` | ρ (kg/m³) | 1 - 8000 |
| `specific_heat` | c (J/kg·K) | 100 - 5000 |

## 🐛 Troubleshooting

### Common Issues

1. **Stability Warning**
   - **Problem:** Heat equation solver shows stability warning
   - **Solution:** Reduce `alpha` or increase `nx`/`ny`, or reduce `dt`

2. **Slow Performance**
   - **Problem:** Simulations run slowly
   - **Solution:** Reduce `nx`, `ny`, or `nt` values

3. **Animation Not Showing**
   - **Problem:** Animation window doesn't appear
   - **Solution:** Ensure matplotlib backend is set correctly (usually automatic)

4. **Import Errors**
   - **Problem:** Module not found errors
   - **Solution:** Ensure you're running from the project root directory

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Aman Singh**

- Created and developed all physics simulations
- Implemented numerical methods and visualizations
- Designed educational examples and documentation

## 🙏 Acknowledgments

- Built for educational purposes
- Uses standard numerical methods from computational physics
- Inspired by various physics simulation tutorials

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**Made with ❤️ by Aman Singh for physics enthusiasts**
