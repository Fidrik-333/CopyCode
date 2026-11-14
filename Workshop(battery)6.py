import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

print("=" * 60)
print("TRAINING EV CHARGING TIME PREDICTION MODEL...")
print("=" * 60)

# 1. Generate training data incorporating CC/CV charging profile & thermal throttling
np.random.seed(42)
n_samples = 1000

train_capacity = np.random.uniform(40, 120, n_samples)       # Battery Capacity (kWh)
train_initial_soc = np.random.uniform(10, 60, n_samples)     # Start SoC (%)
train_target_soc = np.random.uniform(70, 100, n_samples)     # Target SoC (%)
train_charger_kw = np.random.choice([7.2, 22, 50, 150, 300], n_samples) # Charger Power (kW)
train_temp = np.random.uniform(-5, 45, n_samples)            # Battery Temp (°C)
train_soh = np.random.uniform(75, 100, n_samples)            # State of Health (%)

# Physics-informed charging time calculation (Hours)
# Energy to add (kWh)
energy_needed = train_capacity * ((train_target_soc - train_initial_soc) / 100.0)

# Base time based on charger power
base_hours = energy_needed / train_charger_kw

# Penalty factor 1: CV Phase slowdown (charging past 80% SoC takes significantly longer)
cv_penalty = np.where(train_target_soc > 80, 1.25 + (0.02 * (train_target_soc - 80)), 1.0)

# Penalty factor 2: Thermal throttling (cold or hot temps slow down charging)
thermal_penalty = np.where((train_temp < 10) | (train_temp > 35), 1.35, 1.0)

# Penalty factor 3: Battery degradation (lower SoH increases internal resistance)
soh_penalty = 1.0 + (0.005 * (100 - train_soh))

# Total realistic charging time in hours, converted to minutes
train_time_minutes = (base_hours * cv_penalty * thermal_penalty * soh_penalty) * 60.0
train_time_minutes += np.random.normal(0, 2.0, n_samples) # Add sensor noise
train_time_minutes = np.clip(train_time_minutes, 5.0, None) # Min charging time 5 mins

# Create training DataFrame and train model
X_train = pd.DataFrame({
    'battery_capacity_kwh': train_capacity,
    'initial_soc_pct': train_initial_soc,
    'target_soc_pct': train_target_soc,
    'charger_power_kw': train_charger_kw,
    'battery_temp_c': train_temp,
    'battery_soh_pct': train_soh
})
y_train = train_time_minutes

charge_model = RandomForestRegressor(n_estimators=50, random_state=42)
charge_model.fit(X_train, y_train)

print("Charging model trained successfully!\n")
print("=" * 60)
print("INTERACTIVE EV CHARGING PREDICTOR (Type 'q' at any prompt to quit)")
print("=" * 60)

# 2. Interactive While Loop for continuous student experiments
while True:
    user_input = input("\nPress Enter to run a charging prediction (or type 'q' to quit): ").strip().lower()
    if user_input == 'q':
        print("\n🎉 Excellent work wrapping up your tech camp! Wishing you a fantastic final session!")
        break

    try:
        print("\n--- Enter Charging Session Parameters ---")
        battery_capacity_kwh = float(input("Battery Capacity (kWh) [e.g., 75]: "))
        initial_soc_pct = float(input("Initial State of Charge (%) [e.g., 20]: "))
        target_soc_pct = float(input("Target State of Charge (%) [e.g., 80]: "))
        charger_power_kw = float(input("Charger Power Rating (kW) [e.g., 150]: "))
        battery_temp_c = float(input("Battery Temperature (°C) [e.g., 25]: "))
        battery_soh_pct = float(input("Battery State of Health (%) [e.g., 95]: "))

        # Package inputs into a DataFrame
        session_data = pd.DataFrame({
            'battery_capacity_kwh': [battery_capacity_kwh],
            'initial_soc_pct': [initial_soc_pct],
            'target_soc_pct': [target_soc_pct],
            'charger_power_kw': [charger_power_kw],
            'battery_temp_c': [battery_temp_c],
            'battery_soh_pct': [battery_soh_pct]
        })

        # Predict charging time
        predicted_minutes = charge_model.predict(session_data)[0]
        hours = int(predicted_minutes // 60)
        minutes = int(predicted_minutes % 60)

        print("-" * 45)
        if hours > 0:
            print(f"⚡ Predicted Charging Time: {hours} hour(s) and {minutes} minute(s) ({predicted_minutes:.1f} mins)")
        else:
            print(f"⚡ Predicted Charging Time: {predicted_minutes:.1f} minutes")
        print("-" * 45)

    except ValueError:
        print("❌ Invalid input! Please enter numerical values for all parameters.")
