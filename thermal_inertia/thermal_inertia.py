"""
Thermal Inertia Concept
=======================
Thermal Inertia measures how resistant a material is to temperature changes.

Thermal Inertia = √(k × ρ × c)
where:
- k = thermal conductivity (W/m·K)
- ρ = density (kg/m³)
- c = specific heat capacity (J/kg·K)

High thermal inertia = slow temperature change
Low thermal inertia = fast temperature change
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle

class ThermalInertia:
    """
    Thermal Inertia calculator and simulator.
    """
    def __init__(self, thermal_conductivity=1.0, density=1000.0, specific_heat=1000.0):
        """
        Initialize thermal properties.
        
        Parameters:
        -----------
        thermal_conductivity : float
            k (W/m·K)
        density : float
            ρ (kg/m³)
        specific_heat : float
            c (J/kg·K)
        """
        self.k = thermal_conductivity
        self.rho = density
        self.c = specific_heat
        self.thermal_inertia = np.sqrt(thermal_conductivity * density * specific_heat)
    
    def calculate_inertia(self):
        """Calculate thermal inertia."""
        return self.thermal_inertia
    
    def solve_temperature_response(self, initial_temp=25.0, ambient_temp=100.0,
                                  time_span=(0, 100), n_points=1000):
        """
        Solve temperature response to ambient temperature change.
        
        Uses: dT/dt = (h × A × (T_amb - T)) / (m × c)
        where h is heat transfer coefficient, A is area, m is mass
        """
        t = np.linspace(time_span[0], time_span[1], n_points)
        
        # Simplified: using thermal inertia to determine response time
        # Higher inertia = slower response
        tau = self.thermal_inertia / 100.0  # Time constant (scaled)
        
        def dT_dt(T, t_val):
            return (ambient_temp - T) / tau
        
        solution = odeint(dT_dt, initial_temp, t)
        T = solution[:, 0]
        
        return t, T

def example_1_different_materials():
    """
    Example 1: Different Materials with Different Thermal Inertia
    Compare: Water, Metal, Wood, Air
    """
    print("Example 1: Thermal Inertia of Different Materials")
    
    # Material properties (approximate)
    materials = {
        'Water': ThermalInertia(thermal_conductivity=0.6, density=1000, specific_heat=4180),
        'Aluminum': ThermalInertia(thermal_conductivity=205, density=2700, specific_heat=900),
        'Wood': ThermalInertia(thermal_conductivity=0.1, density=600, specific_heat=1700),
        'Air': ThermalInertia(thermal_conductivity=0.025, density=1.2, specific_heat=1005)
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Temperature response
    ax1 = axes[0, 0]
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, (name, material) in enumerate(materials.items()):
        t, T = material.solve_temperature_response(
            initial_temp=25.0,
            ambient_temp=100.0,
            time_span=(0, 200),
            n_points=1000
        )
        ax1.plot(t, T, color=colors[i], linewidth=2, label=f'{name} (I={material.thermal_inertia:.0f})')
    
    ax1.set_xlabel('Time (s)', fontsize=12)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.set_title('Temperature Response to Ambient Change', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=100, color='k', linestyle='--', alpha=0.3, label='Ambient Temp')
    
    # Plot 2: Thermal Inertia comparison
    ax2 = axes[0, 1]
    names = list(materials.keys())
    inertias = [m.thermal_inertia for m in materials.values()]
    bars = ax2.bar(names, inertias, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Thermal Inertia (√(k×ρ×c))', fontsize=12)
    ax2.set_title('Thermal Inertia Comparison', fontsize=14)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, inertia in zip(bars, inertias):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{inertia:.0f}', ha='center', va='bottom', fontsize=10)
    
    # Plot 3: Response time (time to reach 63% of final temp)
    ax3 = axes[1, 0]
    response_times = []
    for name, material in materials.items():
        t, T = material.solve_temperature_response(
            initial_temp=25.0,
            ambient_temp=100.0,
            time_span=(0, 200),
            n_points=1000
        )
        target_temp = 25.0 + 0.63 * (100.0 - 25.0)  # 63% of change
        idx = np.argmin(np.abs(T - target_temp))
        response_times.append(t[idx])
    
    bars = ax3.bar(names, response_times, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Response Time (s)', fontsize=12)
    ax3.set_title('Time to Reach 63% of Final Temperature', fontsize=14)
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, time_val in zip(bars, response_times):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{time_val:.1f}s', ha='center', va='bottom', fontsize=10)
    
    # Plot 4: Rate of temperature change
    ax4 = axes[1, 1]
    for i, (name, material) in enumerate(materials.items()):
        t, T = material.solve_temperature_response(
            initial_temp=25.0,
            ambient_temp=100.0,
            time_span=(0, 200),
            n_points=1000
        )
        dT_dt = np.gradient(T, t)
        ax4.plot(t, dT_dt, color=colors[i], linewidth=2, label=name)
    
    ax4.set_xlabel('Time (s)', fontsize=12)
    ax4.set_ylabel('Rate of Temp Change (°C/s)', fontsize=12)
    ax4.set_title('Rate of Temperature Change', fontsize=14)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle("Thermal Inertia: Different Materials", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('thermal_inertia_example1_materials.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Simulation: Material blocks heating up
    fig_anim, ax_anim = plt.subplots(figsize=(16, 8))
    ax_anim.set_xlim(-1, 8)
    ax_anim.set_ylim(-0.5, 2)
    ax_anim.set_xlabel('Position', fontsize=12)
    ax_anim.set_ylabel('Height', fontsize=12)
    ax_anim.set_title("Simulation: Materials Heating Up (Thermal Inertia Effect)", fontsize=14)
    ax_anim.axis('off')
    
    # Create material blocks
    blocks = []
    block_width = 1.5
    block_height = 1.5
    positions = [0.5, 2.5, 4.5, 6.5]
    block_names = list(materials.keys())
    block_colors = colors
    
    for i, (name, pos) in enumerate(zip(block_names, positions)):
        block = Rectangle((pos, 0), block_width, block_height,
                         facecolor=block_colors[i], edgecolor='black', linewidth=2)
        ax_anim.add_patch(block)
        blocks.append(block)
        
        # Label
        ax_anim.text(pos + block_width/2, -0.3, name, ha='center', fontsize=10, fontweight='bold')
        ax_anim.text(pos + block_width/2, block_height + 0.2, 
                    f'I={materials[name].thermal_inertia:.0f}', 
                    ha='center', fontsize=9)
    
    # Temperature text
    temp_texts = []
    for i, pos in enumerate(positions):
        text = ax_anim.text(pos + block_width/2, block_height/2, '25°C',
                           ha='center', va='center', fontsize=11, fontweight='bold',
                           color='white')
        temp_texts.append(text)
    
    # Heat source
    heat_source = Circle((0, 0.75), 0.2, facecolor='red', edgecolor='darkred', linewidth=2)
    ax_anim.add_patch(heat_source)
    ax_anim.text(0, 0.75, 'HEAT', ha='center', va='center', fontsize=8, 
                fontweight='bold', color='white')
    
    time_text = ax_anim.text(4, 1.8, '', fontsize=12, ha='center',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Get temperature data
    temp_data = {}
    for name, material in materials.items():
        t_temp, T_temp = material.solve_temperature_response(
            initial_temp=25.0, ambient_temp=100.0, time_span=(0, 200), n_points=1000
        )
        temp_data[name] = (t_temp, T_temp)
    
    def animate(frame):
        t_idx = frame * (len(temp_data['Water'][0]) // 200)
        if t_idx < len(temp_data['Water'][0]):
            current_time = temp_data['Water'][0][t_idx]
            
            for i, name in enumerate(block_names):
                t_vals, T_vals = temp_data[name]
                if t_idx < len(T_vals):
                    temp = T_vals[t_idx]
                    
                    # Update block color based on temperature
                    temp_ratio = (temp - 25.0) / (100.0 - 25.0)
                    temp_ratio = max(0, min(1, temp_ratio))
                    # Color from blue (cold) to red (hot)
                    color = plt.cm.RdYlBu(1 - temp_ratio)
                    blocks[i].set_facecolor(color)
                    
                    # Update temperature text
                    temp_texts[i].set_text(f'{temp:.1f}°C')
            
            time_text.set_text(f'Time: {current_time:.1f} s\nAmbient: 100°C')
        return blocks + temp_texts + [time_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=100, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()

def example_2_heating_cooling_cycle():
    """
    Example 2: Heating and Cooling Cycle
    Shows how thermal inertia affects heating and cooling rates.
    """
    print("\nExample 2: Heating and Cooling Cycle")
    
    # High inertia material (water)
    water = ThermalInertia(thermal_conductivity=0.6, density=1000, specific_heat=4180)
    # Low inertia material (aluminum)
    aluminum = ThermalInertia(thermal_conductivity=205, density=2700, specific_heat=900)
    
    # Heating phase
    t1, T1_water = water.solve_temperature_response(
        initial_temp=25.0, ambient_temp=100.0, time_span=(0, 50), n_points=500
    )
    t1, T1_alum = aluminum.solve_temperature_response(
        initial_temp=25.0, ambient_temp=100.0, time_span=(0, 50), n_points=500
    )
    
    # Cooling phase (from 100°C to 25°C)
    t2, T2_water = water.solve_temperature_response(
        initial_temp=100.0, ambient_temp=25.0, time_span=(0, 50), n_points=500
    )
    t2, T2_alum = aluminum.solve_temperature_response(
        initial_temp=100.0, ambient_temp=25.0, time_span=(0, 50), n_points=500
    )
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Heating phase
    axes[0, 0].plot(t1, T1_water, 'b-', linewidth=2, label=f'Water (I={water.thermal_inertia:.0f})')
    axes[0, 0].plot(t1, T1_alum, 'r--', linewidth=2, label=f'Aluminum (I={aluminum.thermal_inertia:.0f})')
    axes[0, 0].set_xlabel('Time (s)', fontsize=12)
    axes[0, 0].set_ylabel('Temperature (°C)', fontsize=12)
    axes[0, 0].set_title('Heating Phase (25°C → 100°C)', fontsize=14)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=100, color='k', linestyle='--', alpha=0.3)
    
    # Plot 2: Cooling phase
    axes[0, 1].plot(t2, T2_water, 'b-', linewidth=2, label='Water')
    axes[0, 1].plot(t2, T2_alum, 'r--', linewidth=2, label='Aluminum')
    axes[0, 1].set_xlabel('Time (s)', fontsize=12)
    axes[0, 1].set_ylabel('Temperature (°C)', fontsize=12)
    axes[0, 1].set_title('Cooling Phase (100°C → 25°C)', fontsize=14)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=25, color='k', linestyle='--', alpha=0.3)
    
    # Plot 3: Combined cycle
    t_combined = np.concatenate([t1, t1[-1] + t2])
    T_combined_water = np.concatenate([T1_water, T2_water])
    T_combined_alum = np.concatenate([T1_alum, T2_alum])
    
    axes[1, 0].plot(t_combined, T_combined_water, 'b-', linewidth=2, label='Water')
    axes[1, 0].plot(t_combined, T_combined_alum, 'r--', linewidth=2, label='Aluminum')
    axes[1, 0].axvline(x=t1[-1], color='gray', linestyle=':', alpha=0.5, label='Switch Point')
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Temperature (°C)', fontsize=12)
    axes[1, 0].set_title('Complete Heating-Cooling Cycle', fontsize=14)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Temperature difference from ambient
    diff_water_heat = 100.0 - T1_water
    diff_water_cool = T2_water - 25.0
    diff_alum_heat = 100.0 - T1_alum
    diff_alum_cool = T2_alum - 25.0
    
    axes[1, 1].plot(t1, diff_water_heat, 'b-', linewidth=2, label='Water (heating)', alpha=0.7)
    axes[1, 1].plot(t1, diff_alum_heat, 'r--', linewidth=2, label='Aluminum (heating)', alpha=0.7)
    axes[1, 1].plot(t1[-1] + t2, diff_water_cool, 'b:', linewidth=2, label='Water (cooling)', alpha=0.7)
    axes[1, 1].plot(t1[-1] + t2, diff_alum_cool, 'r:', linewidth=2, label='Aluminum (cooling)', alpha=0.7)
    axes[1, 1].set_xlabel('Time (s)', fontsize=12)
    axes[1, 1].set_ylabel('Temperature Difference from Ambient (°C)', fontsize=12)
    axes[1, 1].set_title('Temperature Difference from Ambient', fontsize=14)
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle("Thermal Inertia: Heating and Cooling Cycle", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('thermal_inertia_example2_heating_cooling.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Simulation: Heating and cooling cycle
    fig_anim, ax_anim = plt.subplots(figsize=(14, 6))
    ax_anim.set_xlim(-1, 6)
    ax_anim.set_ylim(-0.5, 2)
    ax_anim.set_xlabel('Position', fontsize=12)
    ax_anim.set_ylabel('Height', fontsize=12)
    ax_anim.set_title("Simulation: Heating and Cooling Cycle", fontsize=14)
    ax_anim.axis('off')
    
    # Two material blocks
    water_block = Rectangle((1, 0), 1.5, 1.5, facecolor='blue', 
                           edgecolor='black', linewidth=2)
    alum_block = Rectangle((3.5, 0), 1.5, 1.5, facecolor='red', 
                          edgecolor='black', linewidth=2)
    ax_anim.add_patch(water_block)
    ax_anim.add_patch(alum_block)
    
    ax_anim.text(1.75, -0.3, 'Water\n(High Inertia)', ha='center', fontsize=10, fontweight='bold')
    ax_anim.text(4.25, -0.3, 'Aluminum\n(Low Inertia)', ha='center', fontsize=10, fontweight='bold')
    
    water_text = ax_anim.text(1.75, 0.75, '25°C', ha='center', va='center',
                             fontsize=11, fontweight='bold', color='white')
    alum_text = ax_anim.text(4.25, 0.75, '25°C', ha='center', va='center',
                            fontsize=11, fontweight='bold', color='white')
    
    # Ambient temperature indicator
    ambient_indicator = Rectangle((0, 1.6), 0.3, 0.3, facecolor='red', 
                                  edgecolor='black', linewidth=1)
    ax_anim.add_patch(ambient_indicator)
    ambient_text = ax_anim.text(0.15, 1.75, 'Amb', ha='center', fontsize=8)
    
    time_text = ax_anim.text(2.5, 1.8, '', fontsize=12, ha='center',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Combined cycle data
    t_combined = np.concatenate([t1, t1[-1] + t2])
    T_combined_water = np.concatenate([T1_water, T2_water])
    T_combined_alum = np.concatenate([T1_alum, T2_alum])
    ambient_combined = np.concatenate([np.full_like(t1, 100.0), np.full_like(t2, 25.0)])
    
    def animate(frame):
        idx = frame * (len(t_combined) // 200)
        if idx < len(t_combined):
            # Update water block
            temp_water = T_combined_water[idx]
            temp_ratio_w = (temp_water - 25.0) / (100.0 - 25.0) if ambient_combined[idx] > 25 else (temp_water - 25.0) / (100.0 - 25.0)
            temp_ratio_w = max(0, min(1, abs(temp_ratio_w)))
            color_w = plt.cm.RdYlBu(1 - temp_ratio_w)
            water_block.set_facecolor(color_w)
            water_text.set_text(f'{temp_water:.1f}°C')
            
            # Update aluminum block
            temp_alum = T_combined_alum[idx]
            temp_ratio_a = (temp_alum - 25.0) / (100.0 - 25.0) if ambient_combined[idx] > 25 else (temp_alum - 25.0) / (100.0 - 25.0)
            temp_ratio_a = max(0, min(1, abs(temp_ratio_a)))
            color_a = plt.cm.RdYlBu(1 - temp_ratio_a)
            alum_block.set_facecolor(color_a)
            alum_text.set_text(f'{temp_alum:.1f}°C')
            
            # Update ambient
            ambient_temp = ambient_combined[idx]
            ambient_color = 'red' if ambient_temp > 60 else 'blue' if ambient_temp < 40 else 'orange'
            ambient_indicator.set_facecolor(ambient_color)
            ambient_text.set_text(f'{ambient_temp:.0f}°C')
            
            phase = "Heating" if ambient_temp > 25 else "Cooling"
            time_text.set_text(f'Time: {t_combined[idx]:.1f} s\nPhase: {phase}\n'
                             f'Ambient: {ambient_temp:.0f}°C')
        return [water_block, alum_block, water_text, alum_text, ambient_indicator, time_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=100, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()

def example_3_varying_inertia():
    """
    Example 3: Effect of Varying Thermal Inertia
    Same material with different thermal inertia values.
    """
    print("\nExample 3: Effect of Varying Thermal Inertia")
    
    # Create materials with different inertia by varying properties
    materials = {
        'Low Inertia': ThermalInertia(thermal_conductivity=1.0, density=100, specific_heat=100),
        'Medium Inertia': ThermalInertia(thermal_conductivity=10.0, density=1000, specific_heat=1000),
        'High Inertia': ThermalInertia(thermal_conductivity=100.0, density=5000, specific_heat=2000)
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    colors = ['red', 'orange', 'blue']
    
    # Plot 1: Temperature response
    ax1 = axes[0, 0]
    for i, (name, material) in enumerate(materials.items()):
        t, T = material.solve_temperature_response(
            initial_temp=25.0,
            ambient_temp=100.0,
            time_span=(0, 300),
            n_points=1000
        )
        ax1.plot(t, T, color=colors[i], linewidth=2, 
                label=f'{name} (I={material.thermal_inertia:.0f})')
    
    ax1.set_xlabel('Time (s)', fontsize=12)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.set_title('Temperature Response vs Thermal Inertia', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Response speed comparison
    ax2 = axes[0, 1]
    response_speeds = []
    for name, material in materials.items():
        t, T = material.solve_temperature_response(
            initial_temp=25.0,
            ambient_temp=100.0,
            time_span=(0, 300),
            n_points=1000
        )
        # Time to reach 50% of final temperature
        target = 25.0 + 0.5 * (100.0 - 25.0)
        idx = np.argmin(np.abs(T - target))
        response_speeds.append(t[idx])
    
    bars = ax2.bar(list(materials.keys()), response_speeds, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Time to 50% Response (s)', fontsize=12)
    ax2.set_title('Response Speed Comparison', fontsize=14)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, speed in zip(bars, response_speeds):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{speed:.1f}s', ha='center', va='bottom', fontsize=10)
    
    # Plot 3: Rate of change
    ax3 = axes[1, 0]
    for i, (name, material) in enumerate(materials.items()):
        t, T = material.solve_temperature_response(
            initial_temp=25.0,
            ambient_temp=100.0,
            time_span=(0, 300),
            n_points=1000
        )
        dT_dt = np.gradient(T, t)
        ax3.plot(t, dT_dt, color=colors[i], linewidth=2, label=name)
    
    ax3.set_xlabel('Time (s)', fontsize=12)
    ax3.set_ylabel('Rate of Temp Change (°C/s)', fontsize=12)
    ax3.set_title('Rate of Temperature Change', fontsize=14)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Thermal inertia vs response time
    ax4 = axes[1, 1]
    inertias = [m.thermal_inertia for m in materials.values()]
    ax4.scatter(inertias, response_speeds, s=200, c=colors, alpha=0.7, edgecolors='black')
    for i, name in enumerate(materials.keys()):
        ax4.annotate(name, (inertias[i], response_speeds[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    ax4.set_xlabel('Thermal Inertia', fontsize=12)
    ax4.set_ylabel('Response Time (s)', fontsize=12)
    ax4.set_title('Thermal Inertia vs Response Time', fontsize=14)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle("Thermal Inertia: Effect of Varying Inertia", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('thermal_inertia_example3_varying_inertia.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Simulation: Varying inertia materials
    fig_anim, ax_anim = plt.subplots(figsize=(16, 6))
    ax_anim.set_xlim(-0.5, 10)
    ax_anim.set_ylim(-0.5, 2)
    ax_anim.set_xlabel('Position', fontsize=12)
    ax_anim.set_ylabel('Height', fontsize=12)
    ax_anim.set_title("Simulation: Materials with Different Thermal Inertia", fontsize=14)
    ax_anim.axis('off')
    
    # Create blocks
    blocks = []
    positions = [1, 3.5, 6]
    block_names = list(materials.keys())
    block_colors = colors
    
    for i, (name, pos) in enumerate(zip(block_names, positions)):
        block = Rectangle((pos, 0), 2, 1.5, facecolor=block_colors[i], 
                         edgecolor='black', linewidth=2)
        ax_anim.add_patch(block)
        blocks.append(block)
        ax_anim.text(pos + 1, -0.3, name, ha='center', fontsize=10, fontweight='bold')
        ax_anim.text(pos + 1, 1.8, f'I={materials[name].thermal_inertia:.0f}', 
                    ha='center', fontsize=9)
    
    temp_texts = []
    for i, pos in enumerate(positions):
        text = ax_anim.text(pos + 1, 0.75, '25°C', ha='center', va='center',
                           fontsize=11, fontweight='bold', color='white')
        temp_texts.append(text)
    
    heat_source = Circle((0.5, 0.75), 0.15, facecolor='red', edgecolor='darkred')
    ax_anim.add_patch(heat_source)
    
    time_text = ax_anim.text(5, 1.8, '', fontsize=12, ha='center',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    temp_data = {}
    for name, material in materials.items():
        t_temp, T_temp = material.solve_temperature_response(
            initial_temp=25.0, ambient_temp=100.0, time_span=(0, 300), n_points=1000
        )
        temp_data[name] = (t_temp, T_temp)
    
    def animate(frame):
        t_idx = frame * (len(temp_data['Low Inertia'][0]) // 200)
        if t_idx < len(temp_data['Low Inertia'][0]):
            current_time = temp_data['Low Inertia'][0][t_idx]
            for i, name in enumerate(block_names):
                t_vals, T_vals = temp_data[name]
                if t_idx < len(T_vals):
                    temp = T_vals[t_idx]
                    temp_ratio = (temp - 25.0) / (100.0 - 25.0)
                    temp_ratio = max(0, min(1, temp_ratio))
                    color = plt.cm.RdYlBu(1 - temp_ratio)
                    blocks[i].set_facecolor(color)
                    temp_texts[i].set_text(f'{temp:.1f}°C')
            time_text.set_text(f'Time: {current_time:.1f} s\nAmbient: 100°C')
        return blocks + temp_texts + [time_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=100, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()

def example_4_practical_applications():
    """
    Example 4: Practical Applications
    Building materials, cooking, climate control
    """
    print("\nExample 4: Practical Applications of Thermal Inertia")
    
    applications = {
        'Brick Wall': ThermalInertia(thermal_conductivity=0.7, density=1800, specific_heat=840),
        'Concrete': ThermalInertia(thermal_conductivity=1.4, density=2400, specific_heat=880),
        'Steel': ThermalInertia(thermal_conductivity=50, density=7800, specific_heat=500),
        'Insulation': ThermalInertia(thermal_conductivity=0.04, density=50, specific_heat=1030)
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    colors_list = ['brown', 'gray', 'silver', 'yellow']
    
    # Plot 1: Temperature response
    ax1 = axes[0, 0]
    for i, (name, material) in enumerate(applications.items()):
        t, T = material.solve_temperature_response(
            initial_temp=20.0,
            ambient_temp=40.0,
            time_span=(0, 500),
            n_points=1000
        )
        ax1.plot(t, T, color=colors_list[i], linewidth=2, 
                label=f'{name} (I={material.thermal_inertia:.0f})')
    
    ax1.set_xlabel('Time (s)', fontsize=12)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.set_title('Building Materials: Response to Heat', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Thermal inertia bar chart
    ax2 = axes[0, 1]
    names = list(applications.keys())
    inertias = [m.thermal_inertia for m in applications.values()]
    bars = ax2.bar(names, inertias, color=colors_list, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Thermal Inertia', fontsize=12)
    ax2.set_title('Thermal Inertia of Building Materials', fontsize=14)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, inertia in zip(bars, inertias):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{inertia:.0f}', ha='center', va='bottom', fontsize=9)
    
    # Plot 3: Energy storage capacity
    ax3 = axes[1, 0]
    # Energy stored = m × c × ΔT (proportional to ρ × c for unit volume)
    energy_capacity = [m.rho * m.c for m in applications.values()]
    bars = ax3.bar(names, energy_capacity, color=colors_list, alpha=0.7, edgecolor='black')
    ax3.set_ylabel('Energy Capacity (J/m³·K)', fontsize=12)
    ax3.set_title('Energy Storage Capacity', fontsize=14)
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Plot 4: Time constant comparison
    ax4 = axes[1, 1]
    time_constants = []
    for name, material in applications.items():
        t, T = material.solve_temperature_response(
            initial_temp=20.0,
            ambient_temp=40.0,
            time_span=(0, 500),
            n_points=1000
        )
        # Time to reach 63% of change
        target = 20.0 + 0.63 * (40.0 - 20.0)
        idx = np.argmin(np.abs(T - target))
        time_constants.append(t[idx])
    
    bars = ax4.bar(names, time_constants, color=colors_list, alpha=0.7, edgecolor='black')
    ax4.set_ylabel('Time Constant (s)', fontsize=12)
    ax4.set_title('Thermal Time Constant', fontsize=14)
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, tc in zip(bars, time_constants):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{tc:.0f}s', ha='center', va='bottom', fontsize=9)
    
    plt.suptitle("Thermal Inertia: Practical Applications", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig('thermal_inertia_example4_applications.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Simulation: Building materials
    fig_anim, ax_anim = plt.subplots(figsize=(18, 6))
    ax_anim.set_xlim(-0.5, 10)
    ax_anim.set_ylim(-0.5, 2)
    ax_anim.set_xlabel('Position', fontsize=12)
    ax_anim.set_ylabel('Height', fontsize=12)
    ax_anim.set_title("Simulation: Building Materials Thermal Response", fontsize=14)
    ax_anim.axis('off')
    
    # Create building material blocks
    blocks = []
    positions = [0.5, 2.2, 4, 5.8]
    block_names = list(applications.keys())
    block_colors = colors_list
    
    for i, (name, pos) in enumerate(zip(block_names, positions)):
        block = Rectangle((pos, 0), 1.5, 1.5, facecolor=block_colors[i], 
                         edgecolor='black', linewidth=2)
        ax_anim.add_patch(block)
        blocks.append(block)
        ax_anim.text(pos + 0.75, -0.3, name, ha='center', fontsize=9, fontweight='bold',
                    rotation=45 if len(name) > 8 else 0)
        ax_anim.text(pos + 0.75, 1.8, f'I={applications[name].thermal_inertia:.0f}', 
                    ha='center', fontsize=8)
    
    temp_texts = []
    for i, pos in enumerate(positions):
        text = ax_anim.text(pos + 0.75, 0.75, '20°C', ha='center', va='center',
                           fontsize=10, fontweight='bold', color='white')
        temp_texts.append(text)
    
    # Sun/heat source
    sun = Circle((0.2, 1.5), 0.2, facecolor='yellow', edgecolor='orange', linewidth=2)
    ax_anim.add_patch(sun)
    ax_anim.text(0.2, 1.5, '☀', ha='center', va='center', fontsize=20)
    
    time_text = ax_anim.text(5, 1.8, '', fontsize=11, ha='center',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    temp_data = {}
    for name, material in applications.items():
        t_temp, T_temp = material.solve_temperature_response(
            initial_temp=20.0, ambient_temp=40.0, time_span=(0, 500), n_points=1000
        )
        temp_data[name] = (t_temp, T_temp)
    
    def animate(frame):
        t_idx = frame * (len(temp_data['Brick Wall'][0]) // 200)
        if t_idx < len(temp_data['Brick Wall'][0]):
            current_time = temp_data['Brick Wall'][0][t_idx]
            for i, name in enumerate(block_names):
                t_vals, T_vals = temp_data[name]
                if t_idx < len(T_vals):
                    temp = T_vals[t_idx]
                    temp_ratio = (temp - 20.0) / (40.0 - 20.0)
                    temp_ratio = max(0, min(1, temp_ratio))
                    color = plt.cm.RdYlBu(1 - temp_ratio)
                    blocks[i].set_facecolor(color)
                    temp_texts[i].set_text(f'{temp:.1f}°C')
            time_text.set_text(f'Time: {current_time:.0f} s\nAmbient: 40°C')
        return blocks + temp_texts + [time_text]
    
    anim = FuncAnimation(fig_anim, animate, frames=200, interval=100, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Thermal Inertia Demonstrations")
    print("=" * 50)
    
    example_1_different_materials()
    example_2_heating_cooling_cycle()
    example_3_varying_inertia()
    example_4_practical_applications()

