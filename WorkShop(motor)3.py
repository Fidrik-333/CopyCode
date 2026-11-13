import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_text

print("=" * 60)
print("TRAINING EV MOTOR EFFICIENCY (MTPA) MODEL...")
print("=" * 60)

# 1. Generate synthetic training data for Motor Efficiency & MTPA Control
np.random.seed(42)
n_samples = 1000

train_torque = np.random.uniform(10, 300, n_samples)      # Required Motor Torque (Nm)
train_speed = np.random.uniform(500, 12000, n_samples)    # Motor Speed (RPM)
train_temp = np.random.uniform(20, 100, n_samples)        # Motor Stator Temp (°C)

# Physics approximation for Maximum Torque Per Ampere (MTPA) optimal d-axis current (Amps)
# In reluctance-assisted or interior PMSMs, negative d-axis current is injected at higher torques
# to leverage reluctance torque and minimize total stator current magnitude (copper losses).
optimal_id = np.where(
    train_torque > 150,
    -0.35 * (train_torque - 150) - (0.01 * (train_speed / 1000)),
    0.0 # Zero d-axis current at low torque regions (pure surface PMSM mode)
)
optimal_id += np.random.normal(0, 1.5, n_samples) # Add controller noise

# Calculate resulting total losses (Copper losses + Iron losses in Watts)
copper_loss = 3 * (5.0 * (1.0 + 0.004 * train_temp)) * ((train_torque / 200.0)**2 + optimal_id**2)
iron_loss = 0.02 * (train_speed / 1000.0) * (train_torque / 50.0)
total_loss_watts = copper_loss + iron_loss

# Create training DataFrame
X_train = pd.DataFrame({
    'required_torque_nm': train_torque,
    'motor_speed_rpm': train_speed,
    'stator_temp_c': train_temp
})
y_train = optimal_id  # Target: Optimal d-axis current to minimize losses

# Train a Decision Tree Regressor for interpretable rule extraction
efficiency_tree = DecisionTreeRegressor(max_depth=4, random_state=42)
efficiency_tree.fit(X_train, y_train)

print("Motor Efficiency Model trained successfully!\n")

# 2. Print out the readable text-based decision rules for Data Science students
print("=" * 60)
print("EXTRACTED MOTOR OPTIMIZATION RULES (IF-THEN LOGIC PATHS):")
print("=" * 60)
tree_rules = export_text(efficiency_tree, feature_names=list(X_train.columns))
print(tree_rules)

print("=" * 60)
print("INTERACTIVE MOTOR EFFICIENCY PREDICTOR (Type 'q' to quit)")
print("=" * 60)

# 3. Interactive While Loop for live classroom experimentation
while True:
    user_input = input("\nPress Enter to test an operating point (or type 'q' to quit): ").strip().lower()
    if user_input == 'q':
        print("\n🎓 Congratulations on completing your EV Tech Camp with AI/DS students! Have a wonderful final day!")
        break

    try:
        print("\n--- Enter Motor Operating Parameters ---")
        required_torque_nm = float(input("Required Torque (Nm) [e.g., 180]: "))
        motor_speed_rpm = float(input("Motor Speed (RPM) [e.g., 4000]: "))
        stator_temp_c = float(input("Stator Temperature (°C) [e.g., 65]: "))

        # Package inputs into a DataFrame
        sample_operating_point = pd.DataFrame({
            'required_torque_nm': [required_torque_nm],
            'motor_speed_rpm': [motor_speed_rpm],
            'stator_temp_c': [stator_temp_c]
        })

        # Predict optimal d-axis current using the Decision Tree
        pred_id = efficiency_tree.predict(sample_operating_point)[0]

        # Estimate power loss savings compared to unoptimized control (Id = 0)
        est_loss_saved_watts = abs(pred_id) * 12.5

        print("-" * 45)
        print(f"⚙️ Optimal d-axis Current (Id): {pred_id:.2f} A")
        print(f"💡 Estimated Power Loss Saved:  {est_loss_saved_watts:.1f} Watts")
        print("-" * 45)

    except ValueError:
        print("❌ Invalid input! Please enter numerical values.")
