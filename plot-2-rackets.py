import sys
import pandas as pd
import matplotlib.pyplot as plt

# Change this to the path of your CSV file
file1 = sys.argv[1]
file2 = sys.argv[2]

# Read the CSV file into a pandas DataFrame
data1 = pd.read_csv(file1)
data2 = pd.read_csv(file2)

# Print the DataFrame columns for verification
print("Columns in CSV:", data1.columns)

# Determine if there's a 'time' column; otherwise create one
if 'time' not in data1.columns:
    sample_rate = 1000  # Adjust this to your sensor's sample rate
    data1['time'] = data1.index / sample_rate
    data2['time'] = data2.index / sample_rate


# Group accelerometer and gyroscope columns
accel_columns = ['ax', 'ay', 'az']
gyro_columns = ['gx', 'gy', 'gz']

# Create one figure with 2 columns: accel on left, gyro on right
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 10))

for i, col in enumerate(accel_columns):
    ax = axes[i][0]
    ax.plot(data1['time'], data1[col], label=f'File 1')
    ax.plot(data2['time'], data2[col], label=f'File 2', linestyle='--')
    ax.set_title(f"Accelerometer {col[1].upper()} Axis")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"{col} (m/s^2)")
    ax.grid(True)
    ax.legend()

for i, col in enumerate(gyro_columns):
    ax = axes[i][1]
    ax.plot(data1['time'], data1[col], label=f'File 1')
    ax.plot(data2['time'], data2[col], label=f'File 2', linestyle='--')
    ax.set_title(f"Gyroscope {col[1].upper()} Axis")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"{col} (deg/s)")
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.suptitle("Sensor Data Comparison (File 1 vs File 2)", fontsize=16, y=1.02)
plt.show()
