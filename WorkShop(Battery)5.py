import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_text

print("=" * 60)
print("TRAINING EV CHARGING DECISION TREE MODEL...")
print("=" * 60)

# 1. Generate synthetic training data based on charging physics
np.random.seed(42)
n_samples = 1000

train_capacity = np.random.uniform(40, 120, n_samples)       # Battery Capacity (kWh)
train_initial_soc = np.random.uniform(10, 60, n_samples)     # Start SoC (%)
train_target_soc = np.random.uniform(70, 100, n_samples)     # Target SoC (%)
train_charger_kw = np.random.choice([7.2, 22, 50, 150, 300], n_samples) # Charger Power (kW)

# Physics approximation for charging time (Minutes)
energy_needed = train_capacity * ((train_target_soc - train_initial_soc) / 100.0)
base_hours = energy_needed / train_charger_kw
cv_penalty = np.where(train_target_soc > 80, 1.25, 1.0)
train_time_minutes = (base_hours * cv_penalty) * 60.0
train_time_minutes += np.random.normal(0, 1.0, n_samples) # Sensor noise

# Create training DataFrame
X_train = pd.DataFrame({
    'battery_capacity_kwh': train_capacity,
    'initial_soc_pct': train_initial_soc,
    'target_soc_pct': train_target_soc,
    'charger_power_kw': train_charger_kw
})
y_train = train_time_minutes

# Train a shallow Decision Tree so students can easily inspect the readable rules
tree_model = DecisionTreeRegressor(max_depth=4, random_state=42)
tree_model.fit(X_train, y_train)

print("Decision Tree trained successfully!\n")

# 2. Print out the readable text-based decision rules for Data Science students
print("=" * 60)
print("EXTRACTED DECISION TREE RULES (IF-THEN LOGIC PATHS):")
print("=" * 60)
tree_rules = export_text(tree_model, feature_names=list(X_train.columns))
print(tree_rules)

print("=" * 60)
print("INTERACTIVE EV CHARGING DECISION PREDICTOR (Type 'q' to quit)")
print("=" * 60)

# 3. Interactive While Loop for live classroom experimentation
while True:
    user_input = input("\nPress Enter to test a charging scenario (or type 'q' to quit): ").strip().lower()
    if user_input == 'q':
        print("\n🚀 Wishing you an incredible final session and a successful tech camp!")
        break

    try:
        print("\n--- Enter Charging Parameters ---")
        battery_capacity_kwh = float(input("Battery Capacity (kWh) [e.g., 75]: "))
        initial_soc_pct = float(input("Initial State of Charge (%) [e.g., 20]: "))
        target_soc_pct = float(input("Target State of Charge (%) [e.g., 80]: "))
        charger_power_kw = float(input("Charger Power Rating (kW) [e.g., 150]: "))

        # Package inputs into a DataFrame
        sample_trip = pd.DataFrame({
            'battery_capacity_kwh': [battery_capacity_kwh],
            'initial_soc_pct': [initial_soc_pct],
            'target_soc_pct': [target_soc_pct],
            'charger_power_kw': [charger_power_kw]
        })

        # Predict using the Decision Tree
        predicted_minutes = tree_model.predict(sample_trip)[0]
        hours = int(predicted_minutes // 60)
        minutes = int(predicted_minutes % 60)

        print("-" * 45)
        if hours > 0:
            print(f"⚡ Tree Predicted Charging Time: {hours} hr {minutes} min ({predicted_minutes:.1f} mins)")
        else:
            print(f"⚡ Tree Predicted Charging Time: {predicted_minutes:.1f} minutes")
        print("-" * 45)

    except ValueError:
        print("❌ Invalid input! Please enter numerical values.")
