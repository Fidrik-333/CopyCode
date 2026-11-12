import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

print("=" * 60)
print("TRAINING EV RANGE PREDICTION MODEL...")
print("=" * 60)

# 1. Generate training data behind the scenes so the ML model learns the physics patterns
np.random.seed(42)
n_samples = 800

train_mass = np.random.uniform(1200, 2400, n_samples)      # Vehicle mass (kg)
train_battery = np.random.uniform(40, 100, n_samples)      # Battery capacity (kWh)
train_speed = np.random.uniform(30, 110, n_samples)        # Average speed (km/h)

# Physics approximation for energy consumption (Wh/km)
train_energy = 110 + (0.025 * train_mass) + (0.4 * (train_speed ** 1.15))
train_energy += np.random.normal(0, 4.0, n_samples)         # Minor sensor noise

train_range = (train_battery * 1000) / train_energy

# Create training DataFrame and train model
X_train = pd.DataFrame({
    'vehicle_mass_kg': train_mass,
    'battery_capacity_kwh': train_battery,
    'avg_speed_kmh': train_speed
})
y_train = train_range

ev_model = RandomForestRegressor(n_estimators=50, random_state=42)
ev_model.fit(X_train, y_train)

print("Model trained successfully!\n")
print("=" * 60)
print("INTERACTIVE EV RANGE PREDICTOR (Type 'q' at any prompt to quit)")
print("=" * 60)

# 2. Interactive While Loop for continuous predictions
while True:
    user_input = input("\nPress Enter to run a prediction (or type 'q' to quit): ").strip().lower()
    if user_input == 'q':
        print("Exiting predictor. Happy teaching your tech camp!")
        break
    
    try:
        print("\n--- Enter EV Trip Parameters ---")
        vehicle_mass_kg = float(input("Vehicle Weight (kg) [e.g., 1650]: "))
        battery_capacity_kwh = float(input("Battery Capacity (kWh) [e.g., 75]: "))
        avg_speed_kmh = float(input("Average Speed (km/h) [e.g., 60]: "))
        
        # Package inputs into a DataFrame for the model
        my_ev_trip = pd.DataFrame({
            'vehicle_mass_kg': [vehicle_mass_kg],
            'battery_capacity_kwh': [battery_capacity_kwh],
            'avg_speed_kmh': [avg_speed_kmh]
        })

        # Predict the achievable range
        predicted_range = ev_model.predict(my_ev_trip)[0]

        print("-" * 40)
        print(f"👉 Predicted Achievable Range: {predicted_range:.1f} km")
        print("-" * 40)

    except ValueError:
        print("❌ Invalid input! Please enter numerical values for weight, capacity, and speed.")
