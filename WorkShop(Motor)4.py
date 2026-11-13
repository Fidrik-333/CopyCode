import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

print("=" * 60)
print("TRAINING EV MOTOR EFFICIENCY ZONE CLASSIFIER...")
print("=" * 60)

# 1. Generate synthetic training data for motor operational efficiency zones
np.random.seed(42)
n_samples = 1200

train_torque = np.random.uniform(5, 300, n_samples)        # Motor Torque (Nm)
train_speed = np.random.uniform(200, 10000, n_samples)    # Motor Speed (RPM)
train_freq = np.random.choice([5000, 10000, 20000], n_samples) # Inverter Switching Frequency (Hz)

# Physics logic to determine efficiency class:
# Class 0: Low/Poor Efficiency (< 85%) - Extreme high speed/torque or inefficient high switching loss
# Class 1: Moderate Efficiency (85% - 92%)
# Class 2: High Efficiency / Sweet Spot (> 92%) - Optimal mid-range torque and speed
efficiency_score = 95.0 - (0.015 * abs(train_speed - 4500)) - (0.02 * abs(train_torque - 120)) - (0.0003 * train_freq)
efficiency_score += np.random.normal(0, 1.5, n_samples) # Add noise

# Convert continuous score into discrete classes for classification
# 2: High Efficiency, 1: Moderate, 0: Low Efficiency
efficiency_class = np.where(efficiency_score > 91.0, 2, np.where(efficiency_score >= 86.0, 1, 0))

# Create training DataFrame
X_train = pd.DataFrame({
    'motor_torque_nm': train_torque,
    'motor_speed_rpm': train_speed,
    'switching_freq_hz': train_freq
})
y_train = efficiency_class

# Train an interpretable Decision Tree Classifier
efficiency_classifier = DecisionTreeClassifier(max_depth=4, random_state=42)
efficiency_classifier.fit(X_train, y_train)

print("Efficiency Zone Classifier trained successfully!\n")

# 2. Print out the readable text-based decision rules for Data Science students
print("=" * 60)
print("EXTRACTED EFFICIENCY CLASSIFICATION RULES (IF-THEN LOGIC):")
print("=" * 60)
tree_rules = export_text(efficiency_classifier, feature_names=list(X_train.columns))
print(tree_rules)

print("=" * 60)
print("INTERACTIVE MOTOR EFFICIENCY ZONE PREDICTOR (Type 'q' to quit)")
print("=" * 60)

# Map numeric classes to human-readable labels
class_labels = {
    2: "🟢 High Efficiency Sweet Spot (>92%) - Optimal Zone",
    1: "🟡 Moderate Efficiency (85% - 92%) - Acceptable Zone",
    0: "🔴 Low Efficiency (<85%) - High Thermal Losses Zone"
}

# 3. Interactive While Loop for live classroom experimentation
while True:
    user_input = input("\nPress Enter to test an operating point (or type 'q' to quit): ").strip().lower()
    if user_input == 'q':
        print("\n🎓 Amazing job leading your tech camp! Have an incredible final wrap-up session!")
        break

    try:
        print("\n--- Enter Motor Operating Parameters ---")
        motor_torque_nm = float(input("Motor Torque (Nm) [e.g., 110]: "))
        motor_speed_rpm = float(input("Motor Speed (RPM) [e.g., 4000]: "))
        switching_freq_hz = float(input("Inverter Switching Frequency (Hz) [e.g., 10000]: "))

        # Package inputs into a DataFrame
        sample_point = pd.DataFrame({
            'motor_torque_nm': [motor_torque_nm],
            'motor_speed_rpm': [motor_speed_rpm],
            'switching_freq_hz': [switching_freq_hz]
        })

        # Predict efficiency class
        predicted_class_idx = efficiency_classifier.predict(sample_point)[0]
        result_label = class_labels[predicted_class_idx]

        print("-" * 55)
        print(f"📊 Predicted Efficiency Status: {result_label}")
        print("-" * 55)

    except ValueError:
        print("❌ Invalid input! Please enter numerical values.")
