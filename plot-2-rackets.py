import sys
import pandas as pd
import matplotlib.pyplot as plt
import io

def clean_csv_file(path, max_columns=7):
    with open(path, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line for line in lines if len(line.strip().split(',')) <= max_columns]
    return pd.read_csv(io.StringIO(''.join(cleaned_lines)))

# File paths from command line arguments
file1 = sys.argv[1]
file2 = sys.argv[2]

# Read the cleaned CSV files
data1 = clean_csv_file(file1)
data2 = clean_csv_file(file2)

# Print columns for verification
print("Columns in CSV:", data1.columns)

# Group accelerometer and gyroscope columns
accel_columns = ['ax', 'ay', 'az']
gyro_columns = ['gx', 'gy', 'gz']

# Create one figure with 2 columns: accel on left, gyro on right
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 10))

for i, col in enumerate(accel_columns):
    ax = axes[i][0]
    ax.plot(data1.index, data1[col], label='File 1')
    ax.plot(data2.index, data2[col], label='File 2', linestyle='--')
    ax.set_title(f"Accelerometer {col[1].upper()} Axis")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel(f"{col} (m/s^2)")
    ax.grid(True)
    ax.legend()

for i, col in enumerate(gyro_columns):
    ax = axes[i][1]
    ax.plot(data1.index, data1[col], label='File 1')
    ax.plot(data2.index, data2[col], label='File 2', linestyle='--')
    ax.set_title(f"Gyroscope {col[1].upper()} Axis")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel(f"{col} (deg/s)")
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.suptitle("Sensor Data Comparison (File 1 vs File 2)", fontsize=16, y=1.02)
plt.show()
