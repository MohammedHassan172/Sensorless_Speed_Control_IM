import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib  # For saving and loading the scaler

# Load training data
data = pd.read_csv('Training_data4_perunit.csv')

# Prepare inputs and outputs
x1 = data['Ia magnitude'].values
x2 = data['Ib magnitude'].values
x3 = data['Ic magnitude'].values

y1 = data['Speed'].values
y2 = data['Torque'].values

# Combine inputs and outputs
inputs = np.column_stack([x1, x2, x3])
outputs = np.column_stack([y1, y2])

# Split into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(inputs, outputs, test_size=0.2, random_state=42)

# Standardize the inputs
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_val = scaler.transform(x_val)

# Save the scaler for future use
joblib.dump(scaler, 'scaler_ABC_PerUnit.pkl')

# Define the model with a deeper architecture and dropout
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(2)  # Output layer for predicting Speed and Torque
])

# Compile the model with MAE loss and a smaller learning rate
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
              loss=tf.keras.losses.MeanAbsoluteError(), 
              metrics=['mae'])

# Use early stopping to avoid overfitting
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

# Train the model
history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=1000,
    batch_size=16,
    callbacks=[early_stopping],  # Include early stopping
)

# Save the model
model.save('speed_torque_model_ABC_PerUnit.h5')

# Plotting the learning curves
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Train Loss', color='blue')
plt.plot(history.history['val_loss'], label='Validation Loss', color='orange')
plt.title('Learning Curves')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# Function to get user input
def get_user_input():
    try:
        # Prompting user for input values
        x1 = float(input("Enter Ia magnitude: "))
        x2 = float(input("Enter Ib magnitude: "))
        x3 = float(input("Enter Ic magnitude: "))
        return np.array([[x1, x2, x3]])  # Return as a 2D array
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return get_user_input()  # Retry on invalid input


# Infinite testing loop
try:
    while True:
        # Get user input
        new_input = get_user_input()

        # Standardize the new input using the same scaler used during training
        new_input_scaled = scaler.transform(new_input)  # Use transform instead of fit_transform

        # Make predictions
        predictions = model.predict(new_input_scaled)

        # Display the predictions
        print(f"Predicted Speed: {predictions[0][0]}, Predicted Torque: {predictions[0][1]}")

except KeyboardInterrupt:
    print("Testing loop stopped.")
