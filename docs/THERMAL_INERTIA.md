# Thermal Inertia Documentation

Complete guide for thermal inertia simulations, material property analysis, and temperature response studies.

## Table of Contents

- [Overview](#overview)
- [Class: ThermalInertia](#class-thermalinertia)
- [Examples](#examples)
- [Parameters Reference](#parameters-reference)
- [Material Properties](#material-properties)
- [Visualization](#visualization)
- [Mathematical Background](#mathematical-background)

## Overview

Thermal inertia measures how resistant a material is to temperature changes. Materials with high thermal inertia change temperature slowly, while materials with low thermal inertia change temperature quickly.

### Thermal Inertia Formula

```
I = √(k × ρ × c)
```

where:
- `I` = Thermal Inertia
- `k` = Thermal Conductivity (W/m·K)
- `ρ` = Density (kg/m³)
- `c` = Specific Heat Capacity (J/kg·K)

### Physical Meaning

- **High Thermal Inertia:**
  - Slow temperature change
  - Good for thermal storage
  - Examples: Water, Concrete, Brick

- **Low Thermal Inertia:**
  - Fast temperature change
  - Good for quick response
  - Examples: Air, Insulation, Light materials

## Class: ThermalInertia

### Initialization

```python
from thermal_inertia.thermal_inertia import ThermalInertia

material = ThermalInertia(
    thermal_conductivity=0.6,    # k (W/m·K)
    density=1000,                # ρ (kg/m³)
    specific_heat=4180           # c (J/kg·K)
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `thermal_conductivity` | float | 1.0 | k - Heat transfer rate (W/m·K) |
| `density` | float | 1000.0 | ρ - Material density (kg/m³) |
| `specific_heat` | float | 1000.0 | c - Heat capacity (J/kg·K) |

#### Properties

After initialization, the class automatically calculates:
- `self.thermal_inertia` - Thermal inertia value

### Method: `calculate_inertia()`

Returns the calculated thermal inertia.

```python
inertia = material.calculate_inertia()
print(f"Thermal Inertia: {inertia:.2f}")
```

### Method: `solve_temperature_response()`

Simulates how material temperature responds to ambient temperature changes.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_temp` | float | 25.0 | Initial temperature (°C) |
| `ambient_temp` | float | 100.0 | Ambient temperature (°C) |
| `time_span` | tuple | (0, 100) | Time span (start, end) in seconds |
| `n_points` | int | 1000 | Number of time points |

#### Returns

- `t` (array): Time points
- `T` (array): Temperature at each time point

#### Example

```python
t, T = material.solve_temperature_response(
    initial_temp=25.0,      # Start at 25°C
    ambient_temp=100.0,    # Heat to 100°C
    time_span=(0, 200),    # Over 200 seconds
    n_points=1000
)
```

## Examples

### Example 1: Different Materials

Compares thermal inertia of different materials (Water, Aluminum, Wood, Air).

#### Code

```python
from thermal_inertia.thermal_inertia import example_1_different_materials

example_1_different_materials()
```

#### What It Shows

- **Materials compared:**
  - Water (High inertia)
  - Aluminum (Medium inertia)
  - Wood (Low inertia)
  - Air (Very low inertia)

- **Plots:**
  1. Temperature response over time
  2. Thermal inertia bar chart
  3. Response time comparison
  4. Rate of temperature change

- **Visualization:** Material blocks heating up with color-coded temperatures

#### Expected Results

- **Water:** Slowest to heat (highest inertia)
- **Aluminum:** Moderate response
- **Wood:** Faster response
- **Air:** Fastest response (lowest inertia)

### Example 2: Heating and Cooling Cycle

Shows how materials respond to heating and cooling cycles.

#### Code

```python
from thermal_inertia.thermal_inertia import example_2_heating_cooling_cycle

example_2_heating_cooling_cycle()
```

#### What It Shows

- **Materials:** Water (high inertia) vs Aluminum (low inertia)
- **Cycle:** Heating (25°C → 100°C) then Cooling (100°C → 25°C)
- **Plots:**
  1. Heating phase
  2. Cooling phase
  3. Complete cycle
  4. Temperature difference from ambient

- **Visualization:** Two material blocks showing heating/cooling with ambient indicator

#### Key Insights

- High inertia materials: Slow heating AND slow cooling
- Low inertia materials: Fast heating AND fast cooling
- Response time depends on thermal inertia

### Example 3: Varying Thermal Inertia

Demonstrates effect of different thermal inertia values.

#### Code

```python
from thermal_inertia.thermal_inertia import example_3_varying_inertia

example_3_varying_inertia()
```

#### What It Shows

- **Materials:** Low, Medium, High inertia materials
- **Plots:**
  1. Temperature response comparison
  2. Response speed (time to 50% change)
  3. Rate of temperature change
  4. Thermal inertia vs response time

- **Visualization:** Three material blocks with different inertia values

#### Expected Results

- Lower inertia → Faster response
- Higher inertia → Slower response
- Linear relationship between inertia and response time

### Example 4: Practical Applications

Real-world building materials and their thermal properties.

#### Code

```python
from thermal_inertia.thermal_inertia import example_4_practical_applications

example_4_practical_applications()
```

#### What It Shows

- **Materials:**
  - Brick Wall
  - Concrete
  - Steel
  - Insulation

- **Plots:**
  1. Temperature response to heat
  2. Thermal inertia comparison
  3. Energy storage capacity
  4. Thermal time constant

- **Visualization:** Building material blocks with sun/heat source

#### Applications

- **Brick/Concrete:** High inertia - good for thermal mass
- **Steel:** Medium inertia - structural material
- **Insulation:** Low inertia - fast response, good for control

## Parameters Reference

### Thermal Conductivity (k)

**Units:** W/m·K (Watts per meter per Kelvin)

**Typical Values:**
- Air: 0.025 W/m·K
- Water: 0.6 W/m·K
- Wood: 0.1 W/m·K
- Steel: 50 W/m·K
- Aluminum: 205 W/m·K

**Effect:** Higher k → Faster heat transfer → Lower inertia (if other factors same)

### Density (ρ)

**Units:** kg/m³ (kilograms per cubic meter)

**Typical Values:**
- Air: 1.2 kg/m³
- Water: 1000 kg/m³
- Wood: 600 kg/m³
- Steel: 7800 kg/m³
- Concrete: 2400 kg/m³

**Effect:** Higher ρ → Higher inertia (more mass to heat)

### Specific Heat Capacity (c)

**Units:** J/kg·K (Joules per kilogram per Kelvin)

**Typical Values:**
- Air: 1005 J/kg·K
- Water: 4180 J/kg·K
- Wood: 1700 J/kg·K
- Steel: 500 J/kg·K
- Concrete: 880 J/kg·K

**Effect:** Higher c → More energy needed to heat → Higher inertia

### Combined Effect

All three factors combine:
```
I = √(k × ρ × c)
```

- High k, high ρ, high c → Very high inertia
- Low k, low ρ, low c → Very low inertia

## Material Properties

### Common Materials

| Material | k (W/m·K) | ρ (kg/m³) | c (J/kg·K) | I (approx) |
|----------|-----------|-----------|------------|------------|
| Air | 0.025 | 1.2 | 1005 | ~5 |
| Water | 0.6 | 1000 | 4180 | ~1600 |
| Wood | 0.1 | 600 | 1700 | ~320 |
| Aluminum | 205 | 2700 | 900 | ~22,000 |
| Steel | 50 | 7800 | 500 | ~14,000 |
| Concrete | 1.4 | 2400 | 880 | ~1,700 |
| Brick | 0.7 | 1800 | 840 | ~1,000 |
| Insulation | 0.04 | 50 | 1030 | ~45 |

### Creating Custom Materials

```python
# Custom material: High thermal inertia
custom = ThermalInertia(
    thermal_conductivity=1.0,    # Moderate conductivity
    density=3000,                # High density
    specific_heat=2000           # High specific heat
)

inertia = custom.calculate_inertia()
print(f"Custom Material Inertia: {inertia:.2f}")
```

## Visualization

### Static Plots

Each example generates multiple plots:
1. **Temperature Response** - Temperature vs time
2. **Thermal Inertia Comparison** - Bar charts
3. **Response Time** - Time to reach certain temperature
4. **Rate of Change** - Temperature change rate

### Animations

Interactive animations show:
- Material blocks with color-coded temperatures
- Real-time temperature display
- Ambient temperature indicators
- Heat source visualization

### Color Coding

- **Blue/Cold:** Low temperature
- **Red/Hot:** High temperature
- **Gradient:** Temperature transition

## Mathematical Background

### Temperature Response Model

The temperature response follows:
```
dT/dt = (T_amb - T) / τ
```

where:
- `T` = Material temperature
- `T_amb` = Ambient temperature
- `τ` = Time constant (proportional to thermal inertia)

### Time Constant

The time constant `τ` is related to thermal inertia:
```
τ ∝ I
```

Higher inertia → Larger time constant → Slower response

### Energy Storage

Energy stored in material:
```
E = m × c × ΔT
```

where:
- `m` = Mass (ρ × volume)
- `c` = Specific heat
- `ΔT` = Temperature change

## Tips and Best Practices

1. **Understand the formula:** I = √(k × ρ × c)
2. **Compare materials:** Use example 1 to see differences
3. **Consider applications:** High inertia for storage, low for control
4. **Experiment with values:** Try different combinations
5. **Check response times:** Use plots to understand behavior

## Troubleshooting

### Issue: Temperature Not Changing

**Solution:** Check if thermal inertia is too high (very slow response)

### Issue: Temperature Changes Too Fast

**Solution:** Increase thermal inertia (higher k, ρ, or c)

### Issue: Unrealistic Values

**Solution:** Use realistic material properties from tables

## Applications

### Building Design

- **Thermal Mass:** High inertia materials (concrete, brick) store heat
- **Insulation:** Low inertia materials (insulation) respond quickly
- **Energy Efficiency:** Balance between storage and response

### Cooking

- **Pans:** High conductivity (aluminum) for fast heating
- **Ovens:** High inertia (ceramic) for stable temperature

### Climate Control

- **Buildings:** High inertia materials reduce temperature swings
- **Vehicles:** Low inertia for quick heating/cooling

---

For more examples, see the main [README.md](../README.md) file.

