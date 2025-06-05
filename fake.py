import time
import numpy as np
import pandas as pd

def generate_sensor_data_bell(
    start_time: int,
    num_samples: int = 500,
    total_time: float = 10.0,
    noise_std_acc: float = 0.02,
    noise_std_gyro: float = 0.1,
    center_time: float = 5.0,
    width_acc: float = 2.0,
    width_gyro: float = 3.0
) -> pd.DataFrame:
    """
    Generate fake sensor data (accelerometer and gyroscope) where each axis
    follows a Gaussian (bell curve) over time with added noise.

    Returns a pandas DataFrame with columns:
        time, ax, ay, az, gx, gy, gz

    Args:
        num_samples: Number of samples to generate.
        total_time: Total duration (in seconds).
        noise_std_acc: Standard deviation of added noise for accelerometer.
        noise_std_gyro: Standard deviation of added noise for gyroscope.
        center_time: Center of the Gaussian curve (in seconds).
        width_acc: Width (standard deviation) of Gaussian for accel axes.
        width_gyro: Width (standard deviation) of Gaussian for gyro axes.
    """
    # Create time axis
    time = np.linspace(0, total_time, num_samples) + start_time
    
    # Accelerometer true signals (bell curves)
    ax = 1.0 * np.exp(-((time - center_time) ** 2) / (2 * width_acc ** 2))
    ay = 0.8 * np.exp(-((time - center_time) ** 2) / (2 * width_acc ** 2))
    az = 9.81 + 0.5 * np.exp(-((time - center_time) ** 2) / (2 * width_acc ** 2))
    
    # Gyroscope true signals (bell curves at different scale/width)
    gx = 0.05 * np.exp(-((time - center_time) ** 2) / (2 * width_gyro ** 2))
    gy = 0.04 * np.exp(-((time - center_time) ** 2) / (2 * width_gyro ** 2))
    gz = 0.1 * np.exp(-((time - center_time) ** 2) / (2 * width_gyro ** 2))
    
    # Add Gaussian noise
    ax = ax + np.random.normal(0, noise_std_acc, size=time.shape)
    ay = ay + np.random.normal(0, noise_std_acc, size=time.shape)
    az = az + np.random.normal(0, noise_std_acc, size=time.shape)

    gx = gx + np.random.normal(0, noise_std_gyro, size=time.shape)
    gy = gy + np.random.normal(0, noise_std_gyro, size=time.shape)
    gz = gz + np.random.normal(0, noise_std_gyro, size=time.shape)
    
    # Build DataFrame
    df = pd.DataFrame({
        'time': time,
        'ax': ax,
        'ay': ay,
        'az': az,
        'gx': gx,
        'gy': gy,
        'gz': gz
    })
    
    return df

data1 = generate_sensor_data_bell(0, 500,10,0.002,0.001,5.0,2.0,3.0)
data1.to_csv("Data.csv", index=False)
data1 = generate_sensor_data_bell(0, 500,10,0.002,0.001,7.0,2.0,3.0)
data1.to_csv("Data1.csv", index=False)
