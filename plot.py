import pandas as pd
import matplotlib.pyplot as plt

# Change this to the path of your CSV file
csv_file = 'cam_output/2/Data.csv'

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(csv_file)

# Print the DataFrame columns for verification
print("Columns in CSV:", data.columns)

# If your CSV file doesn't have a time column, you can create one.
# Here, we assume a fixed sample rate. For example, if your sensor is sampled at 1000Hz:
sample_rate = 1000  # samples per second
data['time'] = data.index / sample_rate  # time in seconds

# Create a figure with two subplots: one for accelerometer data, one for gyroscope data
plt.figure(figsize=(12, 8))

# Plot accelerometer data
plt.subplot(2, 1, 1)
plt.plot(data['time'], data['ax'], label='Accel X')
plt.plot(data['time'], data['ay'], label='Accel Y')
plt.plot(data['time'], data['az'], label='Accel Z')
plt.title('Accelerometer Data')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (units)')
plt.legend()
plt.grid(True)

# Plot gyroscope data
plt.subplot(2, 1, 2)
plt.plot(data['time'], data['gx'], label='Gyro X')
plt.plot(data['time'], data['gy'], label='Gyro Y')
plt.plot(data['time'], data['gz'], label='Gyro Z')
plt.title('Gyroscope Data')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity (units)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
