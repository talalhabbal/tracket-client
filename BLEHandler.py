import asyncio
import struct
from bleak import BleakClient
import time

SERVICE_UUID =          "12345678-1234-1234-1234-123456789ABC"
DATA_CHAR_UUID =        "12345678-1234-1234-1234-123456789AB1"
BUFFER_SIZE =           10
READINGS_PER_SAMPLE =   6
PACKET_SIZE =           BUFFER_SIZE * READINGS_PER_SAMPLE * 4


class BLEHandler:
    def __init__(self, address, file_handler):
        self.address = address
        self.client = BleakClient(self.address, timeout=60)
        self.running = asyncio.Event()
        self.connected = False
        self.time_last_notif = None
        self.file_handler = file_handler
    
    #Handles connecting to the device
    async def connect(self):
        """
        Connects to the device with the given address from the :class:`BLEHandler`'s `address` attribute
        """
        try:
            await self.client.connect()
            self.connected = self.client.is_connected # Returns whether the client is connected or not
            if self.connected:
                print(f"Connected to {self.address}") # Prints the address of the device its connected to   
        except Exception as e:
            print(f"Connection error: {e}")
            
    # Handles disconnecting from the device
    async def disconnect(self):
        """
        Disconnects from the currently connected device
        """
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            self.connected = False
            print("Disconnected from device.")
    
    #Handles notification received from device
    def notification_handler(self, sender, data):
        """
        Handles notifications by creating a task to process incoming data. Notifications and data are handled
        separately to reduce overhead of processing the notification and the data at the same time to reduce
        latency and delay between readings.
        """
        current_time = time.time()
        if self.time_last_notif is not None:
            interval = current_time - self.time_last_notif
            print(f"Time between notifications: {interval}")
        self.time_last_notif = current_time
        if not self.running.is_set():
            return
        asyncio.create_task(self.process_data(data))
    
    #Processes the incoming data
    async def process_data(self, data):
        """
        Processes incoming data by unpacking it using :class:`struct.unpack()` and adding it to a list. (For the time being)
        """
        sample_size = READINGS_PER_SAMPLE * 4
        num_of_samples = len(data) // sample_size # length of the data sent from arduino // the size of each sample
        
        try:
            format = '<' + 'f' * (num_of_samples * READINGS_PER_SAMPLE)
            values = struct.unpack(format, data)
            samples = [values[i:i+READINGS_PER_SAMPLE] for i in range(0, len(values), READINGS_PER_SAMPLE)]
            for sample in samples:
                await self.file_handler.add_sample(list(sample))
            print(f"Received {num_of_samples} samples")
        
        except Exception as e:
            print(f"Error Processing Data: {e}")
            
    #Sets the running flag to True
    async def start_reading(self):
        """
        Starts Reading data from connected device.
        """
        print("Starting Reading incoming data...")
        self.running.set()
        try:
            await self.client.start_notify(DATA_CHAR_UUID, self.notification_handler)
        except Exception as e:
            print(f"Starting Reading Error: {e}")
    
    #Sets the running flag to False
    async def stop_reading(self):
        """
        Stops Reading data from connected device.
        """
        print(f"Stopping Reading incoming data...")
        if self.running.is_set():
            self.running.clear()
            try:
                await self.client.stop_notify(DATA_CHAR_UUID)
                self.time_last_notif = None
            except Exception as e:
                print(f"Stopping Reading Error: {e}")
    
    #Monitors BLE connection
    async def monitor_connection(self):
        """
        Monitors the BLE connection and auto-reconnects if connection drops.
        """
        while True:
            await asyncio.sleep(5)
            if self.client and not self.client.is_connected:
                self.client = BleakClient(self.address, timeout=60)
                print("Device disconnected. Attemping to reconnect...")
                await self.connect()