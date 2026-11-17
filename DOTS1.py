import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. VEHICLE & ENVIRONMENT CONFIGURATION
# ==========================================
mass = 1600.0          # Vehicle mass (kg)
g = 9.81             # Acceleration due to gravity (m/s^2)
rho = 1.225          # Air density (kg/m^3)
C_d = 0.28           # Drag coefficient
A_frontal = 2.2      # Frontal area (m^2)
C_rr = 0.012         # Rolling resistance coefficient
eta_drivetrain = 0.92# Total motor & inverter efficiency
battery_capacity_kWh = 75.0 # Total battery capacity in kWh

# ==========================================
# 2. GENERATE A SYNTHETIC DRIVE CYCLE (Data Stream)
# ==========================================
# Let's simulate a 300-second trip comprising acceleration, cruising,
# hill climbing, and deceleration.
time = np.arange(0, 301, 1) # Time steps in seconds

# Create a velocity profile (m/s)
# 0-50s: accelerating, 50-150s: cruising, 150-200s: uphill, 200-300s: deceleration & stop
velocity = np.piecewise(time,
    [time <= 50, (time > 50) & (time <= 150), (time > 150) & (time <= 200), time > 200],
    [lambda t: 0.4 * t,
     lambda t: 20.0,
     lambda t: 20.0 - 0.1 * (t - 150), # slowing down slightly on a hill
     lambda t: 15.0 * (1 - (t - 200)/100)]
)
velocity = np.clip(velocity, 0, None) # Ensure speed never goes negative

# Compute acceleration (dv/dt) using NumPy's gradient function
acceleration = np.gradient(velocity, time)

# Simulate road slope angle (radians): A 5-degree incline between t=150 and t=200
road_angle = np.zeros_like(time)
road_angle[(time >= 150) & (time <= 200)] = np.radians(5.0)

# ==========================================
# 3. PHYSICS-BASED FORCE & POWER CALCULATIONS
# ==========================================
# Force components (Newtons)
F_inertia = mass * acceleration
F_aero = 0.5 * rho * C_d * A_frontal * (velocity ** 2)
F_roll = C_rr * mass * g * np.cos(road_angle)
F_grade = mass * g * np.sin(road_angle)

# Total tractive force required at the wheels
F_tractive = F_inertia + F_aero + F_roll + F_grade

# Instantaneous Power at wheels (Watts) -> P = Force * Velocity
# If power is negative (braking/coasting), account for regenerative braking efficiency
power_wheels = F_tractive * velocity
power_battery = np.where(
    power_wheels >= 0,
    power_wheels / eta_drivetrain,           # Discharging efficiency losses
    power_wheels * eta_drivetrain            # Regenerative braking recovery
)

# Convert power from Watts to Kilowatt-hours (kWh) per second step (dt = 1 sec)
energy_consumed_kWh = np.cumsum(power_battery) / 3600.0 / 1000.0
total_energy_used = energy_consumed_kWh[-1]

# Estimated Driving Range calculation based on current trip efficiency
total_distance_km = np.sum(velocity) * 1 / 3600.0 # Total distance in km
if total_energy_used > 0:
    efficiency_Wh_per_km = (total_energy_used * 1000) / total_distance_km
    estimated_total_range_km = (battery_capacity_kWh * 1000) / efficiency_Wh_per_km
else:
    estimated_total_range_km = 0.0

print(f"--- EV SIMULATION RESULTS ---")
print(f"Total Distance Covered: {total_distance_km:.2f} km")
print(f"Energy Consumed: {total_energy_used:.4f} kWh")
print(f"Average Efficiency: {efficiency_Wh_per_km:.2f} Wh/km")
print(f"Projected Full Battery Range: {estimated_total_range_km:.1f} km")

# ==========================================
# 4. VISUALIZATION (Data Science Dashboards)
# ==========================================
fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

# Plot 1: Velocity Profile
axes[0].plot(time, velocity * 3.6, color='blue', linewidth=2)
axes[0].set_ylabel("Speed (km/h)")
axes[0].set_title("EV Drive Cycle & Longitudinal Dynamics Simulation")
axes[0].grid(True)

# Plot 2: Force Breakdown
axes[1].plot(time, F_aero, label="Aerodynamic Drag", color='orange')
axes[1].plot(time, F_roll, label="Rolling Resistance", color='green')
axes[1].plot(time, F_grade, label="Grade/Gravity Force", color='purple')
axes[1].plot(time, F_tractive, label="Total Tractive Force", color='red', linestyle='--')
axes[1].set_ylabel("Forces (N)")
axes[1].legend(loc="upper left")
axes[1].grid(True)

# Plot 3: Cumulative Battery Energy Depletion
axes[2].plot(time, energy_consumed_kWh, color='crimson', linewidth=2)
axes[2].set_ylabel("Energy Used (kWh)")
axes[2].set_xlabel("Time (seconds)")
axes[2].grid(True)

plt.tight_layout()
plt.show()
